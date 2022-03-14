from unittest import TestCase
from scrapers.zmb.zmb import Zmb
from scrapers import logger
import logging
import os
class TestZmb(TestCase):
    #zmb_test_logger = logger.get_logger("zmb_logger")
    test = Zmb(CSV_FOLDER_PATH=os.environ.get("CSV_UNIT_TEST_PATH"))
    def test_zmb_scraper(self):
        zmb_logger = logger.get_logger("zmb_logger")
        try:
            self.test.scrape()
            assert os.path.exists(self.test.CSV_FOLDER_PATH + '/zmb.csv') is True
            zmb_logger.info("zmb returned filled CSV file")
                    # assert output == {'Milchanlieferung': ('Auswertung 21', '620.897', '- 0,4%', '-1,9%')}
                    # check if the output dict is not an empty dict
        except Exception as e:
            zmb_logger.error("Error: crashed at testcode", str(e))

        logging.info("zmb returned filled dict")


