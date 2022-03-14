
from datetime import datetime
from scraper_classes.chrome_scraper import ChromeScraper

import csv


class Morrisons(ChromeScraper):

    def __init__(self, url = 'https://groceries.morrisons.com/browse', CSV_FOLDER_PATH=None):
        super().__init__(url, CSV_FOLDER_PATH)
        self.Data = []
        self.memo = []

        self.product = []
        self.urls = []
        self.driver.get(url)
        self.main_nav = [i.get_attribute('href') for i in self.driver.find_elements_by_xpath('//*[@id="main-content"]/div/div[1]/div[1]/div/div[1]/div[2]/ul/li/a')]
        print('Start scraping at %s...' % datetime.now())


    def scrape(self):
        lisst = []
        for i in self.main_nav:
            self.driver.get(i)
            lisst += [j.get_attribute('href') for j in self.driver.find_elements_by_xpath(
                '//*[@id="main-content"]/div/div[1]/div[1]/div/div[1]/div/ul/li[@class="level-item has-children"]/a')]
        print(lisst)
        self.get_children(0, lisst)
        print(self.urls)
        self.to_csv()


    def to_csv(self):

        with open(self.CSV_FOLDER_PATH + '/morrisons.csv', "w+", newline="") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            for dic in self.Data:
                writer.writerow(["product", "price"])
                for key in dic.keys():
                    writer.writerow((key, dic[key]))

    def get_children(self,i,list):

        while i<len(list):
            self.driver.get(list[i])

            direct_link = [j.get_attribute('href') for j in self.driver.find_elements_by_xpath('//*[@id="main-content"]/div/div[1]/div[1]/div/div[1]/div/ul/li[@class="level-item leaf"]/a') if j.get_attribute('href') not in self.urls]
            if direct_link != []:
                self.parse_products(direct_link
                                    )
                self.urls += direct_link


            subnav = [j.get_attribute('href') for j in self.driver.find_elements_by_xpath('//*[@id="main-content"]/div/div[1]/div[1]/div/div[1]/div/ul/li[@class="level-item has-children"]/a')if j.get_attribute('href') not in list  ]
            if subnav != []:
                list += subnav
            print(len(list))
            i += 1
            print(subnav)
        return list



    def parse_products(self,links):
            for i in links:
                self.driver.get(i)

                products = [k.text for k in self.driver.find_elements_by_xpath('//*[@id="main-content"]/div/div[2]/ul/li/div[2]/div[1]/a/div[1]/div[2]/h4/span[1]')]
                price = [l.text for l in self.driver.find_elements_by_xpath('//*[@id="main-content"]/div/div[2]/ul/li/div[2]/div[1]/a/div[2]/span[1]')]
                dictionary = dict(zip(products, price))
                self.Data.append(dictionary)
                print(dictionary)

if __name__ == "__main__":
    Morrisons().scrape()
