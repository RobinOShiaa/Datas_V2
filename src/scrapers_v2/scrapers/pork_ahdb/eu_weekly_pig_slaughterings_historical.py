from scraper_classes.chrome_scraper import ChromeScraper
from scrapers.logger import get_logger
import pandas as pd
import time
import csv
import os


class EuWeeklyPigSlaughteringsHistorical(ChromeScraper):

    logger = get_logger("EuWeeklyPigSlaughteringsHistorical")

    def scrape(self):
        self.logger.info("Starting")
        self.url = "https://pork.ahdb.org.uk/prices-stats/production/eu-weekly-pig-slaughterings/"
        tmp_path = self.CSV_FOLDER_PATH + "/euweeklyslaughter-20190630.xls"

        self.driver.get(self.url)

        # Click download button
        self.logger.info("Downloading excel file")
        self.driver.find_element_by_xpath("//*[@id='innerRight']/article/p[4]/a").click()
        time.sleep(self.SECONDS)

        # Read excel
        self.logger.info("Reading excel file")
        xls = pd.ExcelFile(tmp_path)
        sheets = [xls.parse(0), xls.parse(1)]

        # Remove excel file
        self.logger.info("Removing excel file")
        os.remove(tmp_path)

        sheet_names = ["clean_pigs", "sows"]
        i = 0
        # Loop through each sheet
        for sheet in sheets:
            # Update path
            tmp_path = self.CSV_FOLDER_PATH + "/eu_weekly_pig_slaughterings_historical_{}.csv".format(sheet_names[i])

            self.logger.info("Creating new csv file")
            with open(tmp_path, "w+", newline="", encoding="utf-8") as f:
                self.logger.info("Writing to csv file")
                writer = csv.writer(f, quoting=csv.QUOTE_ALL)

                # Write column names
                writer.writerow([x.replace(x, "-") if "unnamed" in x.lower() else x for x in sheet.columns])

                # Loop through each row of current sheet, and write to file
                for row in sheet.values.tolist():
                    if str(row[0]) not in ["na", "nan"]:
                        # 1. convert incorrect float to int and add commas,
                        # 2. add commas to whole numbers,
                        new_row = [str(x).replace(str(x), "{:,}".format(int(float(x)))) if self.is_decimal(str(x)) and int(float(x)) > 100 else
                                   str(x).replace(str(x), "{:,}".format(int(x))) if str(x).isdigit() and int(x) > 100
                                   else x for x in row]
                        writer.writerow(new_row)
            i += 1
        self.logger.info("Finished")

    def is_decimal(self, n):
        """Checks whether a number is a decimal number or not. Method takes a string."""
        n = n.split(".")
        if len(n) == 2:
            if n[0].isdigit() and n[1].isdigit():
                return True
            elif "-" in n[0] and n[0][1:].isdigit():
                return True
        return False


if __name__ == "__main__":
    EuWeeklyPigSlaughteringsHistorical().scrape()
