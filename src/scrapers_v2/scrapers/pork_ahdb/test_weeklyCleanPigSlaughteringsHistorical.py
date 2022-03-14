from scrapers.pork_ahdb.weekly_clean_pig_slaughterings_historical import WeeklyCleanPigSlaughteringsHistorical
import unittest
import os


class TestWeeklyCleanPigSlaughteringsHistorical(unittest.TestCase):

    test_path = os.environ.get("CSV_UNIT_TEST_PATH")
    obj = WeeklyCleanPigSlaughteringsHistorical(CSV_FOLDER_PATH=test_path)

    def test_scrape(self):
        duration = 0.5
        self.obj.scrape(duration)
        assert os.path.exists(self.obj.CSV_FOLDER_PATH + "/{}_weekly_clean_pig_slaughterings_historical.csv".format(duration)) is True


if __name__ == "__main__":
    unittest.main()
