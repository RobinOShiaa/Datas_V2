import unittest
from scrapers import logger
import logging

from scrapers.Supervalue.supervalue import Supervlue
import os


class TestSupervlue(unittest.TestCase):
    def test_scrape(self):
            test = Supervlue(CSV_FOLDER_PATH=os.environ.get("CSV_UNIT_TEST_PATH"))


            lean_hogs = logger.get_logger("Supervalue")

            test.scrape()
            assert os.path.exists(test.CSV_FOLDER_PATH + '/SuperValue.csv') is True
            logging.info("Supervalue CSV file created")

    if __name__ == "__main__":
        unittest.main()

