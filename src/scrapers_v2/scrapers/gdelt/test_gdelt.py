from unittest import TestCase
from scrapers.gdelt.gdelt import gdelt
import unittest
import os
from scrapers import logger

class TestGdelt(TestCase):
    test = gdelt(CSV_FOLDER_PATH=os.environ.get("CSV_UNIT_TEST_PATH"))
    def test_download(self):

        loggergdelt = logger.get_logger("logger gdelt")
        try:
            self.test.scrape()
            assert os.path.exists(self.test.CSV_FOLDER_PATH + '/dairy_australia_export.csv') is True
            loggergdelt.info("bord returned filled CSV file")

        except Exception as e:
            loggergdelt.error("Error: crashed at testcode", str(e))

if __name__ == "__main__":
    unittest.main()

