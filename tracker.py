import praw
import re
from datetime import datetime
import yaml
import sqlite3
import os
import requests
import argparse


def init_praw(**options):
    client_id = options.get("client_id")
    client_secret = options.get("client_secret")
    user_agent = options.get("user_agent")
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
    )
    return reddit


def init_db():
    conn = sqlite3.connect("posts.db")
    c = conn.cursor()
    c.execute(
        """CREATE TABLE posts (
        title TEXT,
        author TEXT,
        score INTEGER,
        date TEXT,
        url TEXT,
        tldr BLOB
    )"""
    )
    conn.commit()
    conn.close()


def parse_selftext(selftext, **options):
    tracked_users = options.get("tracked_users")
    selftext_regex = re.compile(r"|".join(options.get("words")))
    selftext = selftext.split("\n")

    if tracked_users:
        if options.get("author") in tracked_users:
            return selftext if selftext else ["Link Post"]

    for index, line in reversed(list(enumerate(selftext))):
        selftext_match = selftext_regex.match(line.lower())
        if selftext_match:
            return selftext[index:]

    return []


def send_discord_message(message, **options):
    webhook_url = options.get("webhook_url")
    username = options.get("username")
    avatar_url = options.get("avatar_url")
    data = {
        "username": username,
        "avatar_url": avatar_url,
        "content": message,
    }
    requests.post(webhook_url, data=data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Pass config into tracker.py')
    parser.add_argument('--config', help="name of config file")
    args = parser.parse_args()

    with open("./config/{}.yaml".format(args.config), "r") as f:
        print(args.config)
        config = yaml.safe_load(f)
        reddit_bot = config.get("reddit_bot")
        discord = config.get("discord")

    if not os.path.exists("posts.db"):
        init_db()

    discord_info = {
        "webhook_url": discord.get("webhook_url"),
        "username": discord.get("username"),
        "avtar_url": discord.get("avatar_url"),
    }
    reddit = init_praw(
        client_id=reddit_bot.get("client_id"),
        client_secret=reddit_bot.get("client_secret"),
        user_agent=reddit_bot.get("user_agent"),
    )
    subreddit = reddit.subreddit(reddit_bot.get("subreddit_name"))

    conn = sqlite3.connect("posts.db")
    c = conn.cursor()

    if reddit_bot.get("filter") == "hot":
        subreddit = subreddit.hot(limit=reddit_bot.get("num_limit"))
    elif reddit_bot.get("filter") == "new":
        subreddit = subreddit.new(limit=reddit_bot.get("num_limit"))
    elif reddit_bot.get("filter") == "rising":
        subreddit = subreddit.rising(limit=reddit_bot.get("num_limit"))
    elif reddit_bot.get("filter") == "top":
        subreddit = subreddit.top(limit=reddit_bot.get("num_limit"))

    for submission in subreddit:
        parser = parse_selftext(
            submission.selftext,
            words=reddit_bot.get("keywords"),
            author=submission.author.name,
            tracked_users=reddit_bot.get("tracked_users"),
        )
        if parser:
            query_dict = {
                "url": "https://old.reddit.com/{}".format(submission.permalink)
            }
            c.execute("SELECT url FROM posts WHERE url = :url", query_dict)

            if not c.fetchone():
                c.execute(
                    "INSERT INTO posts (title, author, score, date, url, tldr) VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        submission.title,
                        submission.author.name,
                        submission.score,
                        datetime.fromtimestamp(submission.created_utc),
                        "https://old.reddit.com/{}".format(submission.permalink),
                        "\n".join(parser),
                    ),
                )
                formatted_message = "Title: {}\nAuthor: {}\nScore: {}\nDate: {}\nURL: <{}>\n```{}```".format(
                    submission.title,
                    submission.author.name,
                    submission.score,
                    datetime.fromtimestamp(submission.created_utc),
                    "https://old.reddit.com/{}".format(submission.permalink),
                    "\n".join(parser),
                )
                send_discord_message(formatted_message, **discord_info)

    conn.commit()
    conn.close()
