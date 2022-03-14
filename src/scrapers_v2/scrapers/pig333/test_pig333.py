from scrapers.pig333.pig333 import Pig333
import unittest
import os

class TestPig333(unittest.TestCase):

    obj = Pig333(CSV_FOLDER_PATH=os.environ.get("CSV_UNIT_TEST_PATH"))

    def test_scrape(self):
        self.obj.scrape()


if __name__ == "__main__":
    unittest.main()
