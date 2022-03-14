'''
Created on 28 Apr 2015

@author: Suzanne
'''
import time
from datetime import datetime
import sys
import os
from datas.function.function import save_error_to_log
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import get_file_name, create_directory
from datas.web.scraper import WebScraper
from datas.web.path import DOWNLOAD_PATH, WEB_DAIRYCO_PATH
import pandas as pd

def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()
        
        path = '%sprices//' % WEB_DAIRYCO_PATH
        today = datetime.strftime(datetime.now(), '%Y_%m_%d\\')
        
        url= 'http://www.dairyco.org.uk/resources-library/market-information/milk-prices-contracts/world-wholesale-prices/#.VT5alSFVhBc'
         
        scraper = WebScraper('Chrome')
        scraper.open(url)
          
        scraper.click_button('xpath', './/*[@id="wrapper"]/div[6]/div[2]/div/div[@class="column2-content"]/a/img')
        time.sleep(10)
          
        scraper.close()
        
        new_path = create_directory(path, today)
        f = get_file_name(DOWNLOAD_PATH, pattern='world_wholesale_prices_new', extension='.xlsx')
        xls = pd.ExcelFile(DOWNLOAD_PATH+f[0])
        df = xls.parse('Region', index_col=None)
        df.to_csv('%sworld_dairy_wholesale_prices.csv' % new_path, index_label=None, index=False)

        print 'Finish scraping at %s.' % datetime.now()

    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['dairyco.world_dairy_prices.py'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('monthly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['dairyco.world_dairy_prices.py'],[success_msg]]
        save_error_to_log('monthly', msg_list)


if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
    
