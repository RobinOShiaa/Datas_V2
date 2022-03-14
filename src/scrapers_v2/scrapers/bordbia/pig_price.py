from scraper_classes.bs4_scraper import Bs4Scraper
from bs4 import BeautifulSoup
from scrapers import logger
import requests
import csv


class BordBiaPigPrice(Bs4Scraper):
    bord_logger = logger.get_logger("bord_logger")

    def __init__(self, url='https://www.bordbia.ie/farmers-growers/farmers/prices-markets/eu-pig-prices/', CSV_FOLDER_PATH=None):
        super().__init__(url, CSV_FOLDER_PATH)

    def scrape(self):
        self.bord_logger.info("start scraping")
        r = requests.get(self.url)
        soup = BeautifulSoup(r.content, "lxml")

        "#Find tables by tbody and tr/th"
        table = soup.find('tbody')
        thead = soup.find('tr', {'class': 'title'})
        e = thead.find_all('th')
        temp_pig_data = []
        for b in e:
            temp_pig_data.append(b.text)

        '#d dict of data'
        d = {}

        '# list of titles for data'
        l = []

        "#add missing variables"
        pig_price_data = ['Country'] + temp_pig_data[1:6] + ['Change']
        for body in table:
            for contents in body:
                if contents != "\n":
                    try:
                        l.append(contents.text)
                    except AttributeError:
                        # none type
                        pass
            if not l:
                pass
            else:
                d[l[0]] = l[1:]
                l = []

        try:
            "#write tables to csv"
            with open(self.CSV_FOLDER_PATH + '/bordbia_pig_price.csv', 'w', newline='') as f:
                writer = csv.writer(f, delimiter=",", quoting=csv.QUOTE_ALL)
                writer.writerow(pig_price_data)
                for key in d:
                    writer.writerow([key] + d[key])
                    
        except Exception as e:
            self.bord_logger.error("Error:did not run through list > csv function", str(e))
        self.bord_logger.info("finished writing to csv")


if __name__ == "__main__":
    BordBiaPigPrice().scrape()
