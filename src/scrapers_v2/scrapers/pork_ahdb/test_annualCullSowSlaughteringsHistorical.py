from scrapers.pork_ahdb.annual_cull_sow_slaughterings_historical import AnnualCullSowSlaughteringsHistorical
import unittest
import os


class TestAnnualCullSowSlaughteringsHistorical(unittest.TestCase):

    test_path = os.environ.get("CSV_UNIT_TEST_PATH")
    obj = AnnualCullSowSlaughteringsHistorical(CSV_FOLDER_PATH=test_path)

    def test_scrape(self):
        self.obj.scrape()
        assert os.path.exists(self.obj.CSV_FOLDER_PATH + "/annual_cull_sow_slaughterings_historical.csv") is True


if __name__ == "__main__":
    unittest.main()
