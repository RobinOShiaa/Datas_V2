from unittest import TestCase
import unittest
from scrapers import logger
import logging
from scrapers.cme_group.live_corn_quotes import live_corn
import os

class TestLive_corn(TestCase):

    test = live_corn(CSV_FOLDER_PATH=os.environ.get("CSV_UNIT_TEST_PATH"))
    def test_scrape(self):

        live_corns = logger.get_logger("live corn")
        self.test.scrape()
        assert os.path.exists(self.test.CSV_FOLDER_PATH + '/live_corn.csv') is True
        logging.info("live_corn.csv CSV file created")









if __name__ == "__main__":
    unittest.main()
