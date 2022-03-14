import unittest
from scrapers import logger

from scrapers.quandl.quandl import Quandl

class TestQuandl(unittest.TestCase):

    def test_Quandl_scrape(self):
        quandl_logger = logger.get_logger("aus_logger")
        try:
            Quandl.quandl_scraper(self)
            quandl_logger.info("Quandl returned filled CSV file")

        except Exception as e:
            quandl_logger.error("Error: crashed at testcode", str(e))

if __name__ == "__main__":
    unittest.main()

