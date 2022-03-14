from scraper_classes.bs4_scraper import Bs4Scraper
from scrapers import logger
import requests
import csv
import xlrd
import os


class AusTradeImports(Bs4Scraper):
    aus_logger = logger.get_logger("bord_logger")

    def __init__(self, url='https://www.abs.gov.au/ausstats/meisubs.nsf/log?openagent&5368013a.xls&5368.0&Time%20Series%20Spreadsheet&0BCDB106E17AF54DCA258410001230DA&0&Apr%202019&06.06.2019&Latest',
                 CSV_FOLDER_PATH=None):
        super().__init__(url, CSV_FOLDER_PATH)

    def scrape(self):
        self.aus_logger.info('start scraping')
        try:
            "#Get url which is download link"
            r = requests.get(self.url)
            tmp_path = self.CSV_FOLDER_PATH + '/aus_trade_imports.xls'
            output = open(tmp_path, 'wb')

            "#Write xls file to be saved"
            output.write(r.content)
            output.close()

            "#Open xls to begin writing to csv"
            wb = xlrd.open_workbook(tmp_path)
            os.remove(tmp_path)
            sh = wb.sheet_by_index(0)

            "#set directory"
            your_csv_file = open(self.CSV_FOLDER_PATH + '/aus_trade_imports.csv', 'w', newline='')
            wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)
            
            "#Write xls row by row into csv"
            for rownum in range(sh.nrows):
                set(sh.row_values(rownum))
                new_list = list(set(sh.row_values(rownum)))
                wr.writerow(new_list[1:])
            your_csv_file.close()

        except Exception as e:
            self.aus_logger.error("Error:did not run through xl > csv function", str(e))

        self.aus_logger.info("finished xl > csv")


if __name__ == "__main__":
   AusTradeImports().scrape()
