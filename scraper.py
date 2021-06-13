# imports

import sqlite3
import os

# globals

# program

class Scraper:
    def __init__(self, **options):
        """
        db_dir (str): name of the directory to store the database
        db_name (str): name of the db file excluding the extension
        table_name (str): name of the table to store scraped posts
        """

        # constants

        self.SQL_CREATE_TABLE = """CREATE TABLE IF NOT EXISTS {table} (
                                    post_link TEXT NOT NULL,
                                    post_title TEXT NOT NULL,
                                    post_author TEXT NOT NULL,
                                    post_score INTEGER NOT NULL,
                                    post_date DATE NOT NULL,
                                    post_group TEXT NOT NULL,
                                    PRIMARY KEY (post_link, post_group)
                                );"""
        self.SQL_INSERT_POST = """INSERT INTO {table} (post_link, post_title, post_author, post_score, post_date, post_group)
                                VALUES(?, ?, ?, ?, ?, ?)"""
        self.SQL_SELECT_POST = """SELECT * FROM {table} WHERE post_link = ? AND post_group = ?"""
        self.DEFAULT_DB_DIR = "dbs"
        self.DEFAULT_DB_NAME = "db"
        self.DEFAULT_TABLE_NAME = "posts"
        self.DEFAULT_POST_GROUP = "default_group"

        self.db_dir = options.get("db_dir", self.DEFAULT_DB_DIR)
        if not os.path.exists(self.db_dir):
            os.makedirs(self.db_dir)

        self.db_name = options.get("db_name", self.DEFAULT_DB_NAME)

        self.conn = sqlite3.connect(os.path.join(self.db_dir, self.db_name))
        self.cursor = self.conn.cursor()

        self.table_name = options.get("table_name", self.DEFAULT_TABLE_NAME)

        self.cursor.execute(self.SQL_CREATE_TABLE.format(table=self.table_name))

    def post_exists(self, **options):
        """
        post_link (str): link of the post
        post_group (str): name of the group the post is saved under
        """

        post_link = options.get("post_link")
        post_group = options.get("post_group")

        self.cursor.execute(self.SQL_SELECT_POST.format(table=self.table_name), (post_link, post_group))

        return True if self.cursor.fetchall() else False


    def post_save(self, **options):
        """
        post_link (str): link of the post
        post_title (str): title of the post
        post_author (str): author of the post
        post_score (str): score of the post
        post_date (str): date of the post
        post_group (str): name of the group to save the post under
        """

        post_link = options.get("post_link")
        post_title = options.get("post_title")
        post_author = options.get("post_author")
        post_score = options.get("post_score")
        post_date = options.get("post_date")
        post_group = options.get("post_group", self.DEFAULT_POST_GROUP)

        if self.post_exists(post_link=post_link, post_group=post_group):
            return False

        self.cursor.execute(self.SQL_INSERT_POST.format(table=self.table_name), (post_link, post_title, post_author, post_score, post_date, post_group))
        self.conn.commit()

        return True


if __name__ == "__main__":
    s = Scraper()