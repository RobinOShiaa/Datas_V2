'''
Created on 8 Nov 2016

@author: Suzanne
'''
import pandas as pd
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datetime import datetime
from datas.function.function import save_error_to_log
#import os
from datas.web.scraper import WebScraper
from datas.web.path import WEB_AUS_BUREAU_STATS_PATH, DOWNLOAD_PATH
import time
import sys
from datas.function.function import move_download_file, create_directory,\
    get_download_file_name, delete_file, get_file_name

def scrape(db_params):
    #try:
        print 'Start scraping at %s...' % datetime.now()
        today = datetime.now().strftime('%Y_%m_%d')
        dir_path = create_directory(WEB_AUS_BUREAU_STATS_PATH+'imports\\', today)
        url='http://www.abs.gov.au/International-Trade'
        scraper = WebScraper('Chrome')
        scraper.open(url)
        scraper.click_button('xpath', '//*[@id="element2list"]/li[1]/a')
        time.sleep(2)
        scraper.click_button('xpath', '//*[@id="tabsJ"]/ul/li[2]/a/span')
        time.sleep(2)
        scraper.click_button('xpath', '//*[@id="details"]/table/tbody/tr[20]/td[2]/a[1]/img')
        time.sleep(15)
        scraper.close()
        move_download_file(DOWNLOAD_PATH, dir_path)
        
        f = get_file_name(dir_path, pattern='*', extension='.xls')
        xls = pd.ExcelFile(dir_path+f[0])
        df = xls.parse('Data1', index_col=None)
        df.to_csv('%saus_imports.csv' % dir_path, index=False)

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