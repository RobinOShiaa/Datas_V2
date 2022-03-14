import unittest
from scrapers import logger
import os
from scrapers.dairy_australia.dairy_australia_trade import DairyAustraliaTrade

class TestDairyAustraliaTrade(unittest.TestCase):

    test = DairyAustraliaTrade(CSV_FOLDER_PATH=os.environ.get("CSV_UNIT_TEST_PATH"))

    def test_aus_scrape(self):
        aus_logger = logger.get_logger("aus_logger")
        try:
            self.test.scrape()
            assert os.path.exists(self.test.CSV_FOLDER_PATH + '/dairy_australia_trade.csv') is True
            aus_logger.info("aus returned filled CSV file")

        except Exception as e:
            aus_logger.error("Error: crashed at testcode", str(e))

if __name__ == "__main__":
    unittest.main()

