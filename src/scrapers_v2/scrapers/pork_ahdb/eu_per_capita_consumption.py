from scraper_classes.bs4_scraper import Bs4Scraper
from scrapers.logger import get_logger
from bs4 import BeautifulSoup
import requests
import csv


class EuPerCapitaConsumption(Bs4Scraper):

    logger = get_logger("EuPerCapitaConsumption")

    def scrape(self):
        self.logger.info("Starting")
        self.url = "https://pork.ahdb.org.uk/prices-stats/consumption/eu-per-capita-consumption/"
        result = requests.get(self.url)
        soup = BeautifulSoup(result.content, "lxml")

        table = soup.tbody
        columns = [tag.text.strip() for tag in table.find_all("tr")[2].find_all("td") if tag.text.strip() is not ""]
        rows = [tag.td.text.strip() for tag in table.find_all("tr")[1:] if tag.td.text.strip() is not ""]

        self.logger.info("Creating new csv file")
        with open(self.CSV_FOLDER_PATH + "/eu_per_capita_consumption.csv", "w+", newline="", encoding="utf-8") as f:
            self.logger.info("Writing to csv file")
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerow(["Country (kg per head)"] + columns)
            for country in table.find_all("tr")[5:-1]:
                country_name = country.td.text.strip()
                if country_name in rows:
                    writer.writerow([country_name] + [tag.text.strip() for tag in country.find_all("td")[1:]])
        self.logger.info("Finished")


if __name__ == "__main__":
    EuPerCapitaConsumption().scrape()
