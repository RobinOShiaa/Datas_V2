import unittest
from scrapers import logger
import logging
from scrapers.cme_group.soybean_settlements import soy_settlements
import os


class TestSoy_settlements(unittest.TestCase):
    test = soy_settlements(CSV_FOLDER_PATH=os.environ.get("CSV_UNIT_TEST_PATH"))

    def test_scrape(self):
        soybean_logger = logger.get_logger("soy_settlements")

        self.test.scrape()
        assert os.path.exists(self.test.CSV_FOLDER_PATH + '/SoyBean.csv') is True
        logging.info("SoyBean CSV file created")


if __name__ == "__main__":
    unittest.main()
