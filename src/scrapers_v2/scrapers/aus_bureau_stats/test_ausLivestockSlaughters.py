import unittest
from scrapers import logger
import logging
import os
from scrapers.aus_bureau_stats.aus_bureau_stats_scraper import AusLivestockSlaughters
class TestAusLivestockSlaughters(unittest.TestCase):

    test = AusLivestockSlaughters(CSV_FOLDER_PATH=os.environ.get("CSV_UNIT_TEST_PATH"))

    def test_aus_scrape(self):
        aus_logger = logger.get_logger("aus_logger")
        try:
            self.test.scrape()
            assert os.path.exists(self.test.CSV_FOLDER_PATH + '/aus_livestock_slaughters.csv') is True
            logging.info("aimis returned filled CSV file")

        except Exception as e:
            aus_logger.error("Error: crashed at testcode", str(e))

if __name__ == "__main__":
    unittest.main()

