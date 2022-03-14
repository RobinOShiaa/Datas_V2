
from datetime import datetime
import time
from scraper_classes.chrome_scraper import ChromeScraper
from selenium.common.exceptions import ElementNotVisibleException


class comtrade(ChromeScraper):


    def __init__(self, url= 'https://comtrade.un.org/data', CSV_FOLDER_PATH=None):
     super().__init__(url , CSV_FOLDER_PATH)
     self.driver.get(url)
     print('Start scraping at %s...' % datetime.now())


    def scrape(self):
        time.sleep(2)
        self.services() #get csv for data filtered by services

        self.goods()  #get csv for data filtered by goods
        self.goods(True)
        print('Finished scraping at %s.' % datetime.now())

    def services(self):
        self.driver.find_element_by_xpath('//*[@id="type-s"]').click()
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="eb02"]').click()
        time.sleep(2)
        Download = self.driver.find_element_by_xpath('//*[@id="download-csv-top"]/span')
        Download.click()


    def goods(self,checked = False):
        self.driver.find_element_by_xpath('//*[@id="type-c"]').click()
        time.sleep(2)
        if checked:
            self.driver.find_element_by_xpath('//*[@id="freq-m"]').click()
        else:
            self.driver.find_element_by_xpath('//*[@id="freq-a"]').click()
        try:

            time.sleep(2)

            HS = self.driver.find_elements_by_xpath('//*[@id="ct-classifications-row"]/div[1]/fieldset/label')
            SITC = self.driver.find_elements_by_xpath('//*[@id="ct-classifications-row"]/div[2]/fieldset/label')
            BEC = self.driver.find_elements_by_xpath('//*[@id="bec"]')
            options =HS+SITC+BEC
            for i in options:
                time.sleep(3)
                i.click()
                time.sleep(10)
                print(i.text)
                Download = self.driver.find_element_by_xpath('//*[@id="download-csv-top"]/span')
                Download.click()

        except ElementNotVisibleException as e:
            Download = self.driver.find_element_by_xpath('//*[@id="download-csv-top"]/span')
            Download.click()




if __name__ == "__main__":
    comtrade().scrape()











