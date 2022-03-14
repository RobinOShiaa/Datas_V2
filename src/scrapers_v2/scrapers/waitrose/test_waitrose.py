
import unittest
from scrapers import logger
import logging
from scrapers.waitrose.waitrose import waitrose
import os


class TestWaitrose(unittest.TestCase):
    def test_scrape(self):
        test = waitrose(CSV_FOLDER_PATH=os.environ.get("CSV_UNIT_TEST_PATH"))

        lean_hogs = logger.get_logger("Waitrose")

        test.scrape()
        assert os.path.exists(test.CSV_FOLDER_PATH + '/waitrose.csv') is True
        logging.info("Waitrose CSV file created")



if __name__ == "__main__":
        unittest.main()
