from scraper_classes.chrome_scraper import ChromeScraper
from scrapers.logger import get_logger
import time
import csv
import os


class WeeklyCleanPigSlaughteringsHistorical(ChromeScraper):

    logger = get_logger("WeeklyCleanPigSlaughteringsHistorical")

    def scrape(self, duration=5):
        self.logger.info("Starting")
        self.url = "https://pork.ahdb.org.uk/prices-stats/production/gb-slaughterings/weekly-clean-pig/"

        tmp_path = self.CSV_FOLDER_PATH + "/Export.xls"

        # Select duration from dropdown menu
        durations = {
            0.5: "//*[@id='duration']/option[1]",
            1: "//*[@id='duration']/option[2]",
            3: "//*[@id='duration']/option[3]",
            5: "//*[@id='duration']/option[4]"
        }

        if duration not in durations:
            self.logger.error("Invalid Duration")
            return self.logger.info("Valid durations: 0.5, 1, 3, 5 (years).")

        self.driver.get(self.url)

        # Select duration and click download button
        self.logger.info("Downloading excel file")
        self.driver.find_element_by_xpath(durations[duration]).click()
        self.driver.find_element_by_xpath("//*[@id='innerRight']/article/p[2]/a").click()
        time.sleep(self.SECONDS)

        # Renaming this particular file from Excel to csv fixes its problem of being detected as 'corrupt'
        os.rename(tmp_path, self.CSV_FOLDER_PATH + "/tmp.csv")

        # Update tmp_path
        tmp_path = self.CSV_FOLDER_PATH + "/{}_weekly_clean_pig_slaughterings_historical.csv".format(duration)

        # Creating list with data from csv file
        self.logger.info("Reading excel file")
        with open(self.CSV_FOLDER_PATH + "/tmp.csv", "r") as f:
            reader = csv.reader(f)
            csv_list = list(reader)

        self.logger.info("Removing excel file")
        os.remove(self.CSV_FOLDER_PATH + "/tmp.csv")

        # Creating csv file and writing to it
        self.logger.info("Creating new csv file")
        with open(tmp_path, "w+", newline="") as f:
            self.logger.info("Writing to csv file")
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            for row in csv_list:
                date = row[0].split("\t")[0]
                quantity = row[0].split("\t")[1]
                writer.writerow([date, quantity])
        self.logger.info("Finished")


if __name__ == "__main__":
    WeeklyCleanPigSlaughteringsHistorical().scrape()
