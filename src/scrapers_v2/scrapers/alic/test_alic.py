from scrapers.alic.alic import Alic
import unittest
import os


class TestAlic(unittest.TestCase):

    obj = Alic(CSV_FOLDER_PATH=os.environ.get("CSV_UNIT_TEST_PATH"))

    def test_scrape(self):
        # Testing scrape() with specific categories.
        self.obj.scrape(["Supply and Demand for Livestock Products", "Meat relation"])

    def test_html_table_to_dict(self):
        # assert dictionary is not empty
        assert bool(self.obj.html_table_to_dict()) is not False

    def test_download_xlsx(self):
        # I'm assuming here this data exists on the website. If it doesn't this test will obviously fail.

        test_urls = ["Household Consumption (per capita)",
                     "http://lin.alic.go.jp/alic/statis/dome/data2/j_excel/1050a.xlsx",
                     "http://lin.alic.go.jp/alic/statis/dome/data2/OldDate/1050aD.xlsx",
                     "http://lin.alic.go.jp/alic/statis/dome/data2/FYDate/1050aFY.xlsx"]

        # Download the 3 Excel files above.
        self.obj.download_xlsx(test_urls)

        # Check whether files have been successfully downloaded.
        assert os.path.exists(self.obj.CSV_FOLDER_PATH +
                              "/household consumption (per capita)_recent 15 months data.xlsx") is True

        assert os.path.exists(self.obj.CSV_FOLDER_PATH +
                              "/household consumption (per capita)_previous data.xlsx") is True

        assert os.path.exists(self.obj.CSV_FOLDER_PATH +
                              "/household consumption (per capita)_fiscal year data.xlsx") is True


if __name__ == "__main__":
    unittest.main()
