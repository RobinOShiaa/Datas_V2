from scraper_classes.bs4_scraper import Bs4Scraper
from bs4 import BeautifulSoup
from scrapers import logger
import requests


class Zmb(Bs4Scraper):
    zmb_logger = logger.get_logger("zmb_logger")
    def __init__(self, url = "http://www.milk.de/",
                 CSV_FOLDER_PATH=None):
        super().__init__(url, CSV_FOLDER_PATH)
    def zmb_scraper(self):
        try:
            self.zmb_logger.info("start scraping")
            r = requests.get(self.url)
            soup = BeautifulSoup(r.content, "lxml")

                #select table to work with
            table = soup.find('table')

                #selects exact row to use for searching
            row = table.find_all('tr')[2]
            week = table.find_all('tr')[1].find_all('td')[0]#.text#.split('.')[0]#.lstrip()
            week = week.text.split('.')[0].lstrip()

                #data = to metric tons of milk delivered
            data = row.find_all('td')[1].text

                #title = the name milk deliveries in german
            title = row.find("td", {'class': 'auto-style141'}).text.strip()
            percent = row.find_all("td", {'align': 'right'})

                #first percentage is selected
            first_percent = percent[1].text.strip()

                #second percentage is selected (% pervious year)
            second_percent = percent[2].text.strip()

                #dictionary to output to CSV file
            final = ({title: (week, data, first_percent, second_percent)})

                #return final)
            self.zmb_logger.info("made it through program")
            with open(self.CSV_FOLDER_PATH + '/zmb.csv', 'w') as f:
                for key in final.keys():
                    f.write("%s,%s\n" % (key, final[key]))
            return final
        except Exception as e:
            self.zmb_logger.error("Error:did not run through", str(e))

        self.zmb_logger.info('finished writing to csv')
