from scraper_classes.chrome_scraper import ChromeScraper
import xlrd
import csv
import time
import os
from scrapers import logger


class Aimis(ChromeScraper):
    aimis_logger = logger.get_logger("aimis_logger")

    def __init__(self, url = 'http://aimis-simia.agr.gc.ca/rp/index-eng.cfm?menupos=1.02.06&LANG=EN&r=53&pdctc=&action=pR',
                 CSV_FOLDER_PATH=None):
        super().__init__(url, CSV_FOLDER_PATH)

    def scrape(self):

        all_files = set(os.listdir(self.CSV_FOLDER_PATH))

        i = 2
        y = 2019
        compi = 24
        compj = 52
        durations_year = {}
        #loop to create dict of years 2019-1998
        while i < compi:
            durations_year[y] = "//*[@id='p_71']/option[{}]".format(i)
            y -= 1
            i += 1

        j = 2
        durations_week = {}
        '#loop to create dict of weeks 2-52, 52 being the start of the year'
        while j <= compj:
            durations_week[j] = "//*[@id='p_72']/option[{}]".format(j)
            j += 1

        year = 2019
        week = 2
        try:
            self.aimis_logger.info("start scraping")
            '#if most recent data is wanted set year to 2019 and week to 2'
            self.driver.get(self.url)
            '#select year box'
            self.driver.find_element_by_xpath('//*[@id="p_71"]').click()
            '#select year'
            self.driver.find_element_by_xpath(durations_year[year]).click()
            '#click next page'
            self.driver.find_element_by_xpath('//*[@id="promptForm"]/div/input[10]').click()
            '#select week box'
            self.driver.find_element_by_xpath(durations_week[week]).click()
            '#select week'
            self.driver.find_element_by_xpath('//*[@id="report_format_type_code"]/option[4]').click()
            '#select format'
            self.driver.find_element_by_xpath('//*[@id="promptForm"]/div/input[11]').click()
            '#click next page'
            self.driver.find_element_by_xpath('//*[@id="wb-main-in"]/p[2]/a[2]').click()
            time.sleep(5)
        except Exception as e:
            self.aimis_logger.error("Error:did not run through", str(e))
        self.aimis_logger.info("finished scraping")

        all_files_new = set(os.listdir(self.CSV_FOLDER_PATH))
        new_file_path = self.CSV_FOLDER_PATH + "/" + list(all_files_new - all_files)[0]

        self.converting(new_file_path)

    def converting(self, new_file_path):
        tmp_path = self.CSV_FOLDER_PATH
        try:
            self.aimis_logger.info("start writing xl > csv")
            wb = xlrd.open_workbook(new_file_path)
            os.remove(new_file_path)
            sh = wb.sheet_by_index(0)
            your_csv_file = open(tmp_path + '/aimis_simia.csv', 'w', newline='')
            wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

            for rownum in range(sh.nrows):
                if all('' == s or s.isspace() for s in sh.row_values(rownum)):
                    pass
                else:

                    set(sh.row_values(rownum))
                    new_list = list(set(sh.row_values(rownum)))
                    wr.writerow(new_list[1:])
                    
        except Exception as e:
            self.aimis_logger.error("Error:did not run through xl > csv function", str(e))

        self.aimis_logger.info("finished xl > csv")
        your_csv_file.close()


if __name__ == "__main__":
    Aimis().scrape()
