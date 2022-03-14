from scrapers.pork_ahdb.eu_weekly_pig_slaughterings_historical import EuWeeklyPigSlaughteringsHistorical
import unittest
import os


class TestEuWeeklyPigSlaughteringsHistorical(unittest.TestCase):

    test_path = os.environ.get("CSV_UNIT_TEST_PATH")
    obj = EuWeeklyPigSlaughteringsHistorical(CSV_FOLDER_PATH=test_path)

    def test_scrape(self):
        self.obj.scrape()

        # Sheet 1
        assert os.path.exists(self.obj.CSV_FOLDER_PATH + "/eu_weekly_pig_slaughterings_historical_clean_pigs.csv") is True

        # Sheet2
        assert os.path.exists(self.obj.CSV_FOLDER_PATH + "/eu_weekly_pig_slaughterings_historical_sows.csv") is True

    def test_is_decimal(self):
        assert self.obj.is_decimal("5.45") is True
        assert self.obj.is_decimal("-4.45") is True
        assert self.obj.is_decimal("-5") is False
        assert self.obj.is_decimal("5") is False


if __name__ == "__main__":
    unittest.main()
