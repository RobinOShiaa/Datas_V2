import unittest
from scrapers import logger
import os
from scrapers.clal.clal_dutch_smp_price_weekly import Clal_SMP

class TestClal_Milk_prices_fmgt(unittest.TestCase):
    test = Clal_SMP(CSV_FOLDER_PATH=os.environ.get("CSV_UNIT_TEST_PATH"))
    def test_scrape(self):
        clal = logger.get_logger("clal_logger")
        try:
            self.test.scrape()
            assert os.path.exists(self.test.CSV_FOLDER_PATH) is True
            clal.info(" filled CSV folder")

        except Exception as e:
            clal.error("Error: crashed at testcode", str(e))

    if __name__ == "__main__":
        unittest.main()

