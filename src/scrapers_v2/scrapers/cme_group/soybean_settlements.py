from scraper_classes.chrome_scraper import ChromeScraper
import time
import csv
from selenium.common.exceptions import StaleElementReferenceException
from datetime import datetime
class soy_settlements(ChromeScraper):

    def __init__(self,url = 'https://www.cmegroup.com/trading/agricultural/grain-and-oilseed/soybean-meal_quotes_settlements_futures.html',CSV_FOLDER_PATH = None):
        super().__init__(url,CSV_FOLDER_PATH)
        self.driver.get(url)


        self.driver.maximize_window()
        self.urls = []
        self.Data = []
        self.headers = {}
        self.header = []
        print('Start scraping at %s...' % datetime.now())

    def scrape(self):
        time.sleep(5)
        self.driver.implicitly_wait((2))
        if self.driver.find_element_by_id('pardotCookieButton'):
            self.driver.find_element_by_id('pardotCookieButton').click()
        time.sleep(1)

        self.row_values()
        self.to_csv()

    def row_values(self):
        row = []

        i = 0
        j = 0
        n = 0
        months = [i.text for i in self.driver.find_elements_by_xpath('//*[@id="settlementsFuturesProductTable"]/tbody/tr/th')]
        values = self.driver.find_elements_by_xpath('// *[ @ id = "settlementsFuturesProductTable"] / tbody / tr / td')

        row_length = len(self.driver.find_elements_by_xpath('// *[ @ id = "settlementsFuturesProductTable"] / tbody / tr[1]/td')) +1

        self.get_month(j, row, months)
        while i < len(values):

            if n == row_length:

                self.headers = dict(zip([i.text for i in self.driver.find_elements_by_xpath('//*[@id="settlementsFuturesProductTable"]/thead[2]/tr/th')],row))
                self.Data.append(self.headers)
                j+=1
                n=0
                row = []
                self.get_month(j,row,months)

            try:

                row.append((values[i].text))


            except StaleElementReferenceException as e:
                row.append(self.driver.find_element_by_xpath('// *[ @ id = "settlementsFuturesProductTable"] / tbody / tr / td[5] /span').text)

            i+=1
            n+=1

        print(self.Data)


    def get_month(self,i,row,months):
        row.append(months[i])


    def to_csv(self):

        with open(self.CSV_FOLDER_PATH + '/SoyBean.csv', "w+", newline="") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)

            writer.writerow(["Month", "Open", 'High', "Low", "Last", "Change", "Settle", "Estimated Volume", "Prior Day Open Interest"])
            for dic in self.Data:

                    writer.writerow([dic['Month'],dic['Open'],dic['High'],dic['Low'],dic['Last'],dic['Change'],dic['Settle'],dic['Estimated Volume'],dic['Prior Day Open Interest']])


if __name__ == "__main__":
    soy_settlements().scrape()


