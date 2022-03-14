
from datetime import datetime
import time
from scraper_classes.chrome_scraper import ChromeScraper
import csv
from selenium.common.exceptions import NoSuchElementException
class waitrose(ChromeScraper):


    def __init__(self, url = 'https://www.waitrose.com/ecom/shop/Browse/Groceries?flt=promotionflag%3A1&sortBy=MOST_POPULAR', CSV_FOLDER_PATH=None):
        super().__init__(url, CSV_FOLDER_PATH)
        self.driver.get(url)
        self.Data = []
        print('Start scraping at %s...' % datetime.now())

    def scrape(self):
        time.sleep(5)

        try:
            time.sleep(5)

            load_more = self.driver.find_element_by_xpath('//*[@id="tSr"]/div/div[2]/button').click()
            self.scrape()
        except NoSuchElementException as e:
            print('scraping products')
            prices = [i.text for i in self.driver.find_elements_by_xpath(
                '//article[@data-test="product-pod"]/div/section[2]/div[1]/span[1]/span')]
            print(prices)
            products = [i.text for i in self.driver.find_elements_by_xpath(
                '//article[@data-test="product-pod"]/div/section[1]/header/div[1]/a/h2/div/span[1]')]
            print(products)
            product_price = dict(zip(products,prices))

            print(product_price)
            self.to_csv(product_price)

    def to_csv(self,k):

        with open(self.CSV_FOLDER_PATH + '/waitrose.csv', "w+", newline="") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerow(["product", "price"])
            for key in k:
                f.write("%s,%s\n" % (key, k[key]))


if __name__ == "__main__":
    waitrose().scrape()
