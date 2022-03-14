import unittest
from scrapers import logger
import logging
from src.scrapers_v2.scrapers.eurostat.pig_slaughterings import Eurostat_Slaughter
import os

class TestEurostat_Slaughter(unittest.TestCase):
    def test_scrape(self):
        test = Eurostat_Slaughter(CSV_FOLDER_PATH=os.environ.get("CSV_UNIT_TEST_PATH"))

        lean_hogs = logger.get_logger("Eurostat Pig Slaughter")

        test.scrape()
        assert os.path.exists(test.CSV_FOLDER_PATH + '/apro_mt_pwgtm.csv') is True
        logging.info("Milk Pig Slaughter CSV file created")


