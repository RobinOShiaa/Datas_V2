import unittest
from scrapers import logger
import logging
from src.scrapers_v2.scrapers.eurostat.Population_annual import Eurostat_Population
import os


class TestEurostat_Population(unittest.TestCase):
    def test_scrape(self):
        test = Eurostat_Population(CSV_FOLDER_PATH=os.environ.get("CSV_UNIT_TEST_PATH"))

        lean_hogs = logger.get_logger("Eurostat Population")

        test.scrape()
        assert os.path.exists(test.CSV_FOLDER_PATH + '/apro_mt_lscatl.csv') is True
        logging.info("Population CSV file created")


