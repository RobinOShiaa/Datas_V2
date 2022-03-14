from scrapers.usda.usda import Usda, datetime
import unittest


class TestUsda(unittest.TestCase):

    obj = Usda(CSV_FOLDER_PATH=os.environ.get("CSV_UNIT_TEST_PATH"))

    def test_scrape(self):
        # Just get this data and see whether it completes
        self.obj.scrape(desired_stats=["pig_crops"], year_range=[2014, 2015])

    def test_is_valid_year_range(self):
        current_year = datetime.now().year
        assert self.obj.is_valid_year_range([1915, current_year], current_year)
        assert self.obj.is_valid_year_range([2000, 2017], current_year)
        assert not self.obj.is_valid_year_range([1914, 1920], current_year)
        assert not self.obj.is_valid_year_range([1915, 2000, 2005], current_year)
        assert not self.obj.is_valid_year_range("w", current_year)
        assert not self.obj.is_valid_year_range(["w", "w"], current_year)


if __name__ == "__main__":
    unittest.main()
