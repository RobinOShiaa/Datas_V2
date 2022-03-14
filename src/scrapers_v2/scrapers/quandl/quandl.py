from scraper_classes.bs4_scraper import Bs4Scraper
from bs4 import BeautifulSoup
import requests
import time
from scrapers import logger
class Quandl(Bs4Scraper):

    def __init__(self):
        self.urls = ['https://www.quandl.com/api/v1/datasets/GDT/REN_SU.csv',
                'https://www.quandl.com/api/v1/datasets/ODA/PSUNO_USD.csv',  # sunflower oil
                'https://www.quandl.com/api/v1/datasets/ODA/PROIL_USD.csv',  # rapeseed oil
                'https://www.quandl.com/api/v3/datasets/ODA/PPOIL_USD.csv',  # palm oil
                'https://www.quandl.com/api/v3/datasets/ODA/PSOIL_USD.csv'  # soybean oil
                ]

    quandl_logger = logger.get_logger("bord_logger")
    def quandl_scraper(self):
        self.quandl_logger.info("start scraping")
        try:
            d = {}

            "#go through each link and add it to dict d"
            for url in self.urls:
                s = requests.get(url)
                time.sleep(5)
                soup = BeautifulSoup(s.text, "lxml")

                temp = soup.text.replace("\n", "")
                t = Bs4Scraper(url)
                dd = {t, temp}
                d[t] = temp
                print(dd)
                with open(self.CSV_FOLDER_PATH + '/quandl.csv', 'w') as f:
                    for key in d.keys():
                        f.write("%s,%s\n" % (key, d[key]))
        except Exception as e:
            self.quandl_logger.error("Error:did not run through xl > csv function", str(e))
        self.quandl_logger.info("finished xl > csv")
#Quandl().quandl_scraper()


if __name__ == "__main__":
    Quandl().scrape()
