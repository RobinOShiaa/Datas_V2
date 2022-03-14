from scrapers.usda.gats import Gats
import unittest


class TestGats(unittest.TestCase):

    obj = Gats(CSV_FOLDER_PATH=os.environ.get("CSV_UNIT_TEST_PATH"))

    def test_scrape(self):
        # Just get this data and see whether it completes
        self.obj.scrape(desired_stats=["trade_flow_casein"], product_type="imports - general", year_range=[2019, 2019])


if __name__ == "__main__":
    unittest.main()
