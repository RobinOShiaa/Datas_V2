from selenium.webdriver.common.action_chains import ActionChains
from scraper_classes.chrome_scraper import ChromeScraper
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from scrapers.logger import get_logger
from datetime import datetime
import time
import glob
import csv
import os


class Gats(ChromeScraper):

    logger = get_logger("Usda")
    product_types = {
                        "exports": "X",
                        "imports - consumption": "C",
                        "imports - general": "G",
                        "re-exports": "R"
    }

    def scrape(self, desired_stats=None, product_type="imports - general", year_range=None):
        self.logger.info("Starting")
        self.driver.maximize_window()
        self.url = "https://apps.fas.usda.gov/gats/ExpressQuery1.aspx"
        self.driver.get(self.url)
        self.SECONDS = 2

        desired_stats_to_code = {
            "trade_flow_casein": self.get_hs_codes("3501", "3501"),
            "trade_flow_dairy": self.get_hs_codes("0401", "0406"),
            "trade_flow_meat": self.get_hs_codes("0201", "0206")
        }

        # If desired_stats is not supplied, change it to the keys of the dictionary above
        if desired_stats is None:
            desired_stats = desired_stats_to_code.keys()
        else:
            # Check whether the user input is valid (if desired_stats is not a subset of dictionary)
            if not set(x.lower() for x in desired_stats).issubset(desired_stats_to_code.keys()):
                return self.logger.error("Invalid desired_stats")

        # Go to ExpressQuery
        self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_lbExpressQuery").click()
        time.sleep(self.SECONDS)

        # The dictionary's values are lists of strings (called 'codes'). So the the outer list comprehension loops
        # through the dictionary's items, and the nested list comprehension loops through the list of codes.
        #
        #                           (str)      (list) (str)         (str)       (list)     (str)   (str)
        #                           title       codes  code         title        codes      code    code
        #                             |             |  |              |           |          |       |
        #                             |             |  |              |           |          |       |
        # Example dictionary: {"trade_flow_casein": ["3501"], "trade_flow_dairy": ["0401", "0402", "0403"]}
        #
        # 1. Reload page, 2. type code into Commodity Search, 3. click Go, 4. select Products, 5. select Countries,
        # 6. click Retrieve Data, 7. click Create CSV File, 8. format csv file, 9. clear code from Commodity Search.

        for title, codes in desired_stats_to_code.items():
            if title in desired_stats:
                for code in codes:
                    self.reload_page(year_range, product_type)
                    self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtProductSearch").send_keys(code)
                    self.driver.execute_script("arguments[0].click();", self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_btnProductSearch"))
                    time.sleep(5)

                    # Select codes from Products box if code is in desired_stats_to_code[something]
                    [ActionChains(self.driver).key_down(Keys.CONTROL).click(option).key_up(Keys.CONTROL).perform()
                     for option in self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_lb_Products").
                         find_elements_by_tag_name("option") if code in option.text]

                    # Select countries from Partners
                    [ActionChains(self.driver).key_down(Keys.CONTROL).click(country).key_up(Keys.CONTROL).perform() for
                    country in self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_lb_Partners").
                         find_elements_by_tag_name("option") if len(country.get_attribute("value")) == 2
                     and "!" not in country.text]

                    # Click Retrieve Data & wait for page to load
                    self.driver.execute_script("arguments[0].click();", self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_btnRetrieveData"))
                    time.sleep(10)

                    try:
                        # Click Create CSV File & wait for download
                        self.driver.execute_script("arguments[0].click();", self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_UltraWebTab1__ctl1_grdExpressQuery_btn_ExportToExcel"))
                        time.sleep(20)

                        # Fix the formatting of the csv file. Example: keys = "trade_flow_casein"
                        self.format_csv_file(title, code, product_type, year_range)
                    except:
                        self.logger.error("Could not download CSV file")
                        pass
        self.logger.info("Finished")

    def get_hs_codes(self, a, b):
        """Returns a list of HS codes."""
        return ["{}{}".format(a[0], i) for i in range(int(a[1:]), int(b[1:]) + 1)]

    def reload_page(self, year_range, product_type):
        """Reload page and select all of the options."""
        self.driver.refresh()

        # Select Imports - General from Product Type
        Select(self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_ddlProductType")).select_by_value(self.product_types[product_type])
        time.sleep(4)

        # Selecting options. 1. Commodity Search: Code, 2. Statistics: Value: Dollars,
        # 3. Statistics: Quantity: FAS Non Converted, 4. Dates: Series: Monthly
        Select(self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_ddlProductSearch")).select_by_value("Code")
        Select(self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_ddlValueUnit")).select_by_visible_text("Dollars")
        Select(self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_ddlQuantityType")).select_by_visible_text("Quantity")
        Select(self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_ddlDateSeries")).select_by_value("Monthly")

        # If a year range has been supplied, select it from Dates
        if year_range is not None:
            Select(self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_ddlStartYear")).select_by_value(
                str(year_range[0]))
            Select(self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_ddlEndYear")).select_by_value(
                str(year_range[1]))

    def format_csv_file(self, title, code, product_type, year_range):
        """Reads downloaded CSV file, removes it, and creates a new CSV file with a clean format."""
        self.logger.info("Writing to new CSV file")
        # Find newest file (the one that just got downloaded)
        files = glob.glob(self.CSV_FOLDER_PATH + "/*")
        new_file_path = max(files, key=os.path.getctime)

        # Open file and store its contents in variable reader and then remove file
        with open(new_file_path, "r") as f:
            reader = list(csv.reader(f))[3:]
        os.remove(new_file_path)

        # Create a new file path
        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        new_file_path = self.CSV_FOLDER_PATH + "/" + title + "_" + product_type.lower() + "_" + code +\
                        "_{}-{}_".format(year_range[0], year_range[1]) + current_datetime + ".csv"

        # Create new file with the above path
        with open(new_file_path, "w+", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerow(reader[0][1:] + ["", "", ""])
            for row in reader[1:]:
                # row is a list, so row[0] is the first string in the list
                if "Notes" in row[0]:
                    break
                writer.writerow(row[1:])


if __name__ == "__main__":
    Gats().scrape()
