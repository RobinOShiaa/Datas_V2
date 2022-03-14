from scraper_classes.chrome_scraper import ChromeScraper
import time
import csv
from selenium.common.exceptions import NoSuchElementException


class Clal_Dairy_Acid_Casein(ChromeScraper):

    def __init__(self, url = ('https://www.clal.it/en/index.php?section=caseine#acida'), CSV_FOLDER_PATH=None):
        super().__init__(url, CSV_FOLDER_PATH)
        self.driver.get(url)
        self.Data = []
        self.d = {}

    def scrape(self):
        titles1 = [i.text for i in self.driver.find_elements_by_xpath(
            '//*[@id="pagina"]/table/tbody/tr[5]/td/a/table[1]/tbody/tr/td/table/tbody/tr/td/table[1]/tbody/tr[1]/td[2]/table/tbody/tr[3]/td')]
        print(titles1)

        titles2 = [i.text for i in self.driver.find_elements_by_xpath(
            '//*[@id="pagina"]/table/tbody/tr[5]/td/a/table[1]/tbody/tr/td/table/tbody/tr/td/table[1]/tbody/tr[1]/td[2]/table/tbody/tr[2]/td')]
        print(titles2)
        i = 2
        while i < len(self.driver.find_elements_by_xpath(
                '//*[@id="pagina"]/table/tbody/tr[9]/td/a/table[1]/tbody/tr/td/table/tbody/tr/td/table[1]/tbody/tr/td')):
            try:
                data = self.driver.find_element_by_xpath(
                    '//*[@id="pagina"]/table/tbody/tr[9]/td/a/table[1]/tbody/tr/td/table/tbody/tr/td/table[1]/tbody/tr[{}]/td[1]'.format(
                        i)).text

                data_data = [j.text for j in self.driver.find_elements_by_xpath(
                    '//*[@id="pagina"]/table/tbody/tr[9]/td/a/table[1]/tbody/tr/td/table/tbody/tr/td/table[1]/tbody/tr[{}]/td[2]/table/tbody/tr/td'.format(
                        i))]

                self.d[data] = data_data

                i += 1



            except NoSuchElementException as e:
                print('error')
                break

        self.to_csv(titles1, titles2)


    def to_csv(self, titles1, titles2):
        with open(self.CSV_FILE_PATH, "w+", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerow(['Survey Date'] + [titles2[0] + " " + titles1[0], titles2[1] + " " + titles1[1], titles1[2],
                                               titles2[-1] + " " + titles1[0], titles1[-1]])

            # +titles1[1:3] + [titles2[2]] + titles1[3:5])
            for j in self.d.keys():
                writer.writerow([j] + self.d[j])


if __name__ == "__main__":
    Clal_Dairy_Acid_Casein().scrape()
