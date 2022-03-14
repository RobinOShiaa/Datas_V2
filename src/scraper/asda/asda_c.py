# -*- coding: utf-8 -*-
'''
Date Created: 15 Jul 2016
Author: Cliodhna Harrison

13-09-2016(sue):
changed 'driver' to 'browser.web_driver' on 169,
printed out exception,
moved lines above continue at end,
got rid of database code,
commented out r and beautifulsoup code not being used,
14-09-2016(sue): 
moved url calls to before window maximise,
note: nothing to catch error when object is unavailable
Why scraping each individual product page????
'''

import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime
import sys
from datas.db.manager import DBManager
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import create_directory, save_error_to_log
from datas.web.path import WEB_ASDA_PATH
from datas.web.scraper import WebScraper

def scrape(db_params):

    print 'Start scraping at %s...' % datetime.now()

    dir_title = datetime.now().strftime('%Y_%m_%d')
    dir_path =  WEB_ASDA_PATH
    
    links_url = 'https://groceries.asda.com/?cmpid=ahc-_-ghs-_-asdacom-_-hp-_-nav-_-ghs'
    
    #r = requests.get(url=links_url, verify=False)
    browser = WebScraper('Chrome')
    browser.open(links_url)
    browser.web_driver.maximize_window()
    
    #links_soup = BeautifulSoup(r.content, "html.parser")
    urls = []
    i = 1
    list_primary_nav = browser.find_elements('xpath', '//*[@id="primary-nav-items"]/div/li')
    num_primary_nav = len(list_primary_nav)
    while i <= num_primary_nav:
        link = browser.find_element("xpath", '//*[@id="primary-nav-items"]/div/li[{}]/a'.format(i)).get_attribute("href")
        urls.append(link)
        i += 1
    newdir_path = create_directory(dir_path, dir_title)
    
    for url in urls[1:]:
        #try:
        browser = WebScraper('Chrome')
        browser.open(url)
        browser.web_driver.maximize_window()
        
        time.sleep(3)
        #html = browser.web_driver.page_source
        #soup = BeautifulSoup(html, 'html.parser')
        
        
        urls_underline = []
        i = 1
        list_secondary_nav = browser.find_elements('xpath', '//*[@class="container"]/ul/div/li')
        num_secondary_nav = len(list_secondary_nav)
        while i <= num_secondary_nav:
            link = browser.find_element("xpath", '//*[@class="container"]/ul/div/li[{}]/a'.format(i)).get_attribute("href")
            urls_underline.append(link)
            i += 1
            
        urls_underline = urls_underline[:-1]
        #takes special offers off list
            
        for url_2 in urls_underline:
            browser = WebScraper('Chrome')
            browser.open(url_2)
            browser.web_driver.maximize_window()
            
            time.sleep(3)
            #html = browser.web_driver.page_source
            #soup = BeautifulSoup(html, 'html.parser')
            
            menu_aisles = []
            i = 1
            list_tertiary_nav = browser.find_elements('xpath', '//*[@class="menu_aisles"]/div/li')
            num_tertiary_nav = len(list_tertiary_nav)
            while i <= num_tertiary_nav:
                link = browser.find_element("xpath", '//*[@class="menu_aisles"]/div/li[{}]/a'.format(i)).get_attribute("href")
                menu_aisles.append(link)
                i += 1
                
            
            for url_3 in menu_aisles:
                browser = WebScraper('Chrome')
                browser.open(url_3)
                browser.web_driver.maximize_window()
                
                time.sleep(3)
                
                menu_shelf = []
                i = 1
                list_quaternary_nav = browser.find_elements('xpath', '//*[@class="menu_shelf"]/div/li')
                num_quaternary_nav = len(list_quaternary_nav)
                while i <= num_quaternary_nav:
                    link = browser.find_element("xpath", '//*[@class="menu_shelf"]/div/li[{}]/a'.format(i)).get_attribute("href")
                    menu_shelf.append(link)
                    i += 1
                
                for url_4 in menu_shelf:
                    
                    browser = WebScraper('Chrome')
                    browser.open(url_4)
                    browser.web_driver.maximize_window()
                    
                    time.sleep(3)
                    #r = requests.get(url=url_4, verify=False)
                    #soup = BeautifulSoup(r.content, "html.parser")
                    
                    title = browser.find_element('xpath', '//*[@id="pageTitle"]/h1')
                    title = title.text
                    
                    if "View" in str(title):
                        browser.close()
                        break
                    
                    print "2"
                    product_pages_web = browser.find_elements('xpath', '//*[@id="componentsContainer"]/div[@id="listingsContainer"]/div/div/div[@class="container"]/div/div/div/span[@id="productTitle"]/a')
                    product_pages = [page.get_attribute('href') for page in product_pages_web]
                    
                    init = True

                    for url_5 in product_pages:
                        price_per_bool = False
                        browser.open(url_5)
                        time.sleep(3)
                        #r = requests.get(url=url_5, verify=False)
                        #soup = BeautifulSoup(r.content, "html.parser")
                    
                        product_title_web = browser.find_element('xpath', '//*[@id="itemDetails"]/h1')
                        product_title = product_title_web.text
                    
                        amounts_web = browser.find_element('xpath', '//*[@id="itemDetails"]/span')
                        amount = amounts_web.text
                        
                        price_web = browser.find_elements('xpath', '//*[@id="itemDetails"]/div[3]/p[1]/span')
                        if len(price_web) > 1:
                            price = price_web[0].text
                            price_per = price_web[1].text
                            price_per_bool = True
                        else:
                            price = price_web[0].text
            
                        file_path = newdir_path + str(title) + ".csv"
                        out_file = open(file_path, 'a')
                        if init:
                            out_file.write(url_5 + ',\n')
                        init = False
                        
                        if price_per_bool:
                            price = price.encode('ascii', 'replace')
                            price_per = price_per.encode('ascii', 'replace')
                            content = product_title +"," + price + "," + amount + "," + price_per + ",\n"
                            
                        else:
                            price = price.encode('ascii', 'replace')
                            content = product_title + "," + price + "," + amount + ",\n"
                        out_file.write(content.encode('ascii', 'replace'))
                        print url_5
                        
                    print "Page finished"
                    try:
                        browser.open(url_4)
                        next_button = browser.find_element('xpath', '//*[@id="listings-pagination-container-top"]/div/a[2]')
                        next_button.click()
                        menu_shelf.append(browser.web_driver.current_url)
                        browser.close()
                    except:
                        out_file.close()
                        browser.close()
                        continue
                            
#         except Exception as e:
#             print e
#                 
#     print 'Finish scraping at %s.' % datetime.now()
#     browser.close()


if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
