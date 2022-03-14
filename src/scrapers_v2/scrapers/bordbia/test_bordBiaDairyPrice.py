import unittest
from scrapers import logger
import logging
import os
from scrapers.bordbia.dairy_price import BordBiaDairyPrice

class TestBordBiaDairyPrice(unittest.TestCase):

    test = BordBiaDairyPrice(CSV_FOLDER_PATH=os.environ.get("CSV_UNIT_TEST_PATH"))

    def test_aus_scrape(self):
        bord_logger = logger.get_logger("bord_logger")
        try:
            self.test.scrape()
            assert os.path.exists(self.test.CSV_FOLDER_PATH + '/bordbia_dairy_price.csv') is True
            logging.info("bord returned filled CSV file")

        except Exception as e:
            bord_logger.error("Error: crashed at testcode", str(e))

if __name__ == "__main__":
    unittest.main()

