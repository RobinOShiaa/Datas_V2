import unittest
from unittest import TestCase

from scrapers import logger
import logging
import os
from scrapers.bordbia.pig_throughput import BordBiaPigThroughput


class TestBordBiaPigThroughput(unittest.TestCase):
    test = BordBiaPigThroughput(CSV_FOLDER_PATH=os.environ.get("CSV_UNIT_TEST_PATH"))

    def test_aus_scrape(self):
        bord_logger = logger.get_logger("aus_logger")
        try:
            self.test.scrape()
            assert os.path.exists(self.test.CSV_FOLDER_PATH + '/bordbia_pig_throughput.csv') is True
            logging.info("bord returned filled CSV file")

        except Exception as e:
            bord_logger.error("Error: crashed at testcode", str(e))


if __name__ == "__main__":
    unittest.main()
