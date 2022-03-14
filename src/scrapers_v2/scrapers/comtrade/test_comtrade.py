
import unittest
from scrapers import logger
import logging
from scrapers.comtrade.comtrade import comtrade
import os

class TestComtrade(unittest.TestCase):
    def test_scrape(self):
        test = comtrade(CSV_FOLDER_PATH=os.environ.get("CSV_UNIT_TEST_PATH"))


        com = logger.get_logger("comtrade")
        test.scrape()
        assert os.path.exists(test.CSV_FOLDER_PATH + '/comtrade.csv') is True
        logging.info("comtrade.csv CSV file created")












if __name__ == "__main__":
    unittest.main()
