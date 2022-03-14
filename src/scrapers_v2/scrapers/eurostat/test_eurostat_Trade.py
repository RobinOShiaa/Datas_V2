import unittest
from scrapers import logger
import logging
from src.scrapers_v2.scrapers.eurostat.all_trade_monthly import Eurostat_Trade
import os

class TestEurostat_Trade(unittest.TestCase):
    def test_scrape(self):
        test = Eurostat_Trade(CSV_FOLDER_PATH=os.environ.get("CSV_UNIT_TEST_PATH"))

        lean_hogs = logger.get_logger("Eurostat Trade")

        test.scrape()
        assert os.path.exists(test.CSV_FOLDER_PATH + '/ei_eteu28_m.csv') is True
        logging.info("Trade Monthly CSV file created")



