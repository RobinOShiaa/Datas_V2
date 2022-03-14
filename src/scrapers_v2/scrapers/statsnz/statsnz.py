from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoAlertPresentException
from scraper_classes.chrome_scraper import ChromeScraper
from selenium.webdriver.support.ui import Select
from scrapers.logger import get_logger
from datetime import datetime
import time
import glob
import os


class Statsnz(ChromeScraper):

    logger = get_logger("Statsnz")

    def scrape(self, start_date, end_date, desired_stats="dairy_imports"):
        self.logger.info("Starting")
        self.SECONDS = 2
        self.url = "http://archive.stats.govt.nz/infoshare/TradeVariables.aspx"
        self.driver.get(self.url)
        time.sleep(self.SECONDS)

        if "dairy_imports" in desired_stats.lower():
            self.driver.find_element_by_id("ctl00_MainContent_rbTIM").click()
            hs_codes = self.get_hs_codes("0401", "0410")

        elif "dairy_exports" in desired_stats.lower():
            self.driver.find_element_by_id("ctl00_MainContent_rbTEX").click()
            hs_codes = self.get_hs_codes("0401", "0410")

        elif "casein_trade" in desired_stats.lower():
            self.driver.find_element_by_id("ctl00_MainContent_rbTEX").click()
            hs_codes = self.get_hs_codes("3501", "3507")

        else:
            return self.logger.error("Incorrect input")

        # Click Select all (countries), click Add, click on Search in HS codes
        self.driver.find_element_by_xpath("//*[@id='countryTabs']/div[1]/table/tbody/tr/td[1]/div[1]/a[1]").click()
        self.driver.find_element_by_xpath("//*[@id='ctl00_MainContent_btnAddCountries']").click()
        self.driver.find_element_by_xpath("//*[@id='hsCodeTabs']/ul/li[2]/a").click()
        self.driver.find_element_by_xpath("//*[@id='hsCodeSearchCodeOnly']").click()

        # Paths to Add button & Search bar (used in the list comprehension below)
        self.logger.info("Inputting HS codes")
        btn_add_code = self.driver.find_element_by_xpath("//*[@id='ctl00_MainContent_btnAddSearchCode']")
        input_bar = self.driver.find_element_by_xpath("//*[@id='hsCodeSearchText']")

        # Add all codes into 'Selected HS codes' box
        [(input_bar.send_keys(code),                                                # Type HS code into Search bar
          self.driver.execute_script("OnHSCodeSearch()"),                           # Click on Find
          input_bar.clear(),                                                        # Clear Search bar
          time.sleep(self.SECONDS),                                                 # Wait for the result to load
          self.driver.find_element_by_xpath("//*[@id='hsCodeCheckBox0']").click(),  # Select result by clicking on it
          btn_add_code.click())                                                     # Click Add button
         for code in hs_codes]

        # Click Go button
        self.driver.find_element_by_id("ctl00_MainContent_btnGo").click()

        # Rearrange table format
        self.rearrange_table()

        # Select csv
        Select(self.driver.find_element_by_id("ctl00_MainContent_ctl01").
               find_element_by_id("ctl00_MainContent_dlOutputOptions")).select_by_value("csv")

        # Select years & download csv file(s)
        find_btn = self.driver.find_element_by_xpath("//*[@id='ctl00_MainContent_TimeVariableSelector_lbFind']")
        input_bar = self.driver.find_element_by_xpath("//*[@id='ctl00_MainContent_TimeVariableSelector_tbSearchVariables']")
        years_months = self.get_year_month_range(start_date, end_date)

        # all_data will be a list of lists. Each sublist is an individual csv file's data
        all_data = []
        file_counter = 0

        # This counter keeps track of the number of dates we have selected. Gets reset every 12 iterations
        selected = 0

        # Loop through the dates (e.g.: '1990M01', '1990M02', etc.)
        for date in years_months:
            # (If we reached the last date and we have selected less than 12 dates) OR (we have selected less than 11 dates)
            if (date == years_months[-1] and selected < 12) or selected == 11:
                # Type date into Search bar, click Find, and clear Search bar
                (input_bar.send_keys(date), find_btn.click(), input_bar.clear())

                # Click Go button
                self.driver.find_element_by_xpath("//*[@id='ctl00_MainContent_btnGo']").click()
                try:
                    self.driver.switch_to.alert.accept()
                except NoAlertPresentException:
                    pass

                # Wait for download to finish
                self.logger.info("Downloading csv file")
                time.sleep(8)

                # Clear time periods selection
                self.driver.find_element_by_xpath(
                    "//*[@id='ctl00_MainContent_TimeVariableSelector_lblClearSelection']").click()
                all_data.append(self.csv_to_list(file_counter))
                file_counter += 1
                selected = 0
            else:
                # Type date into Search bar, click Find, and clear Search bar
                (input_bar.send_keys(date), find_btn.click(), input_bar.clear())
                selected += 1
        # Lastly, write to new csv file
        self.logger.info("Writing to new csv file")
        self.list_to_horizontal_csv(all_data, start_date, end_date, desired_stats)
        self.logger.info("Finished")

    def get_hs_codes(self, a, b):
        """Returns a list of HS codes."""
        return ["{}{}".format(a[0], i) for i in range(int(a[1:]), int(b[1:]) + 1)]

    def get_year_month_range(self, year_month_start, year_month_end):
        """Takes two strings in the format: '2019M06', '2019M09', and returns a list of dates in the selected range,
        in the following format: ['2019M06', '2019M07', '2019M08', '2019M09']"""
        date_time = datetime.now()
        # A list of lists. Each sublist is one year (12 months max)
        years_months = [["{}M{}".format(year, str(month).zfill(2)) for month in range(1, 13)] for year in range(1988, date_time.year + 1)]

        # Convert list of lists into a single list
        years_months = [element for sublist in years_months for element in sublist]

        # Using these indexes we specify the output's range of dates
        index_start = years_months.index(year_month_start)
        index_end = years_months.index(year_month_end) + 1
        return years_months[index_start:index_end]

    def rearrange_table(self):
        """Method rearranges the formatting of the table to the following:
        Columns: New Zealand Harmonised System Classification, Observations, Time
        Rows: Trade Country Classification (2 Alpha)."""
        # These are source: destination mappings (used in the list comprehension)
        elements = {self.driver.find_element_by_id("variable_Trade Country Classification (2 Alpha)"):
                    self.driver.find_element_by_id("ctl00_MainContent_ctlDragDropVariableLocation_tdRows"),

                    self.driver.find_element_by_id("variable_Time"):
                    self.driver.find_element_by_id("ctl00_MainContent_ctlDragDropVariableLocation_tdColumns")}
        # Performs the rearrangements of the table
        [ActionChains(self.driver).drag_and_drop(source, destination).perform() for source, destination in elements.items()]

    def csv_to_list(self, file_counter):
        """Opens new csv file, returns its data in a list, and removes the file."""
        # Find path to downloaded file
        files = glob.glob(self.CSV_FOLDER_PATH + "/*")
        new_file_path = max(files, key=os.path.getctime)

        # Read downloaded file and remove it
        with open(new_file_path, "r") as f:
            reader = f.read().splitlines()[1:]
        os.remove(new_file_path)

        # Keep the country column from first file
        if file_counter == 0:
            return reader
        else:
            # Remove country column from other files
            return [country[country[1:].index('"') + 3:] if len(country) > 2 else country for country in reader]

    def list_to_horizontal_csv(self, all_data, start_date, end_date, desired_stats):
        """Takes a list of lists, and converts them to a string where they are horizontally concatenated. The number of
        total rows is equal to the number of countries (+ column name rows), meaning that if there is more than one file,
        their contents will be concatenated to the right side of the first file.

        Example: all_data = [   ['columns', 'country1,data,data', 'country2,data,data'],    # file 1
                                ['columns', 'country1,data,data', 'country2,data,data']     # file 2
                        ]

                                # file 1             # file 2
        resulting_string =      "'columns',          'columns\n',
                                'country1,data,data','data,data\n'
                                'country2,data,data','data,data\n'"
        PS: desired_stats is simply used in the file name creation."""
        new_row = True
        row = 0
        i = 0
        s = ""
        # Loop through all rows
        while row < len(all_data[0]):
            # This string indicates the end of data, so we break out of the loop
            if "Table information" in all_data[i][row]:
                break

            # If we're on a new row, don't add a comma at the start
            if new_row:
                s += all_data[i][row]
                new_row = False
            else:
                s += "," + all_data[i][row]

            # If we have reached the last file reset i, increment row, and add "\n" at the end of the current row
            i += 1
            if i == len(all_data):
                i = 0
                new_row = True
                s += "\n"
                row += 1

        # Since the string is already in its final format, simply write it to a new csv file
        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        new_file_path = self.CSV_FOLDER_PATH + "/{}_{}_{}-{}.csv".format(current_datetime, desired_stats, start_date, end_date)
        with open(new_file_path, "w", encoding="utf-8") as f:
            f.write(s)


if __name__ == "__main__":
    Statsnz().scrape(start_date="2016M01", end_date="2019M05")
