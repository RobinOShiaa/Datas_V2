'''
date created: 12/12/14
Author: Conor
'''
from selenium import webdriver
from datetime import datetime
import sys
import time
#import os
from datas.function.function import save_error_to_log
from datas.function.function import create_directory
from datas.web.path import WEB_MORRISONS_PATH
#from datas.web.scraper import WebScraper
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from bs4 import BeautifulSoup
import re
from selenium.common.exceptions import NoSuchElementException,\
    WebDriverException
        
def scrape(db_params):
    try:
        print 'Start scrape at %s...' % datetime.now()
        url = 'https://groceries.morrisons.com/webshop/getCategories.do?tags='
    
        browser = webdriver.Chrome()
        browser.get(url)
        
        #browse_shop = browser.find_element_by_xpath(".//*[@id='browseShopContainer']/div/a")
            
        category_links = browser.find_elements_by_xpath(".//*[@id='supernavSidebar_Grocery']/ul/li/a")
    
        category_names = []
        link_list = []
        for category_link in category_links:
            link_list.append(str(category_link.get_attribute('href')))
            tmp = str(category_link.text)
            tmp = re.sub(" \(\d+\)","", tmp)
            category_names.append(tmp.replace("&","").replace(",", "").replace(" ","_"))
    
        for link in xrange(0,len(link_list)):
            #print link_list[link]
            browser.get(link_list[link])
        
            browser.implicitly_wait(10)
            
            try:
                list_button = browser.find_element_by_xpath("//*[@id='content']/div[4]/div/div[2]/div/form[2]/button")
                list_button.click()
            except (NoSuchElementException, TypeError, WebDriverException) as e:
                continue
                
            time.sleep(3)    
            for scroll in xrange(0,500):
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
            html = browser.page_source
        
            soup = BeautifulSoup(html, 'html5')
        
            product_list = soup.find_all("div",{"class":"listProductWrap"})
            #print product_list
            product_names = []
            product_prices = []
        
            for product in product_list:
                product_name = product.find_all("a")
                #print product_name[1].text
                product_names.append(product_name[1].text.replace("\n","").replace("  ","").replace(",","").strip().encode('utf-8'))
                product_price = product.find_all("p",{"class":"pricePerWeight"})
                if not product_price:
                    continue
                product_prices.append(product_price[0].text.strip().encode('ascii', 'replace'))
            #print product_names
            #return
            #print len(product_prices)   
        
            if len(product_names) != len(product_prices):
                continue
            dir_title = datetime.now().strftime('%Y_%m_%d')
            file_path = create_directory(WEB_MORRISONS_PATH, dir_title)
            headers = ["product","unit","price"] 
            out_file = open('%s%s.csv' % (file_path, category_names[link]),'w')
            #print category_names[link]
            out_file.write('url,%s\n' % (link_list[link]))
            out_file.write(','.join(headers))
            out_file.write('\n')
            for product in xrange(0,len(product_names)):
                #print product_prices[product]
                price_list = product_prices[product].split('per')
                #print price_list
                #print product_names[product]
                try:
                    row = [product_names[product], price_list[1], price_list[0]]
                    
                    #print row
                except:
                    pass
                else:
                    out_file.write(','.join(row))
                    out_file.write('\n')
            out_file.close()
        
        browser.quit()
        print 'Finished scrape at %s' % datetime.now()
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['morrisons_scraper.py'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('daily', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['morrisons_scraper.py'],[success_msg]]
        save_error_to_log('daily', msg_list) 

if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)

