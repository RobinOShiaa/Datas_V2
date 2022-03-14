# -*- coding: utf-8 -*-
'''
Created on 22 Jun 2015

@author: Suzanne
'''
from datetime import datetime
import time
import subprocess
import urllib
from datas.web.scraper import WebScraper
from datas.web.path import WEB_ZUIVELNL_PATH
from datas.function.function import create_directory, save_error_to_log
from datas.db.manager import DBManager, RAW_DB_NAME, TEST_DB_NAME, USERNAME, PASSWORD, HOST
import sys

def scrape():
    try:
        print 'Start scraping at %s...' % datetime.now()
        dir_path = '%sprices' % WEB_ZUIVELNL_PATH
        today = datetime.strftime(datetime.now(), '%Y_%m_%d')
        dir_path = create_directory(dir_path, today)
        url = 'http://www.zuivelnl.org/'
        scraper = WebScraper('Chrome')
        scraper.open(url)
        
        xpath = '//*[@id="post-878"]/div[2]//li'
        date = scraper.find_element('xpath','//*[@id="post-878"]/h2/a/cufon[5]/cufontext').text
        elements = scraper.find_elements('xpath',xpath)
        
        for e in elements[:-1]:
            product=e.text.split(':')[0].replace(',','-')
            price=e.text.split(u"\u20AC")[-1].replace(',','.').replace(' ','')
            with open(dir_path+'prices.csv','ab') as file:
                file.write(','.join([date,product,price]).encode('ascii','replace')+'\n')
        
        scraper.close()
        print 'Finished scraping at %s.' % datetime.now()
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['zuivelnl_price_weekly.py'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('weekly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['zuivelnl_price_weekly.py'],[success_msg]]
        save_error_to_log('weekly', msg_list)
        
if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape()