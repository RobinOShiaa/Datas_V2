import unittest
from scrapers import logger
import logging
from scrapers.cme_group.live_hog_quotes import lean_hog
import os



class TestLive_cattle(unittest.TestCase):

    test = lean_hog(CSV_FOLDER_PATH=os.environ.get("CSV_UNIT_TEST_PATH"))
    def test_scrape(self):
        lean_hogs = logger.get_logger("Lean_Hog.csv")

        self.test.scrape()
        assert os.path.exists(self.test.CSV_FOLDER_PATH + '/Lean_Hog.csv') is True
        logging.info("Lean_Hog CSV file created")












    if __name__ == "__main__":
        unittest.main()
