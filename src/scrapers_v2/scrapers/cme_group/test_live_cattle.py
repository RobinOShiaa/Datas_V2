import unittest
from scrapers import logger
import logging
from scrapers.cme_group.live_cattle_quotes import live_cattle
import os


class TestLive_cattle(unittest.TestCase):

    test = live_cattle(CSV_FOLDER_PATH=os.environ.get("CSV_UNIT_TEST_PATH"))
    def test_scrape(self):
        live_cattles = logger.get_logger("cattle_quotes")

        self.test.scrape()
        assert os.path.exists(self.test.CSV_FOLDER_PATH + '/live_cattle.csv') is True
        logging.info("live_cattle.csv CSV file created")







    if __name__ == "__main__":
        unittest.main()
