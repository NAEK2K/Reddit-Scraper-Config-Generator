import praw
import re
from datetime import datetime
import yaml
import sqlite3
import os

#     TITLE TEXT,
#     SCORE INTEGER,
#     DATE TEXT,
#     URL TEXT,
#     TLDR TEXT

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

    for index, line in reversed(list(enumerate(selftext))):
        selftext_match = selftext_regex.match(line.lower())
        if selftext_match:
            return selftext[index:]

    return []


if __name__ == "__main__":
    if not os.path.exists("wsb_posts.db"):
        init_db()

    conn = sqlite3.connect("wsb_posts.db")

    c = conn.cursor()

    reddit = init_praw()

    subreddit = reddit.subreddit("wallstreetbets")

    for submission in subreddit.new(limit=100):
        parser = parse_selftext(submission.selftext, words=[".*tl(.|)dr.*"])
        if parser:
            # print("TITLE: {}\nSCORE: {}\nDATE: {}\nURL: {}".format(submission.title, submission.score, datetime.fromtimestamp(submission.created_utc), "https://old.reddit.com/{}".format(submission.permalink)))
            print("\n".join(parser))
            # print(50*"=")
            c.execute(
                "INSERT INTO wsb_posts (title, score, date, url, tldr) VALUES (?, ?, ?, ?, ?)",
                    (submission.title,
                    submission.score,
                    datetime.fromtimestamp(submission.created_utc),
                    "https://old.reddit.com/{}".format(submission.permalink),
                    "\n".join(parser))
            )
        print("Command executed successfully.")
    conn.commit()
    conn.close()