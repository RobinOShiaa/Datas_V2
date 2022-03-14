from scraper_classes.chrome_scraper import ChromeScraper
import time
from scrapers import logger

class StatcanDairy(ChromeScraper):
    statcan_logger = logger.get_logger("statcan_logger")

    def __init__(self,
                 url='https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=3210000101',
                 CSV_FOLDER_PATH=None):
        super().__init__(url, CSV_FOLDER_PATH)

    def scrape(self):
        self.statcan_logger.info('Start Scraping')
        self.driver.get(self.url)
        time.sleep(2)

        '#get to the row selection'
        self.driver.find_element_by_xpath('//*[@id="downloadButton"]/a[2]').click()
        time.sleep(3)
        self.driver.find_element_by_xpath('//*[@id="panel18075-lnk"]').click()
        time.sleep(3)
        self.driver.find_element_by_xpath('//*[@id="select_All2"]').click()
        time.sleep(3)

        '#unselect all rows and select rows which contain useable data'
        self.driver.find_element_by_xpath('//*[@id="3D1_anchor"]/i[1]').click()
        self.driver.find_element_by_xpath('//*[@id="3D3_anchor"]/i[1]').click()
        self.driver.find_element_by_xpath('//*[@id="3D4_anchor"]/i[1]').click()
        self.driver.find_element_by_xpath('//*[@id="3D5_anchor"]/i[1]').click()
        self.driver.find_element_by_xpath('//*[@id="3D6_anchor"]/i[1]').click()

        self.driver.find_element_by_xpath('//*[@id="3D13_anchor"]/i[1]').click()
        self.driver.find_element_by_xpath('//*[@id="3D14_anchor"]/i[1]').click()
        self.driver.find_element_by_xpath('//*[@id="3D15_anchor"]/i[1]').click()
        self.driver.find_element_by_xpath('//*[@id="3D17_anchor"]/i[1]').click()

        '#apply changes'
        time.sleep(3)
        self.driver.find_element_by_xpath('//*[@id="cvApplyButton"]').click()
        time.sleep(5)
        
        '#choose download type and download'
        self.driver.find_element_by_xpath('//*[@id="downloadOverlayLink"]').click()
        self.driver.find_element_by_xpath('//*[@id="downloadAsDisplay"]/div/div[2]/div[2]/p').click()
        time.sleep(5)
        self.statcan_logger.info('finished scraping')

if __name__ == "__main__":
   StatcanDairy().scrape()
