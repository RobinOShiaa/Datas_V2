from scraper_classes.chrome_scraper import ChromeScraper
import csv
import time
from scrapers import logger

class Walmart(ChromeScraper):
    def __init__(self, url='https://www.walmart.com/cp/food/976759',
                 CSV_FOLDER_PATH=None):
        #self.CSV_FOLDER_PATH = CSV_FOLDER_PATH
        super().__init__(url, CSV_FOLDER_PATH)

    def scrape(self):
        walmart_logger = logger.get_logger(('Walmart logger'))
        walmart_logger.info('Start scraping')
        self.driver.get(self.url)

        "#collect all category's urls to scrape"
        cat = [x.get_attribute("href") for x in self.driver.find_element_by_class_name('clearfix').find_elements_by_tag_name("a")][:-1]

        "#begin writing first page to csv"
        with open('csv_files/walmart.csv', 'w', encoding='utf-8', newline='') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)

            "#set row titles"
            wr.writerow(["Product", "Price"])
            for url in cat:
                "#click on first url"
                self.driver.get(url)
                condition = True
                "#if contained in alt tag grab product"
                while condition:
                    product = [j.get_attribute('alt') for j in self.driver.find_elements_by_xpath(
                        '//*[@id="searchProductResult"]/ul/li/div/div[2]/div[2]/div/a/img')]
                    find_elem = self.driver.find_elements_by_class_name("price-main-block")
                    product_price = []
                    for tag in find_elem:
                        "#if contains /... split and format it like other numbers"
                        if '/' in tag.text:
                            product_price.append(".".join([tag.text.split(".")[0], tag.text.split(".")[1][:2]]))
                        else:
                            product_price.append(tag.text)

                    "#dict of both product and price"
                    prod_price = dict(zip(product, product_price))
                    for row in prod_price.items():
                        wr.writerow([row[0], row[1]])

                    "#try to click next button"
                    try:
                        self.driver.find_element_by_xpath(
                            '//*[@id="mainSearchContent"]/div[3]/div[2]/button[@class="elc-icon paginator-hairline-btn paginator-btn paginator-btn-next outline"]').click()
                        time.sleep(2)

                        print('turning page')

                    except Exception as e:
                        # print('no more products', str(e))
                        "#if no more products exit"
                        condition = False
                        # your_csv_file.close()
                        walmart_logger.info('Walmart finished scraping')

if __name__ == "__main__":
    Walmart().scrape()
