import unittest
from scrapers import logger
import logging
from scrapers.statcan.statcan_hog_stocks import StatcanHog
import os
class TestStatcanHog(unittest.TestCase):

    test = StatcanHog(CSV_FOLDER_PATH=os.environ.get("CSV_UNIT_TEST_PATH"))

    def test_statcan_hog_scraper(self):
        statcan_logger = logger.get_logger("Statcan_logger")
        try:
            self.test.scrape()
            logging.info("Statcan returned filled CSV file")

        except Exception as e:
            statcan_logger.error("Error: crashed at testcode", str(e))
        statcan_logger.info('finished testing')
if __name__ == "__main__":
    unittest.main()
