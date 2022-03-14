from scrapers.tesco.tesco import Tesco, BeautifulSoup
import unittest
import os


class TestTesco(unittest.TestCase):

    test_path = os.environ.get("CSV_UNIT_TEST_PATH")
    obj = Tesco(CSV_FOLDER_PATH=test_path)

    def test_scrape(self):
        # Scrape everything
        self.obj.scrape()

        # Check whether csv file was created
        assert os.path.exists(self.obj.CSV_FILE_PATH) is True

    def test_scrape_products(self):
        self.obj.driver.get("https://www.tesco.ie/groceries/product/browse/default.aspx?N=4294829730&Ne=4294954028")
        soup = BeautifulSoup(self.obj.driver.page_source, "lxml")

        # Assert dictionary is not empty
        assert not self.obj.scrape_products(soup, "Fresh Food", "Fresh Fruit") is False

    def test_get_menu_dict(self):
        # Assert dictionary is not empty
        assert not self.obj.get_menu_dict() is False


if __name__ == "__main__":
    unittest.main()
