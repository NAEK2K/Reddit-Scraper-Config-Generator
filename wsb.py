import praw
import re
from datetime import datetime
import yaml
import sqlite3
import os
import requests

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)


def init_praw():
    reddit = praw.Reddit(
        client_id=config.get("reddit_bot", {}).get("client_id", {}),
        client_secret=config.get("reddit_bot", {}).get("client_secret", {}),
        user_agent=config.get("reddit_bot", {}).get("user_agent", {}),
    )
    return reddit


def init_db():
    conn = sqlite3.connect("wsb_posts.db")
    c = conn.cursor()
    c.execute(
        """CREATE TABLE wsb_posts (
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
    selftext_regex = re.compile(r"|".join(options.get("words")))
    selftext = selftext.split("\n")

    if config.get("reddit_bot").get("reputable_traders", []):
        if options.get("author") in config.get("reddit_bot", {}).get("reputable_traders", []):
            return selftext if selftext else ["Link Post"]

    for index, line in reversed(list(enumerate(selftext))):
        selftext_match = selftext_regex.match(line.lower())
        if selftext_match:
            return selftext[index:]

    return []

def send_discord_message(message, webhook_url=config.get("discord", {}).get("webhook_url", "")):
    data = {
        "username": config.get("discord", {}).get("username", "Unnamed Webhook"),
        "avatar_url": config.get("discord", {}).get("avatar_url", ""),
        "content": message
    }
    requests.post(webhook_url, data = data)


if __name__ == "__main__":
    if not os.path.exists("wsb_posts.db"):
        init_db()

    conn = sqlite3.connect("wsb_posts.db")
    c = conn.cursor()
    reddit = init_praw()
    subreddit = reddit.subreddit("wallstreetbets")

    for submission in subreddit.new(limit=100):
        parser = parse_selftext(submission.selftext, words=[".*tl(.|)dr.*"], author=submission.author.name)
        if parser:
            query_dict = {"url": "https://old.reddit.com/{}".format(submission.permalink)}
            c.execute("SELECT url FROM wsb_posts WHERE url = :url", query_dict)

            if not c.fetchone():
                c.execute(
                    "INSERT INTO wsb_posts (title, author, score, date, url, tldr) VALUES (?, ?, ?, ?, ?, ?)",
                        (submission.title,
                        submission.author.name,
                        submission.score,
                        datetime.fromtimestamp(submission.created_utc),
                        "https://old.reddit.com/{}".format(submission.permalink),
                        "\n".join(parser))
                )
                formatted_message = "Title: {}\nAuthor: {}\nScore: {}\nDate: {}\nURL: {}\n{}".format(submission.title, submission.author.name, submission.score, datetime.fromtimestamp(submission.created_utc), "https://old.reddit.com/{}".format(submission.permalink), "\n".join(parser))
                send_discord_message(formatted_message)

    conn.commit()
    conn.close()