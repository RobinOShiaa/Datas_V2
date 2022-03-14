from scraper_classes.chrome_scraper import ChromeScraper
import xlrd
import csv
import time
import os
from scrapers import logger

class EcEuropaPrices(ChromeScraper):
    ec_logger = logger.get_logger("ec europa_logger")
    def __init__(self, url = 'https://ec.europa.eu/agriculture/market-observatory/milk',
                 CSV_FOLDER_PATH=None):
        super().__init__(url, CSV_FOLDER_PATH)

    def scrape(self):
        all_files = set(os.listdir(self.CSV_FOLDER_PATH))
        self.ec_logger.info('Start scraping')
        self.driver.get(self.url)
        self.driver.find_element_by_xpath('//*[@id="content1level"]/div[8]/p[1]/a').click()
        time.sleep(3)
        all_files_new = set(os.listdir(self.CSV_FOLDER_PATH))
        new_file_path = self.CSV_FOLDER_PATH + "/" + list(all_files_new - all_files)[0]
        self.converting(new_file_path)

    def converting(self, new_file_path):

        tmp_path = self.CSV_FOLDER_PATH
        try:
            self.ec_logger.info("start writing xl > csv")
            wb = xlrd.open_workbook(new_file_path)
            os.remove(new_file_path)
            sh = wb.sheet_by_index(1)
            your_csv_file = open(tmp_path + '/ec_europa_dairy_prices.csv', 'w', newline='')
            wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

            for rownum in range(sh.nrows):
                set(sh.row_values(rownum))
                new_list = list(set(sh.row_values(rownum)))
                if new_list == ['']:
                    pass
                else:
                    wr.writerow(new_list)

        except Exception as e:
            self.ec_logger.error("Error:did not run through xl > csv function", str(e))

        self.ec_logger.info("finished xl > csv")
        your_csv_file.close()
