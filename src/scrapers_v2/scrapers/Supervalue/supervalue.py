import time

from datetime import datetime
from scraper_classes.chrome_scraper import ChromeScraper
import csv



class Supervlue(ChromeScraper):

    def __init__(self,url = 'https://shop.supervalu.ie/shopping/?gclid=EAIaIQobChMItP2P_Pvy4gIVSLDtCh08RgTLEAAYASAAEgI2oPD_BwE&gclsrc=aw.ds',CSV_FOLDER_PATH = None):
        super().__init__(url,CSV_FOLDER_PATH)
        self.driver.get(url)
        self.urls = []
        self.Data = []
        self.memo = {}
        print('Start scraping at %s...' % datetime.now())



    def scrape(self):
        self.driver.find_element_by_xpath('//*[@id="msg-container"]/div[2]/div/span').click()
        time.sleep(5)
        self.driver.find_element_by_xpath('//*[@id="menuToggle"]/span').click()
        self.parse_dropdown()
        print(self.urls)
        self.parse_products_cat()
        self.to_csv()

    def parse_dropdown(self):
        dropdown = self.driver.find_elements_by_xpath('//*[@id="megaMenu"]/div/a')
        for i in dropdown:
            if (i.get_attribute('href')):
                print(i.get_attribute('href'))
                self.urls.append(i.get_attribute('href'))
            if (i.get_attribute('data-url')):
                print(i.get_attribute('data-url'))
                self.urls.append(i.get_attribute('data-url'))
        return self.urls


    def parse_products_cat(self):
        print(self.urls)
        for i in self.urls:
            self.driver.get(i.replace("'",''))
            prod = self.driver.find_elements_by_xpath('//div[@class = "product-list-item-details"]/a/h4[@class="product-list-item-details-title"]')
            if prod:

                cat_urls=[i.get_attribute('href') for i in self.driver.find_elements_by_xpath('//a[@class="subcat-name "]')]

                self.parse_products(cat_urls)
            else:
                print('images')
                images = self.driver.find_elements_by_xpath("//div[@onclick]")
                for j in images:
                    url = j.get_attribute('onclick')
                    url = url.split('=')[1]

                    if '{{' not in url:
                        url.replace("'", '')
                        self.urls.append(url)



    def parse_products(self,link_url,save = {}):
        save = set(save)
        if link_url:
            for i in link_url:


                    print(i)

                    self.driver.get(i)

                    cat_urls = [i.get_attribute('href') for i in self.driver.find_elements_by_xpath('//a[@class="subcat-name "]')]
                    
                    if cat_urls:
                        print('sub_categorys')
                        product = [i.text for i in self.driver.find_elements_by_xpath('//div[@class = "product-list-item-details"]/a/h4[@class="product-list-item-details-title"]') if i.text not in save]
                        save.union(set(product))
                        price = [i.text for i in self.driver.find_elements_by_xpath('//span[@class="product-details-price-item"]')]
                        product_price = dict(zip(product, price))
                        self.Data.append(product_price)

                        link_url += list(set(link_url) - set(cat_urls))
                        return self.parse_products(cat_urls,save)

                    else:

                        product = [i.text for i in self.driver.find_elements_by_xpath('//div[@class = "product-list-item-details"]/a/h4[@class="product-list-item-details-title"]')if i.text not in save]
                        save.union(set(product))
                        price = [i.text for i in self.driver.find_elements_by_xpath('//span[@class="product-details-price-item"]')]
                        product_price = dict(zip(product, price))
                        self.Data.append(product_price)
                        print(self.Data)

        return(self.Data)






    def to_csv(self):

        with open(self.CSV_FOLDER_PATH + '/SuperValue.csv', "w+", newline="") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            for dic in self.Data:
                for key in dic.keys():
                    writer.writerow(["product", "price"])
                    f.write("%s,%s\n" % (key, dic[key]))








if __name__ == "__main__":
    Supervlue().scrape()





