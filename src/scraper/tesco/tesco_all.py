'''
date created: 5/12/2014
Author: Conor
'''

from bs4 import BeautifulSoup
import sys
#import os
from datas.function.function import save_error_to_log
from datas.function.function import create_directory
from datas.web.scraper import WebScraper
from datas.web.path import WEB_TESCO_PATH
from datetime import datetime
from datas.db.manager import RAW_DB_NAME, USERNAME, PASSWORD, HOST


def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()
        url = 'http://www.tesco.ie/groceries/'
           
        browser = WebScraper('Chrome')
        browser.web_driver.implicitly_wait(10)
        browser.open(url)
        
        dir_title = datetime.now().strftime('%Y_%m_%d')
        file_path = create_directory(WEB_TESCO_PATH, dir_title)
        
        categories = browser.find_elements('xpath','//div[@id="secondaryNav"]/ul/li/a[@class="flyout"]')
    
        url_links = []
        sub_category_names = []
        
        for category in categories:
            browser.hover('element', category)
    
            sub_categories = browser.find_elements('xpath','//ul[@class="tertNav"]/li/h3/a')
    
            for sub_category in sub_categories:
                url_links.append(str(sub_category.get_attribute('href')))
                sub_category_names.append(str(sub_category.text).replace(' ','_').replace(',','').replace('&','').replace('-','').strip())
        
        browser.close()
        headers = ["product","price","unit"]
        sub_category_number = 0
        
        for url_link in url_links:
            product_names = []
            product_prices = []
            
            browser = WebScraper('Chrome')
            browser.web_driver.implicitly_wait(10)
            browser.open(url_link)
                    
            more_info = True
            while (more_info == True):
    
                html = browser.web_driver.page_source
                soup = BeautifulSoup(html,'html5')
                #if(sub_category_number == 1):
                #    print soup.prettify()
                product_div = soup.find_all("ul",{"class":"cf products line"})
                
                for variety in xrange(0, len(product_div)):
                    product_lis = product_div[variety].find_all("li")
                    for product_li in product_lis:
                        product_name = product_li.find_all("h3")
                        if(len(product_name) > 0):
                            product_price = product_li.find_all("p",{"class":"price"})[0].find_all("span")[1]
                            product_names.append(product_name[0].text.strip().encode('utf-8', 'ignore').replace(',',''))
                            product_prices.append(product_price.text.strip().encode('utf-8', 'ignore').replace(',',''))
                
                try:
                    browser.click_button('xpath', '//ul/li/p[@class="next"]/a')
                except:
                    more_info = False
                    break
                else:
                    more_info = True  
            
            browser.close()
            out_file = open('%s%s.csv' % (file_path, sub_category_names[sub_category_number]),'w')
            out_file.write('url,%s\n' % (url_link))
            out_file.write(','.join(headers))
            out_file.write('\n')
            for product in xrange(0,len(product_names)):
                out_file.write(product_names[product] + ',' + product_prices[product].replace('/',','))
                out_file.write('\n')
            out_file.close()    
            sub_category_number += 1
    
        print 'Finish scraping at %s.' % datetime.now()

    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['tesco_all.py'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('daily', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['tesco_all.py'],[success_msg]]
        save_error_to_log('daily', msg_list)
        
if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)

    
