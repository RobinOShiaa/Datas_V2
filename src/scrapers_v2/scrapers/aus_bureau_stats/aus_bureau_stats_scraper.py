from scraper_classes.bs4_scraper import Bs4Scraper
from scrapers import logger
import requests
import csv
import xlrd
import os


class AusLivestockSlaughters(Bs4Scraper):
    aus_logger = logger.get_logger("bord_logger")

    def __init__(self, url='https://www.abs.gov.au/AUSSTATS/ABS@Archive.nsf/log?openagent&7218001.xls&7218.0.55.001&Time'
                           '%20Series%20Spreadsheet&0D392DF078874158CA25840F00189E50&0&Apr%202019&05.06.2019&Latest',
                 CSV_FOLDER_PATH=None):
        super().__init__(url, CSV_FOLDER_PATH)


    def scrape(self):
        self.aus_logger.info('start scraper')
        try:
            "#Get url which is download link"
            r = requests.get(self.url)
            tmp_path = self.CSV_FOLDER_PATH + '/aus_livestock_slaughters.xls'
            output = open(tmp_path, 'wb')
            output.write(r.content)
            output.close()

            "#save xls to directory"
            wb = xlrd.open_workbook(tmp_path)
            sh = wb.sheet_by_index(0)
            your_csv_file = open(self.CSV_FOLDER_PATH + '/aus_livestock_slaughters.csv', 'w', newline='')
            wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

            "#Write xls to csv row by row"
            for rownum in range(sh.nrows):
                set(sh.row_values(rownum))
                new_list = list(set(sh.row_values(rownum)))
                wr.writerow(new_list[1:])
            your_csv_file.close()
            os.remove(tmp_path)

        except Exception as e:
            self.aus_logger.error("Error:did not run through xl > csv function", str(e))

        self.aus_logger.info("finished xl > csv")


if __name__ == "__main__":
    AusLivestockSlaughters().scrape()
