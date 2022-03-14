from scraper_classes.bs4_scraper import Bs4Scraper
from bs4 import BeautifulSoup
from scrapers import logger
import requests
import csv


class BordBiaBeef(Bs4Scraper):

    def __init__(self, url = 'https://www.bordbia.ie/farmers-growers/farmers/prices-markets/cattle-prices/',
                 CSV_FOLDER_PATH=None):
        super().__init__(url, CSV_FOLDER_PATH)

    bord_logger = logger.get_logger("bord_logger")

    def scrape(self):
        self.bord_logger.info("start scraping")
        r = requests.get(self.url)
        soup = BeautifulSoup(r.content, "lxml")

        "#find table to scrape using tbody and tr for rows"
        table = soup.find('tbody')
        thead = soup.find('tr', {'class': 'title'})
        e = thead.find_all('th')
        beef_price_data = []

        "#Go through e and add it to list beef_price_data"
        for b in e:
            beef_price_data.append(b.text)
        d = {}
        l = []

        "#if row in table is \n add it"
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

            "#Write to csv file from tables"
            with open(self.CSV_FOLDER_PATH + '/bordbia_beef_price.csv', 'w', newline='') as f:
                writer = csv.writer(f, delimiter=",", quoting=csv.QUOTE_ALL)
                writer.writerow(beef_price_data)
                for key in d:
                    writer.writerow([key] + d[key])
                    
        except Exception as e:
            self.bord_logger.error("Error:did not run through list > csv function", str(e))
        self.bord_logger.info("finished writing to csv")


if __name__ == "__main__":
    BordBiaBeef().scrape()
