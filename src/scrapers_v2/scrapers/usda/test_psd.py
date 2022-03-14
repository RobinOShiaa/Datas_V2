from scrapers.usda.psd import Psd
import unittest


class TestPsd(unittest.TestCase):

    obj = Psd(CSV_FOLDER_PATH=os.environ.get("CSV_UNIT_TEST_PATH"))

    def test_scrape(self):
        # Just get this data and see whether it completes
        self.obj.scrape(desired_stats=["tree nuts"], year_range=[2017, 2019])

    def test_get_year_range(self):
        assert self.obj.get_year_range(year_range=[2017, 2019]) == [2017, 2018, 2019]


if __name__ == "__main__":
    unittest.main()
