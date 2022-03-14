
import time

from datetime import datetime
from scraper_classes.chrome_scraper import ChromeScraper
from selenium.common.exceptions import NoSuchElementException
import csv


class Sainsburys(ChromeScraper):

    def __init__(self,url = 'https://www.sainsburys.co.uk/webapp/wcs/stores/servlet/gb/groceries?langId=44&storeId=10151&krypto=VBmpDQc90g6rN55EpRIURJNtFxtQWhj2k1UCYZXXrATkx0gmA3du01Ac6uuewU4eHdW3qe6D8qRyE1SavMX1q3s7URrLjZCBGBEWr1tZuPP9Oa2QYgS0IQt1cDaqODmK&ddkey=https%3Agb%2Fgroceries',CSV_FOLDER_PATH = None):
        super().__init__(url,CSV_FOLDER_PATH)
        self.Data = []
        self.memo = {}
        self.urls = []
        self.driver.get(url)
        self.main_nav = [i.get_attribute('href') for i in self.driver.find_elements_by_xpath('//*[@id="megaNavLevelOne"]/li/a')]
        print('Start scraping at %s...' % datetime.now())


    def scrape(self):
        time.sleep(2)
        self.driver.find_element_by_id('cookieContinue').click()
        for i in self.main_nav:
            self.driver.get(i)
            dropdown = [i.get_attribute('href') for i in
                        self.driver.find_elements_by_xpath('//*[@id="content"]/div[2]//ul[@class]/li/a')]
            self.parse_dropdown(dropdown)

        self.to_csv()



    def parse_dropdown(self, span):

        for i in span:
            self.driver.get(i)
            word = i.split("/")
            word = word[len(word) - 1]
            print(word)
            if word in self.memo:
                return self.urls
            self.memo[word] = i
            dropdown2 = [i.get_attribute('href') for i in self.driver.find_elements_by_xpath('//*[@id="content"]/div[2]//ul[@class]/li/a')]
            mid = (list(set(dropdown2) - set(span)))

            self.urls += mid
            if len(mid) == 0:
                self.parse_products('https://www.sainsburys.co.uk/webapp/wcs/stores/servlet/gb/groceries/food-cupboard?langId=44&storeId=10151&krypto=USBR0X48g9DvDjUSu5ucYzgY5tHKdyz2EoP286Mku%2Bfv26Hci8c2%2BZv%2BL4a3OtYGl1l0fYSAeH9Y4hx9hEZRBDrKBxuiLk9rdQcsKZVljCo000LT8roHRfgI%2Bm1KVKiOzgAqYHK%2FY22a3bzHZxPhUfxuQGY0ivXwN5Xxjv5SgSU%3D&ddkey=https%3Agb%2Fgroceries%2Ffood-cupboard')
                self.driver.implicitly_wait(3)
                print('Scraping product data')

            else:
                print(mid)
                return self.parse_dropdown(mid)



    def to_csv(self):
        
        with open(self.CSV_FOLDER_PATH + '/sainburys.csv', "w+", newline = "") as f:
            writer = csv.writer(f,quoting = csv.QUOTE_ALL)
            for dic in self.Data:
                writer.writerow(["product", "price"])
                for key in dic.keys():

                    writer.writerow((key, dic[key]))






    def parse_products(self,link,more_products = True):

        while more_products:
            products = [k.text for k in self.driver.find_elements_by_xpath('//*[@id="productLister"]/ul/li/div/div[1]/div/h3/a')]
            price = [l.text for l in self.driver.find_elements_by_class_name('pricePerUnit')]
            dictionary = dict(zip(products, price))
            self.Data.append(dictionary)
            print(dictionary)


            try:
                self.driver.find_element_by_xpath('//li[@class="next"]/a').click()
                time.sleep(2)
                # browser.click_button('xpath', '//*[@id="productLister"]/div[1]/ul[2]/li[4]/a')

                print('turning page')
                time.sleep(2)

            except NoSuchElementException as e:
                print('no more products')
                self.driver.get(link)
                more_products = False

if __name__ == "__main__":
    Sainsburys().scrape()
