from scraper_classes.bs4_scraper import Bs4Scraper
from bs4 import BeautifulSoup
from scrapers import logger
import requests
import csv


class BordBiaPigThroughput(Bs4Scraper):
    bord_logger = logger.get_logger("bord_logger")

    def __init__(self, url='https://www.bordbia.ie/farmers-growers/farmers/prices-markets/pig-throughput/', CSV_FOLDER_PATH=None):
        super().__init__(url, CSV_FOLDER_PATH)

    def scrape(self):
        self.bord_logger.info("start scraping")
        r = requests.get(self.url)
        soup = BeautifulSoup(r.content, "lxml")

        try:
            "#Search for table using tr and th"
            thead = soup.find('tr', {'class': 'title'})
            title_finder = thead.find_all('th')
            title_list = []
            for b in title_finder:
                title_list.append(b.text)

            "#add in missing titles for csv file"
            title_list = ['Type'] + title_list[1:4] + ['Change']


            names = soup.find_all('h2')
            country_list = []
            for country in names:
                country_list.append(country.text)

            b = soup.find_all('td')
            i = 0
            temp = []
            while i < len(b):
                temp.append(b[i:i+5])
                i += 6
            dumb_counter = 3
            i = 0

            "#start writing to csv"
            with open(self.CSV_FOLDER_PATH + '/bordbia_pig_throughput.csv', 'w', newline='') as f:
                writer = csv.writer(f, delimiter=",", quoting=csv.QUOTE_ALL)
                writer.writerow(title_list)
                for row in temp:
                    if dumb_counter % 3 == 0:
                        writer.writerow([country_list[i]])
                        i += 1

                    writer.writerow([tag.text for tag in row])
                    dumb_counter += 1

        except Exception as e:
            self.bord_logger.error("Error:did not run through list > csv function", str(e))
        self.bord_logger.info("finished writing to csv")


if __name__ == "__main__":
    BordBiaPigThroughput().scrape()
