import unittest
from scrapers import logger
import logging
from scrapers.walmart.walmart import Walmart
import os
class TestWalmart(unittest.TestCase):

    test = Walmart(CSV_FOLDER_PATH=os.environ.get("CSV_UNIT_TEST_PATH"))

    def test_walmart_scraper(self):
        walmart_logger = logger.get_logger("aimis_logger")
        try:
            self.test.scrape()
            assert os.path.exists(self.test.CSV_FOLDER_PATH + '/walmart.csv') is True
            logging.info("Walmart returned filled CSV file")

        except Exception as e:
            walmart_logger.error("Error: crashed at testcode", str(e))

if __name__ == "__main__":
    unittest.main()
