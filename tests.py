import unittest
from scraper import Scraper

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
    self.assertTrue(Scraper(db_dir="custom_dir", db_name="custom_db", table_name="custom_table"))

  def test_post_save_default_group(self):
    """
    Save a post to the database with the default group.
    """
    s = Scraper()
    self.assertTrue(s.post_save(post_link="https://reddit.com", post_title="Test Post", post_author="Test Author", post_date="1623611382", post_score=500))

  def test_post_save_custom_group(self):
    """
    Save a post to the database with a custom group.
    """
    s = Scraper()
    self.assertTrue(s.post_save(post_link="https://reddit.com", post_title="Test Post", post_author="Test Author", post_date="1623611382", post_score=500, post_group="custom_group"))
  
  def test_post_save_duplicate(self):
    """
    Attempt to save a post that is a duplicate.
    """
    s = Scraper()
    self.assertFalse(s.post_save(post_link="https://reddit.com", post_title="Test Post", post_author="Test Author", post_date="1623611382", post_score=500, post_group="custom_group"))

if __name__ == "__main__":
  unittest.main()
