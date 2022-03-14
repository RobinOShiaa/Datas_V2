
from scraper_classes.chrome_scraper import ChromeScraper
import time
import csv
from datetime import datetime

class live_corn(ChromeScraper):



    def __init__(self, url = 'https://www.cmegroup.com/trading/agricultural/grain-and-oilseed/corn.html', CSV_FOLDER_PATH=None):
     super().__init__(url, CSV_FOLDER_PATH)
     self.driver.get(url)

     self.driver.maximize_window()
     self.temp = []
     self.Data = []
     self.headers = []
     self.row = []
     print('Start scraping at %s...' % datetime.now())



    def scrape(self):
        time.sleep(5)
        if self.driver.find_element_by_id('pardotCookieButton'):
            self.driver.find_element_by_id('pardotCookieButton').click()
        time.sleep(1)
        self.make_table()


    def to_csv(self):

        with open(self.CSV_FOLDER_PATH + '/live_corn.csv', "w+", newline="") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)

            writer.writerow(["Month","Options","Last","Change","Prior Settle","Open","High",'Low','Volume','Hi / Low Limit','Updated'])
            for dic in self.Data:
                writer.writerow([dic['Month'], dic['Options'],  dic['Last'], dic['Change'],dic['Prior Settle'], dic['Open'],dic['High'],dic['Low'],dic['Volume'],dic['Hi / Low Limit'],dic['Updated']])



    def make_table(self):
        self.headers = [i.text for i in self.driver.find_elements_by_xpath('//*[@id="quotesFuturesProductTable1"]/thead[2]/tr/th')]
        self.headers.remove('Charts')
        options2 = [i.text for i in self.driver.find_elements_by_xpath('//tbody/tr/td') if i.text is not '']
        stri = ''
        n= 0
        print(options2)
        for i in options2:
            stri = stri + i + "*"
            self.row = stri.split('*')

            if len(self.row) == len(self.headers) + 1:
                self.temp.append(self.row)
                print(self.row)
                self.row = []
                stri = ''



        for i in self.temp:
            self.Data.append(dict(zip(self.headers,i)))

        print(self.Data)
        print('Finished scraping at %s.' % datetime.now())
        self.to_csv()




if __name__ == "__main__":
    live_corn().scrape()
