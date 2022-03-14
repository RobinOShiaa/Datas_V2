from scraper_classes.chrome_scraper import ChromeScraper
from scrapers import logger
import time


class Imf(ChromeScraper):
    imf_logger = logger.get_logger("aimis_logger")
    def __init__(self, url = 'https://www.imf.org/external/np/fin/ert/GUI/Pages/CountryDataBase.aspx',
                 CSV_FOLDER_PATH=None):
        super().__init__(url, CSV_FOLDER_PATH)

    def scrape(self):
        self.imf_logger.info("start scraping")
        try:
            #self.chrome_options = webdriver.ChromeOptions
            #self.chrome_options.add_experimental_option("prefs", {'safebrowsing.enabled': 'false'}

            "#traverse page for newest data"
            self.driver.get(self.url)

            self.driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_RadioDateRangePeriod"]').click()

            self.driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_SelectPeriod"]/option[5]').click()

            self.driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_BtnContinue"]').click()
            time.sleep(3)
            self.driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_BtnSelect"]').click()
            time.sleep(3)
            self.driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_BtnContinue"]').click()
            self.driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_rdoDispFormatNA"]').click()
            self.driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_btnPrepareReport"]').click()
            time.sleep(3)
            self.driver.find_element_by_xpath('//*[@id="content1"]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/div/table/tbody/tr[2]/td/table/tbody/tr/td[2]/small/a[1]').click()
            time.sleep(5)

        except Exception as e:
            self.imf_logger.error("Error:did not run through xl > csv function", str(e))

        self.imf_logger.info("finished xl > csv")
if __name__ == "__main__":
    Imf().scrape()
