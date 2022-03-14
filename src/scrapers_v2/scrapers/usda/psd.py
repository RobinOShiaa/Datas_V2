from selenium.webdriver.common.action_chains import ActionChains
from scraper_classes.chrome_scraper import ChromeScraper
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from scrapers.logger import get_logger
from datetime import datetime
import pandas as pd
import time
import glob
import os


class Psd(ChromeScraper):

    logger = get_logger("PSD")
    commodity_to_value = {
                            "coffee": "string:cof",
                            "cotton": "string:cot",
                            "dairy": "string:dai",
                            "field crops - production": "string:fcr",
                            "fruits and vegetables": "string:htp",
                            "grains": "string:gra",
                            "juice": "string:juc",
                            "livestock and poultry": "string:liv",
                            "oilseeds": "string:oil",
                            "poultry": "string:pou",
                            "sugar": "string:sug",
                            "tree nuts": "string:nut"
    }

    def scrape(self, desired_stats=None, year_range=None):
        self.logger.info("Starting")
        self.driver.maximize_window()
        self.url = "https://apps.fas.usda.gov/psdonline/app/index.html#/app/advQuery"
        self.driver.get(self.url)
        self.SECONDS = 2

        if year_range is None:
            year_range = self.get_year_range([1960, int(datetime.now().year)+1])
        else:
            year_range = self.get_year_range(year_range)

        if desired_stats is None:
            desired_stats = self.commodity_to_value.keys()
        else:
            # Check whether the user input is valid (if desired_commodities is not a subset of dictionary)
            if not set([x.lower() for x in desired_stats]).issubset(self.commodity_to_value.keys()):
                return self.logger.error("Invalid desired_commodities")

        # Loop through the commodities
        for commodity in desired_stats:
            self.driver.refresh()
            time.sleep(self.SECONDS)

            commodity_value = self.commodity_to_value[commodity]

            # Select commodity from Commodities
            Select(self.driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div[2]/div[2]/div[1]/div[1]/select")).select_by_value(commodity_value)
            time.sleep(self.SECONDS)

            # Select all rows in Commodities
            commodities = self.driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div[2]/div[2]/div[1]/select").find_elements_by_tag_name("option")
            [(ActionChains(self.driver).key_down(Keys.CONTROL).click(tag).key_up(Keys.CONTROL).perform(),
              time.sleep(1)) for tag in commodities]
            time.sleep(self.SECONDS)

            # Select all rows from Attributes
            attributes = self.driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div[2]/div[2]/div[2]/select").find_elements_by_tag_name("option")
            [ActionChains(self.driver).key_down(Keys.CONTROL).click(tag).key_up(Keys.CONTROL).perform() for tag in attributes]

            # Click All Countries from Countries
            self.driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div[2]/div[2]/div[3]/select/optgroup[1]/option[2]").click()

            # Select years from Market Years
            market_years = self.driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div[2]/div[2]/div[4]/select").find_elements_by_tag_name("option")
            [ActionChains(self.driver).key_down(Keys.CONTROL).click(tag).key_up(Keys.CONTROL).perform()
             for tag in market_years if int(tag.text) in year_range]

            # Select Attribute from Column
            Select(self.driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div[2]/div[4]/div[1]/select")).select_by_value("attribute")

            # Select Commodity/Country/Year from Sort Order
            Select(self.driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div[2]/div[4]/div[2]/select")).select_by_value("string:Commodity/Country/Year")

            # Click File Format & click Include Codes
            self.driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div[2]/div[5]/div[1]/input").click()
            self.driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div[2]/div[6]/div[1]/input").click()

            # Click Run Query
            self.driver.execute_script("arguments[0].click();", self.driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div[2]/div[8]/div/button[1]"))
            self.logger.info("Waiting for query to load (50 seconds)")
            time.sleep(50)

            # Click Download
            self.driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div[3]/div[1]/a[2]/i").click()
            time.sleep(self.SECONDS)

            # Convert xls to csv & remove xls file
            new_file_path = self.get_new_file_path()
            xls_data = pd.read_html(new_file_path)
            os.remove(new_file_path)

            # Write data to new csv file
            current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            new_file_path = self.CSV_FOLDER_PATH + "\\psd_" + commodity + "_{}-{}_".format(year_range[0], year_range[-1]) +\
                            current_datetime + ".csv"
            xls_data[0].to_csv(new_file_path, encoding="utf-8", index=None)

            # Go back to URL
            self.driver.get(self.url)
        self.logger.info("Finished")

    def get_year_range(self, year_range):
        """Returns a list of years in the specified range."""
        return list(range(year_range[0], year_range[1]+1))

    def get_new_file_path(self):
        """Return a path to the newest file in directory."""
        # Find newest file (the one that just got downloaded)
        files = glob.glob(self.CSV_FOLDER_PATH + "\\*")
        new_file_path = max(files, key=os.path.getctime)
        return new_file_path


if __name__ == "__main__":
    Psd().scrape()
