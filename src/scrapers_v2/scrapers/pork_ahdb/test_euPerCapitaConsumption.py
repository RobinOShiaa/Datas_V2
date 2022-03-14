from scrapers.pork_ahdb.eu_per_capita_consumption import EuPerCapitaConsumption
import unittest
import os


class TestEuPerCapitaConsumption(unittest.TestCase):

    test_path = os.environ.get("CSV_UNIT_TEST_PATH")
    obj = EuPerCapitaConsumption(CSV_FOLDER_PATH=test_path)

    def test_scrape(self):
        self.obj.scrape()
        assert os.path.exists(self.obj.CSV_FOLDER_PATH + "/eu_per_capita_consumption.csv") is True


if __name__ == "__main__":
    unittest.main()
