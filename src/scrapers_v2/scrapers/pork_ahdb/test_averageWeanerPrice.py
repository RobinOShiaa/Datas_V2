from scrapers.pork_ahdb.average_weaner_price import AverageWeanerPrice
import unittest
import os


class TestAverageWeanerPrice(unittest.TestCase):

    test_path = os.environ.get("CSV_UNIT_TEST_PATH")
    obj = AverageWeanerPrice(CSV_FOLDER_PATH=test_path)

    def test_scrape(self):
        duration = 0.5
        self.obj.scrape(duration)
        assert os.path.exists(self.obj.CSV_FOLDER_PATH + "/{}_average_weaner_price.csv".format(duration)) is True


if __name__ == "__main__":
    unittest.main()
