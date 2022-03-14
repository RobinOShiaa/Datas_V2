from scraper_classes.chrome_scraper import ChromeScraper
import csv
from scrapers import logger

class DairyAustraliaTrade(ChromeScraper):
    aus_logger = logger.get_logger("bord_logger")
    def __init__(self, url = "https://www.dairyaustralia.com.au/industry/prices/farmgate-milk-price",
                 CSV_FOLDER_PATH=None):
        super().__init__(url, CSV_FOLDER_PATH)

    def scrape(self):
        self.aus_logger.info('Start scraping')
        self.driver.get(self.url)

        try:
            "#find table using xpath"
            x = self.driver.find_element_by_xpath('/html/body/div[2]/div/div[5]/div/section/div/div[1]/div[1]/div/div/div/div[1]/div/div/table')
            y = x.text.strip()
            string = []
            string.append(y)
            td = self.driver.find_elements_by_tag_name('td')
            tist = []

            "#append to tist unless empty row"
            for t in td:
                tmp = t.text
                if tmp == '':
                    pass
                else:
                    tist.append(tmp)

            "#add extra headings"
            headings = ['Factory'] + ['Units'] + tist[0:4] + ['Units'] + tist[0:4]
            tist = tist[4:]
            dict = {}
            i = 0
            j = 0

            "#limit data to avoid useless data"
            while i < 7:
                dict[tist[j]] = tist[j+1: j+6] + tist[j+6:j+11]
                i+= 1
                j+= 11
                
            "#write to csv"
            with open(self.CSV_FOLDER_PATH + '/dairy_australia_trade.csv', 'w', newline='') as f:
                writer = csv.writer(f, delimiter=",", quoting=csv.QUOTE_ALL)
                writer.writerow(headings)
                for key in dict.keys():
                    f.write("%s,%s\n" % (key, dict[key]))

        except Exception as e:
            self.aus_logger.error("Error:did not run through xl > csv function", str(e))

        self.aus_logger.info("finished xl > csv")
if __name__ == "__main__":
    DairyAustraliaTrade().scrape()
