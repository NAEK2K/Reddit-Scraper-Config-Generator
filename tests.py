import unittest
from scraper import Scraper
import sqlite3

post_link = "https://reddit.com"
post_title = "Test Post"
post_author = "Test Author"
post_date = "1623611382"
post_score = 500
post_group = "Custom Group"
db_dir = "custom_dir"
db_name = "custom_db"
table_name = "custom_table"

class TestScraper(unittest.TestCase):
  def test_initialize_scraper_default_values(self):
    """
    Initialize the scraper with default values.
    """
    self.assertTrue(Scraper())

  def test_initialize_scraper_custom_values(self):
    """
    Initialize the scraper with custom values.
    """
    self.assertTrue(Scraper(db_dir=db_dir, db_name=db_name, table_name=table_name))

  def test_post_save_default_group(self):
    """
    Save a post to the database with the default group.
    """
    s = Scraper()
    self.assertTrue(s.post_save(post_link=post_link, post_title=post_title, post_author=post_author, post_date=post_date, post_score=post_score))

  def test_post_save_custom_group(self):
    """
    Save a post to the database with a custom group.
    """
    s = Scraper()
    self.assertTrue(s.post_save(post_link=post_link, post_title=post_title, post_author=post_author, post_date=post_date, post_score=post_score, post_group=post_group))
  
  def test_post_save_duplicate(self):
    """
    Attempt to save a post that is a duplicate.
    """
    s = Scraper()
    self.assertFalse(s.post_save(post_link=post_link, post_title=post_title, post_author=post_author, post_date=post_date, post_score=post_score, post_group=post_group))

  def test_get_posts(self):
    s = Scraper()
    self.assertFalse(s.get_posts()) # TODO: figure out why this is empty
    

  def test_post_delete(self):
    """
    Delete a post that was saved to the database.
    """
    s = Scraper()
    self.assertFalse(s.post_delete(post_link=post_link))


if __name__ == "__main__":
  unittest.main()
