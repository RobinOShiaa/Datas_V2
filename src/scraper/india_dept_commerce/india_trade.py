'''
Created on 10 May 2016

@author: Suzanne
'''
from datas.function.function import save_error_to_log, chunck_list
import os
import csv
import sys
from bs4 import BeautifulSoup
import time
from datetime import datetime
from datetime import timedelta
from datas.db.manager import DBManager
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import create_directory
from datas.web.path import DOWNLOAD_PATH
from datas.web.path import WEB_INDIA_DEPT_COMMERCE_PATH
from datas.web.scraper import WebScraper

def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()
        scraper = WebScraper('Chrome')
        url='http://commerce.nic.in/eidb/ecntcomq.asp'
        today = datetime.now().strftime('%Y_%m_%d')
        dir_path = create_directory(WEB_INDIA_DEPT_COMMERCE_PATH+'trade', today)
        
        heads = ['Partner']
        
        scraper.open(url)
        countries_k = scraper.get_dropdown_list('name', 'cntcode')
        countries_v = scraper.get_dropdown_list('name', 'cntcode','text')
        scraper.close()
        countries_d = dict(zip(countries_k,countries_v))
        run_once = 0
        for key, value in countries_d.iteritems():
            data = []
            scraper = WebScraper('Chrome')
            scraper.open(url)
            scraper.load_field('select','name','cntcode',key)
            scraper.load_field('select','name','hslevel','8')
            radio_button = scraper.find_element('xpath', '//*[@id="radioDAll"]')
            radio_button.click()
            scraper.click_button('name', 'radioqty')
            scraper.click_button('name', 'button1')
            time.sleep(10)
             
            html = scraper.html_source()
            soup = BeautifulSoup(html, 'html5')
            if run_once == 0:
                headers = soup.find_all('th')
                for h in headers:
                    heads.append(h.text.replace(' ','').replace('\n','').replace('\t',''))
                    
                with open (dir_path+'trade.csv','a') as f:
                    f.write(','.join(heads))
                    f.write('\n')
                run_once = 1
            
            data_points = soup.find_all('td')
            string = '\xa0'
            decoded_str = string.decode("windows-1252")
            #encoded_str = decoded_str.encode("utf8")
            for d in data_points:
                data.append(d.text.replace('\n','').replace('\t','').replace(',','-').replace(decoded_str,'-').strip(' '))
               
            scraper.close()
            data = chunck_list(data, len(heads)-1) 
            
            with open (dir_path+'trade.csv','a') as f:
                for datum in data:
                    f.write(value+','+','.join(datum))
                    f.write('\n')
            print 'Finished scraping at %s.' % datetime.now()
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['india_trade.py'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('monthly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['india_trade.py'],[success_msg]]
        save_error_to_log('monthly', msg_list)
         
if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)