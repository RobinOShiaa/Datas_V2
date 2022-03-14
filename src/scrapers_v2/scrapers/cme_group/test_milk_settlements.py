
import unittest
from scrapers import logger
import logging
from scrapers.cme_group.milk_settlements import milk_settlements
import os

class TestMilkSettlements(unittest.TestCase):

    test = milk_settlements(CSV_FOLDER_PATH=os.environ.get("CSV_UNIT_TEST_PATH"))

    def test_scrape(self):
        milk_settlement = logger.get_logger("milk_settlements")

        self.test.scrape()
        assert os.path.exists(self.test.CSV_FOLDER_PATH + '/milk_sett.csv') is True
        logging.info("milk_sett CSV file created")



if __name__ == "__main__":
    unittest.main()
