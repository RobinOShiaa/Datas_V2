from scrapers.statsnz.statsnz import Statsnz
import unittest


class TestStatsnz(unittest.TestCase):

    obj = Statsnz(CSV_FOLDER_PATH=os.environ.get("CSV_UNIT_TEST_PATH"))

    def test_scrape(self):
        # Get data for dairy imports
        self.obj.scrape(start_date="2018M01", end_date="2019M02")

    def test_get_hs_codes(self):
        assert self.obj.get_hs_codes("0401", "0404") == ["0401", "0402", "0403", "0404"]

    def test_get_year_month_range(self):
        assert self.obj.get_year_month_range("2018M11", "2019M04") == ["2018M11", "2018M12", "2019M01", "2019M02",
                                                                       "2019M03", "2019M04"]


if __name__ == "__main__":
    unittest.main()
