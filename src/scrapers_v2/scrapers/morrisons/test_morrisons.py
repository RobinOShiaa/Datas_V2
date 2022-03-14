import unittest
from scrapers import logger
import logging
from scrapers.morrisons.morrisons import Morrisons
import os



class TestMorrisons(unittest.TestCase):
    def test_scrape(self):
        test =  Morrisons(CSV_FOLDER_PATH=os.environ.get("CSV_UNIT_TEST_PATH"))

        lean_hogs = logger.get_logger("Morrisons")

        test.scrape()
        assert os.path.exists(test.CSV_FOLDER_PATH + '/morrisons.csv') is True
        logging.info("Morrisons CSV file created")


if __name__ == "__main__":
    unittest.main()
