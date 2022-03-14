'''
Created on 14 Nov 2016

@author: Suzanne
'''
'''
Created on 8 Nov 2016

@author: Suzanne
'''
import pandas as pd
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datetime import datetime
from datas.function.function import save_error_to_log, chunck_list
#import os
from datas.web.scraper import WebScraper
from datas.web.path import WEB_AUS_BUREAU_STATS_PATH, DOWNLOAD_PATH
import time
import sys
from bs4 import BeautifulSoup
from datas.function.function import move_download_file, create_directory,\
    get_download_file_name, delete_file, get_file_name

def scrape(db_params):
    #try:
        print 'Start scraping at %s...' % datetime.now()
        years = []
        data = []
        today = datetime.now().strftime('%Y_%m_%d')
        dir_path = create_directory(WEB_AUS_BUREAU_STATS_PATH+'imports\\', today)
        url='http://stat.data.abs.gov.au/'
        scraper = WebScraper('Chrome')
        scraper.web_driver.maximize_window()
        scraper.open(url)
        scraper.click_button('xpath', '//*[@id="browsethemes"]/ul/li[1]') #economy
        time.sleep(2)
        scraper.click_button('xpath', '//*[@id="browsethemes"]/ul/li[1]/ul/li[3]') #trade
        time.sleep(2)
        scraper.click_button('xpath', '//*[@id="browsethemes"]/ul/li[1]/ul/li[3]/ul/li[3]') #imports
        time.sleep(2)
        scraper.click_button('xpath', '//*[@id="browsethemes"]/ul/li[1]/ul/li[3]/ul/li[3]/ul/li') #thousand $
        time.sleep(2)
        scraper.click_button('xpath', '//*[@id="browsethemes"]/ul/li[1]/ul/li[3]/ul/li[3]/ul/li/ul/li[3]/a[2]') #by SITC
        time.sleep(15)
        
        ths = scraper.find_elements('xpath','//table/thead/tr/th[@class="HDim"]')
        for th in ths:
            if th.text not in years:
                years.append(th.text)
                
        tds = scraper.find_elements('xpath','.//table[@class="DataTable"]/tbody/tr[contains(@class,"row")]/td')
        for td in tds:
            data.append(td.text)
            
        data = filter(None, data)
        #data = chunck_list(data,len(years))
        for d in data:
            print data.index(d)
            if 'TOTAL' in d:
                
                print d
        
        #years = filter(None, years)
        #years = list(set(years))
        
        
#         html = scraper.web_driver.page_source()
#         soup = BeautifulSoup(html)
#         table = soup.find('table',{'class':'DataTable'})
#         print table
        
        
        
        #scraper.close()
        
        print 'Finished scraping at %s.' % datetime.now()

#     except Exception as err:
#         exc_info = sys.exc_info()
#         error_msg = 'auto_run() scrape error:\n'
#         msg_list = [['aus_trade_imports.py'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
#         print msg_list
#         save_error_to_log('monthly', msg_list)
#     else:
#         success_msg = 'auto_run() scraped successfully\n'
#         msg_list = [['aus_trade_imports.py'],[success_msg]]
#         save_error_to_log('monthly', msg_list)
    
if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)