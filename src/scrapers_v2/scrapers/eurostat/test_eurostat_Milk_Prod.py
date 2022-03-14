
from scrapers import logger
import logging
from src.scrapers_v2.scrapers.eurostat.milk_prod_annual import Eurostat_Milk_Prod
import os


class TestEurostat_Milk_Prod(TestCase):
    def test_scrape(self):
        test = Eurostat_Milk_Prod(CSV_FOLDER_PATH=os.environ.get("CSV_UNIT_TEST_PATH"))

        lean_hogs = logger.get_logger("Eurostat Milk Production")

        test.scrape()
        assert os.path.exists(test.CSV_FOLDER_PATH + '/apro_mk_farm.csv') is True
        logging.info("Milk Production Annual CSV file created")
