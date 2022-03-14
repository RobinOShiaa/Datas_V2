from scraper_classes.chrome_scraper import ChromeScraper
from scrapers.logger import get_logger
import pandas as pd
import time
import csv
import os


class AnnualCullSowSlaughteringsHistorical(ChromeScraper):

    logger = get_logger("AnnualCullSowSlaughteringsHistorical")

    def scrape(self):
        self.logger.info("Starting")
        self.url = "http://pork.ahdb.org.uk/prices-stats/production/gb-slaughterings/annual-cull-sow/"

        tmp_path = self.CSV_FOLDER_PATH + "/gbcullsowslaughterings_000.xls"

        self.driver.get(self.url)

        # Click download button
        self.logger.info("Downloading excel file")
        self.driver.find_element_by_xpath("//*[@id='innerRight']/article/p[3]/a").click()
        time.sleep(self.SECONDS)

        # Excel to csv
        self.logger.info("Reading excel file")
        df = pd.read_excel(tmp_path)
        df.to_csv(self.CSV_FOLDER_PATH + "/annual_cull_sow_slaughterings_historical.csv",
                  index=False, encoding="utf-8")

        # Remove Excel file since now we have a csv
        self.logger.info("Removing excel file")
        os.remove(tmp_path)

        # Update tmp_path
        tmp_path = self.CSV_FOLDER_PATH + "/annual_cull_sow_slaughterings_historical.csv"

        # Creating list with data from csv file
        with open(tmp_path, "r") as f:
            reader = csv.reader(f)
            csv_list = list(reader)

            # Fix formatting issues caused by pandas
            self.logger.info("Creating new csv file")
            with open(tmp_path, "w+", newline="", encoding="utf-8") as f:
                self.logger.info("Writing to csv file")
                writer = csv.writer(f, quoting=csv.QUOTE_ALL)
                writer.writerow(["Year", "Footnotes", "Annual GB Sow and Boar Slaughterings ('000 head)"])

                # Get the index of first row with real data
                start_row = [i for i in range(0, len(csv_list)) if "1974" == csv_list[i][0].strip()][0]
                for row in csv_list[start_row:]:
                    writer.writerow(row[:-1])
        self.logger.info("Finished")


if __name__ == "__main__":
    AnnualCullSowSlaughteringsHistorical().scrape()
