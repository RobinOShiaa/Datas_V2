

import csv
from scraper_classes.chrome_scraper import ChromeScraper

class Clal_Milk_prices3_fmg(ChromeScraper):

    def __init__(self, url = ('https://www.clal.it/en/index.php?section=latte_new_zealand'), CSV_FOLDER_PATH=None):
        super().__init__(url, CSV_FOLDER_PATH)
        self.driver.get(url)
        self.Data = []
        self.d = {}

    def scrape(self):
        i = 3
        Years = [i.text for i in self.driver.find_elements_by_xpath('//*[@id="pagina"]/table/tbody/tr/td/table[4]/tbody/tr[2]/td/div/table[1]/tbody/tr[2]/td')]
        self.Data.append(Years)


        while i < len(self.driver.find_elements_by_xpath('//*[@id="pagina"]/table/tbody/tr/td/table[4]/tbody/tr[2]/td/div/table[1]/tbody/tr/td')):
            el = [j.text for j in self.driver.find_elements_by_xpath('//*[@id="pagina"]/table/tbody/tr/td/table[4]/tbody/tr[2]/td/div/table[1]/tbody/tr[{}]/td'.format(i))]
            self.Data.append(el)
            if el == []:
                break
            print(el)
            i+=1


        self.to_csv()


    def to_csv(self):
        with open(self.CSV_FILE_PATH, "w+", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerow(['Month'] + self.Data[0])
            for j in self.Data[2:-3]:

                writer.writerow(j)


if __name__ == "__main__":
    Clal_Milk_prices3_fmg().scrape()
