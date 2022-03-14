import unittest
from scrapers import logger
import logging
from scrapers.aimis_simia.aimis_simia_scraper import Aimis
import os
class TestAimis(unittest.TestCase):

    test = Aimis(CSV_FOLDER_PATH=os.environ.get("CSV_UNIT_TEST_PATH"))

    def test_aimis_scraper(self):
        aimis_logger = logger.get_logger("aimis_logger")
        try:
            self.test.scrape()
            assert os.path.exists(self.test.CSV_FOLDER_PATH + '/aimis_simia.csv') is True
            logging.info("aimis returned filled CSV file")

        except Exception as e:
            aimis_logger.error("Error: crashed at testcode", str(e))

if __name__ == "__main__":
    unittest.main()
