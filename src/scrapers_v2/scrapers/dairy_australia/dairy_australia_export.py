from scraper_classes.bs4_scraper import Bs4Scraper
from scrapers import logger
import requests
import xlrd
import csv

class DairyAustraliaExport(Bs4Scraper):
    aus_logger = logger.get_logger('aus_logger')
    def __init__(self, url='https://www.dairyaustralia.com.au/-/media/dairyaustralia/documents/industry/industry-resources/latest-trade-exports/dairy-export-report-april-2019.xls?la=en&hash=6C57CA8D85C76D5214029A54B1292551D53EE370',
                 CSV_FOLDER_PATH=None):
        super().__init__(url, CSV_FOLDER_PATH)

    def scrape(self):
        self.aus_logger.info('Start scraping')
        try:
            "#get url which is a download link"
            r = requests.get(self.url)
            tmp_path = self.CSV_FOLDER_PATH + '/dairy_australia_export.xls'
            output = open(tmp_path, 'wb')
            output.write(r.content)
            output.close()

            "#open saved xls and convert to csv"
            wb = xlrd.open_workbook(tmp_path)
            sh = wb.sheet_by_index(0)
            your_csv_file = open(self.CSV_FOLDER_PATH + '/dairy_australia_export.csv', 'w', newline='')
            wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

            for rownum in range(sh.nrows):
                    set(sh.row_values(rownum))
                    new_list = list(set(sh.row_values(rownum)))
                    wr.writerow(new_list[1:])
            your_csv_file.close()
            
        except Exception as e:
            self.aus_logger.error("Error:did not run through xl > csv function", str(e))

        self.aus_logger.info("finished xl > csv")
if __name__ == "__main__":
    DairyAustraliaExport().scrape()
