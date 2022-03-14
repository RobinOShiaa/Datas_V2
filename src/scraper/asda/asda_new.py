# -*- coding: utf-8 -*-
'''
Date Created: 15 Jul 2016
Author: Cliodhna Harrison
'''

import requests
import time
from bs4 import BeautifulSoup
import time
from datetime import datetime
import sys
from datas.db.manager import DBManager
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import create_directory, save_error_to_log
from datas.web.path import WEB_ASDA_PATH
from datas.web.scraper import WebScraper

def scrape(db_params):

    print 'Start scraping at %s...' % datetime.now()

    # get the latest data date from DB
    dbm = DBManager(db_params[0], db_params[1], db_params[2], db_params[3])
    sql = ('select max(date) as max_date from pig333_pig_price '
    'group by geo order by max_date asc limit 1;')
    date_from = dbm.get_latest_date_record(sql)
    date_from = date_from[0]
    del dbm


    dir_title = datetime.now().strftime('%Y_%m_%d')
    dir_path =  WEB_ASDA_PATH
    try:
        links_url = 'https://groceries.asda.com/?cmpid=ahc-_-ghs-_-asdacom-_-hp-_-nav-_-ghs'
        
        r = requests.get(url=links_url, verify=False)
        browser = WebScraper('Chrome')
        browser.web_driver.maximize_window()
        browser.open(links_url)
        links_soup = BeautifulSoup(r.content, "html.parser")

        urls = []
        i = 1
        list_primary_nav = browser.find_elements('xpath', '//*[@id="primary-nav-items"]/div/li')
        num_primary_nav = len(list_primary_nav)
        while i <= num_primary_nav:
            link = browser.find_element("xpath", '//*[@id="primary-nav-items"]/div/li[{}]/a'.format(i)).get_attribute("href")
            urls.append(link)
            i += 1
        newdir_path = create_directory(dir_path, dir_title)
        
        for url in urls:
            browser = WebScraper('Chrome')
            browser.web_driver.maximize_window()
            browser.open(url)
            time.sleep(3)

            html = browser.web_driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            
            
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
                browser.web_driver.maximize_window()
                browser.open(url_2)
                time.sleep(3)

                html = browser.web_driver.page_source
                soup = BeautifulSoup(html, 'html.parser')

                
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
                    browser.web_driver.maximize_window()
                    browser.open(url_3)
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
                        browser.web_driver.maximize_window()
                        browser.open(url_4)
                        time.sleep(3)

                        r = requests.get(url=url_4, verify=False)
                        soup = BeautifulSoup(r.content, "html.parser")
                        
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

                            r = requests.get(url=url_5, verify=False)
                            soup = BeautifulSoup(r.content, "html.parser")
                        
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
                                out_file.write(url_4 + ',\n')
                            init = False
                            
                            if price_per_bool:
                                price = price.encode('ascii', 'replace')
                                price_per = price_per.encode('ascii', 'replace')
                                content = product_title +", " + price + ", " + amount + "," + price_per + ", \n"
                                
                            else:
                                price = price.encode('ascii', 'replace')
                                content = product_title + ", " + price + ", " + amount + ", \n"
                            out_file.write(content)

                            print "product finished"
                            print url_5

                            
                        print "Page finished"
                        try:
                            browser.open(url_4)
                            next_button = browser.find_element('xpath', '//*[@id="listings-pagination-container-top"]/div/a[2]')
                            next_button.click()

                            menu_shelf.append(browser.current_url)

                            menu_shelf.append(browser.web_driver.current_url)

                            browser.close()
                        except:
                            continue
                            out_file.close()
                            browser.close()

    except:
        print "Error"
    except Exception as e:
        print e

                
    print 'Finish scraping at %s.' % datetime.now()
    browser.close()


if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
