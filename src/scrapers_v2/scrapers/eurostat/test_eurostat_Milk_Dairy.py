import unittest
from scrapers import logger
import logging
from src.scrapers_v2.scrapers.eurostat.milk_dairy_annual import Eurostat_Milk_Dairy
import os

class TestEurostat_Milk_Dairy(unittest.TestCase):
    def test_scrape(self):
        test = Eurostat_Milk_Dairy(CSV_FOLDER_PATH=os.environ.get("CSV_UNIT_TEST_PATH"))

        lean_hogs = logger.get_logger("Eurostat Trade")

        test.scrape()
        assert os.path.exists(test.CSV_FOLDER_PATH + '/apro_mk_pobta.csv') is True
        logging.info("Milk Dairy Annual CSV file created")




