
import unittest
from scrapers import logger
import logging
from scrapers.sainsburys.sainsburys import Sainsburys
import os

class TestSainsburys(unittest.TestCase):
    def test_scrape(self):
        test = Sainsburys(CSV_FOLDER_PATH=os.environ.get("CSV_UNIT_TEST_PATH"))

        lean_hogs = logger.get_logger("Sainsburys")

        test.scrape()
        assert os.path.exists(test.CSV_FOLDER_PATH + '/sainsburys.csv') is True
        logging.info("Sainsburys CSV file created")

