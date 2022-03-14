
import unittest
from scrapers.logger import logging
from scrapers import logger as l
from scrapers.Zuivelnl.zuive_products import ZuiveProd
import os



class TestZuiveProd(unittest.TestCase):
        test = ZuiveProd(CSV_FOLDER_PATH=os.environ.get("CSV_UNIT_TEST_PATH"))

        def test_scrape(self):
            lean_hogs = l.get_logger("Zuive products")

            self.test.scrape()
            assert os.path.exists(self.test.CSV_FOLDER_PATH + '/Products') is True
            logging.info("Zuive products CSV files created")

if __name__ == "__main__":
        unittest.main()

