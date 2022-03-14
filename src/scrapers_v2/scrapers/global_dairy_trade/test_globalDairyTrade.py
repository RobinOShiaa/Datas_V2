from scrapers.global_dairy_trade.global_dairy_trade import GlobalDairyTrade
import unittest
import os


class TestGlobalDairyTrade(unittest.TestCase):

    obj = GlobalDairyTrade(CSV_FOLDER_PATH=os.environ.get("CSV_UNIT_TEST_PATH"))

    def test_scrape(self):
        self.obj.scrape()
        assert os.path.exists(self.obj.CSV_FILE_PATH) is True

    def test_is_number(self):
        assert self.obj.is_number("$472") is True
        assert self.obj.is_number("$472.9") is True
        assert self.obj.is_number("$4,725") is True
        assert self.obj.is_number("$") is False
        assert self.obj.is_number("") is False

    def test_is_decimal(self):
        assert self.obj.is_decimal("472") is False
        assert self.obj.is_decimal("472.7") is True
        assert self.obj.is_decimal("-472.4") is True


if __name__ == "__main__":
    unittest.main()
