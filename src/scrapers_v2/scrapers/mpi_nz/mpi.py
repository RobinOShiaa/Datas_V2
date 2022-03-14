from scraper_classes.firefox_scraper import FirefoxScraper
from scrapers import logger
import xlrd
import csv
import os
class Mpi(FirefoxScraper):
    mpi_logger = logger.get_logger("mpi_logger")

    def __init__(self, url='https://www.mpi.govt.nz/news-and-resources/economic-intelligence-unit/data/#sts=Livestock%20slaughter%20statistics',
                 CSV_FOLDER_PATH=None):
        super().__init__(url, CSV_FOLDER_PATH)

    def scrape(self):
        all_files = set(os.listdir(self.CSV_FOLDER_PATH))
        self.mpi_logger.info("start scrapping")
        self.driver.get(self.url)

        "#locate download link"
        link = self.driver.find_element_by_xpath('//*[@id="main-content"]/ul[1]/li[1]/a')
        print(link)
        link = self.driver.find_element_by_xpath('//*[@id="main-content"]/ul[1]/li[1]/a').get_attribute('href')
        print(link)
        bb = Mpi(link)

        "#download responds unexpected so multiple get's seem to be required"
        #bb.driver.get(link)
        bb.driver.get(link).get()
        bb.driver.implicitly_wait(10)
        bb.driver.close()
        all_files_new = set(os.listdir(self.CSV_FOLDER_PATH))

        "#create folder path"
        new_file_path = self.CSV_FOLDER_PATH + "/" + list(all_files_new - all_files)[0]

        self.converting(new_file_path)

    def converting(self,new_file_path):
        try:
            self.mpi_logger.info("start writing xl > csv")
            wb = xlrd.open_workbook(new_file_path)
            os.remove(new_file_path)
            sh = wb.sheet_by_index(0)

            your_csv_file = open('mpi.csv', 'w', newline='')
            wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

            "#make sure data is not filled with empty rows"
            for rownum in range(sh.nrows):
                if all('' == s or s.isspace() for s in sh.row_values(rownum)):
                    pass
                else:
                    set(sh.row_values(rownum))
                    new_list = list(set(sh.row_values(rownum)))
                wr.writerow(new_list[1:])

        except Exception as e:
            self.mpi_logger.error("Error:did not run through xl > csv function", str(e))

        self.mpi_logger.info("finished xl > csv")
        your_csv_file.close()


#Mpi().converting()
Mpi().scrape()
#needs to be fixed after dan does base class