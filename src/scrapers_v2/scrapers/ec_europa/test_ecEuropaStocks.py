import unittest
from scrapers import logger
from scrapers.ec_europa.ec_europa_dairy_stocks import EcEuropaStocks
import os
class TestEcEuropaStocks(unittest.TestCase):

    test = EcEuropaStocks(CSV_FOLDER_PATH=os.environ.get("CSV_UNIT_TEST_PATH"))

    def test_ec_europa_stocks_scraper(self):
        ec_logger = logger.get_logger("ec_europa_logger")
        try:
            self.test.scrape()
            assert os.path.exists(self.test.CSV_FOLDER_PATH + '/ec_europa_dairy_stocks.csv') is True
            ec_logger.info("ec europa returned filled CSV file")

        except Exception as e:
            ec_logger.error("Error: crashed at testcode", str(e))

if __name__ == "__main__":
    unittest.main()
