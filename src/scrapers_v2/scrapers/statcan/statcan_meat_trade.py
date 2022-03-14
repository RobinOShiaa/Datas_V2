from scraper_classes.chrome_scraper import ChromeScraper
import time
from scrapers import logger

class StatcanMeat(ChromeScraper):
    statcan_logger = logger.get_logger("statcan_logger")

    def __init__(self,
                 url='https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=3210012501',
                 CSV_FOLDER_PATH=None):
        super().__init__(url, CSV_FOLDER_PATH)

    def scrape(self):
        self.statcan_logger.info('Start scraping')
        self.driver.get(self.url)
        time.sleep(2)

        "#open drop down"
        self.driver.find_element_by_xpath('//*[@id="downloadOverlayLink"]').click()
        time.sleep(2)

        "#selects download option"
        self.driver.find_element_by_xpath('//*[@id="downloadAsDisplay"]/div/div[2]/div[1]').click()
        time.sleep(8)
        self.statcan_logger.info('finished scraping')


#StatcanMeat().scrape()
if __name__ == "__main__":
    StatcanMeat().scrape()
