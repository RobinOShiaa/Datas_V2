# -*- coding: utf-8 -*-
'''
Created on 31 Aug 2016

@author: Suzanne
'''

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException,\
    TimeoutException
from datetime import datetime
import time
from datas.function.function import create_directory#, save_to_file_append
from datas.web.scraper import WebScraper
import sys
#import os
from datas.function.function import save_error_to_log , chunck_list
from datas.web.path import WEB_SUPERVALU_PATH
from datas.db.manager import RAW_DB_NAME, USERNAME, PASSWORD, HOST

def login(scraper, username_element, password_element, username, password, button_id):
    '''Uses tag IDs. NB - Must have already registered with site.'''
    element1 = scraper.find_element('id', username_element)
    element1.send_keys(username)
    element2 = scraper.find_element('id', password_element)
    element2.send_keys(password)
    scraper.click_button('id', button_id)

def find_next(scraper):
    try:
        next_button = scraper.find_element('xpath', '//div[@class="pagingDisplay"]/a[text()="Next"]')
    except NoSuchElementException:
        return False 
    else:
        next_button.click()
        return True 


def scrape(db_params):
    try:
        print 'Start scrape at %s...' % datetime.now()
        link_urls=[]
        
        url = 'https://shop.supervalu.ie/shopping/selected-offers'
        today = datetime.now().strftime("%Y_%m_%d")
        headers = ['Product name','Price (euro)', 'per unit']
        
        dir_path = create_directory(WEB_SUPERVALU_PATH, today)
        file_path = '%ssupermarket.csv' % (dir_path)
        
        with open(file_path, 'a') as file:
            file.write('url,'+url+'\n'+','.join(headers)+'\n')
        
        scraper = WebScraper('Chrome')
        scraper.web_driver.implicitly_wait(0)
        scraper.open(url)
        scraper.web_driver.maximize_window()
    
        scraper.click_button('xpath', '//*[@id="menuToggle"]/span')
        
        
        
        tags = scraper.find_elements('xpath', '//*[@class="menu-inner"]/a')
        for tag in tags:
            scraper.hover('element', tag)
            tags2 = scraper.find_elements('xpath','//*[@class="pseudo-group"]//a')
            for tag2 in tags2:
                link_urls.append(tag2.get_attribute('href'))
        
        scraper.close()
        
        for l_u in link_urls:
            data=[]
            try:
                scraper = WebScraper('Chrome')
                scraper.open(l_u)
                tags3 = scraper.find_elements('class', 'product-list-item-details')
                
                for tag3 in tags3:
                    data.append(tag3.text.encode('ascii', 'ignore').replace('    View all items in offer','').replace(',','-'))
                scraper.close() 
                #data = chunck_list(data,2)
    
                
                '''Data output'''
                with open(file_path, 'a') as file:
                    for d in data:
                        d = d.split('\n')
                        #file.write(d[0]+','+d[1].split(' ')[0]+d[1].split(' ')[1:]+'\n')
                        file.write(d[0]+','+d[1].split(' ')[0]+','+' '.join(d[1].split(' ')[1:])+'\n')
            except TimeoutException:
                continue
        #scraper.close()
        print 'Finished scrape at %s.' % datetime.now()
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['supervalu'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('daily', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['supervalu'],[success_msg]]
        save_error_to_log('daily', msg_list)
       

if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)

    
