import unittest
from scrapers import logger
import os
from scrapers.dairy_australia.rdairy_australia_export import DairyAustraliaExport

class TestDairyAustraliaExport(unittest.TestCase):

    test = DairyAustraliaExport(CSV_FOLDER_PATH=os.environ.get("CSV_UNIT_TEST_PATH"))

    def test_aus_scrape(self):
        aus_logger = logger.get_logger("aus_logger")
        try:
            self.test.scrape()
            assert os.path.exists(self.test.CSV_FOLDER_PATH + '/dairy_australia_export.csv') is True
            aus_logger.info("bord returned filled CSV file")

        except Exception as e:
            aus_logger.error("Error: crashed at testcode", str(e))

if __name__ == "__main__":
    unittest.main()

