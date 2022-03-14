import unittest
from scrapers import logger as l
import logging
from scrapers.Zuivelnl.zuive_prices import ZuivePri
import os


class TestZuivePri(unittest.TestCase):
        test = ZuivePri(CSV_FOLDER_PATH=os.environ.get("CSV_UNIT_TEST_PATH"))
        def test_scrape(self):
            lean_hogs = l.get_logger("Zuive prices")

            self.test.scrape()
            assert os.path.exists(self.test.CSV_FOLDER_PATH + '/Prices') is True
            logging.info("Zuive prices CSV files created")



if __name__ == "__main__":
        unittest.main()