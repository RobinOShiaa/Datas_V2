import unittest
from scrapers import logger
import logging
from src.scrapers_v2.scrapers.eurostat.cows_milk_monthly import Eurostat_Cows_milk
import os

class TestEurostat_Cows_milk(unittest.TestCase):
    def test_scrape(self):
        test = Eurostat_Cows_milk(CSV_FOLDER_PATH=os.environ.get("CSV_UNIT_TEST_PATH"))

        lean_hogs = logger.get_logger("Eurostat Cows Milk")

        test.scrape()
        assert os.path.exists(test.CSV_FOLDER_PATH + '/apro_mk_colm.csv') is True
        logging.info("Cow Milk CSV file created")

