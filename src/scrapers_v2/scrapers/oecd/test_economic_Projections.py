import unittest
from scrapers import logger
import logging
from scrapers.oecd.economic_projections import Economic_Projections
import os


class TestEconomic_Projections(unittest.TestCase):
    def test_scrape(self):
        test = Economic_Projections(CSV_FOLDER_PATH=os.environ.get("CSV_UNIT_TEST_PATH"))

        lean_hogs = logger.get_logger("Economic Projections")

        test.scrape()
        assert os.path.exists(test.CSV_FOLDER_PATH + '/EXT:.csv') is True
        logging.info("Economic Projections CSV file created")



if __name__ == "__main__":
    unittest.main()



