from scraper_classes.bs4_scraper import Bs4Scraper
from bs4 import BeautifulSoup
from scrapers import logger
import requests
import csv


class BordBiaDairyPrice(Bs4Scraper):
    bord_logger = logger.get_logger("bord_logger")

    def __init__(self, url='https://www.bordbia.ie/farmers-growers/farmers/prices-markets/dairy-summary/',
                 CSV_FOLDER_PATH=None):
        super().__init__(url, CSV_FOLDER_PATH)

    def scrape(self):
        self.bord_logger.info("start scraping")

        try:
            r = requests.get(self.url)
            soup = BeautifulSoup(r.content, "lxml")

            "#locate table by tr and th"
            thead = soup.find('tr', {'class': 'title'})
            title_finder = thead.find_all('th')
            title_list = []

            "#website missing two titles so add on type and change to existing ones"
            for b in title_finder:
                title_list.append(b.text)
            title_list = ['Type'] + title_list[2:8] + ['Change']


            names = soup.find_all('h2')
            country_list = []
            for country in names:
                country_list.append(country.text)

            "#make sure it starts at top of each uneven length table"
            row_strs = [tag.text.strip() for tag in soup.find_all("tr") if "Week Ending" not in tag.text.strip()]

            tables = []
            tmp_row = []

            "#Correct data format depending on the tag it is under"
            for row in row_strs:
                if "Prev.Week" in row:
                    tables.append(tmp_row)
                    tmp_row = []
                elif row == row_strs[-1]:
                    row_ = "".join([c.replace("\n", ",") for c in row]).split(",")
                    tmp_row.append([row_[0]] + row_[2:])
                    tables.append(tmp_row)
                else:
                    row_ = "".join([c.replace("\n", ",") for c in row]).split(",")
                    tmp_row.append([row_[0]] + row_[2:])
            tables = tables[1:]

            i = 0

            "#Begin writing to a csv from the table"
            with open(self.CSV_FOLDER_PATH + '/bordbia_dairy_prices.csv', 'w', newline='') as f:
                writer = csv.writer(f, delimiter=",", quoting=csv.QUOTE_ALL)
                writer.writerow(title_list)
                for table in tables:
                    writer.writerow([country_list[i]])
                    for row in table:
                        writer.writerow(row)
                    i += 1

        except Exception as e:
            self.bord_logger.error("Error:did not run through list > csv function", str(e))
        self.bord_logger.info("finished writing to csv")


if __name__ == "__main__":
    BordBiaDairyPrice().scrape()
