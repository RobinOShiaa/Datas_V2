import unittest
from scrapers import logger
import os
from scrapers.clal.chees_prod import Clal_Cheese

class TestClal_Cheese(unittest.TestCase):

    test = Clal_Cheese(CSV_FOLDER_PATH=os.environ.get("CSV_UNIT_TEST_PATH"))

    def test_aus_scrape(self):
        clal = logger.get_logger("clal_logger")
        try:
            self.test.scrape()
            assert os.path.exists(self.test.CSV_FOLDER_PATH) is True
            clal.info(" filled CSV folder")

        except Exception as e:
            clal.error("Error: crashed at testcode", str(e))

if __name__ == "__main__":
    unittest.main()

