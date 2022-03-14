import unittest
from scrapers import logger

from scrapers.imf.imf import Imf

class TestImf(unittest.TestCase):

    test = Imf(CSV_FOLDER_PATH=os.environ.get("CSV_UNIT_TEST_PATH"))

    def test_aus_scrape(self):
        imf_logger = logger.get_logger("imf_logger")
        try:
            self.test.scrape()
            imf_logger.info("imf returned filled CSV file")

        except Exception as e:
            imf_logger.error("Error: crashed at testcode", str(e))

if __name__ == "__main__":
    unittest.main()

