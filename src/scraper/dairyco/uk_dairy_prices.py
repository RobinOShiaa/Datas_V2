'''
Created on 28 Apr 2015

@author: Suzanne
Note that this scraper requires chrome as the browser, cannot run with firefox
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
        
        url= 'http://www.dairyco.org.uk/resources-library/market-information/milk-prices-contracts/uk-wholesale-prices/#.VT5aByFVhBc'
          
        scraper = WebScraper('Chrome')
        scraper.open(url)

        scraper.click_button('xpath', './/*[@id="wrapper"]/div[6]/div[2]/div/div[@class="column2-content"]/a')

        time.sleep(5)
        scraper.close()
         
        new_path = create_directory(path, today)
        f = get_file_name(DOWNLOAD_PATH, pattern='uk_wholesale_prices', extension='.xls')
        xls = pd.ExcelFile(DOWNLOAD_PATH+f[0])
        df = xls.parse('UK Wholesale Prices', index_col=None)
        df.to_csv('%suk_dairy_wholesale_prices.csv' % new_path, encoding='utf-8',index_label=None, index=False)

        print 'Finish scraping at %s.' % datetime.now()
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['dairyco.uk_dairy_prices.py'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('monthly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['dairyco.uk_dairy_prices.py'],[success_msg]]
        save_error_to_log('monthly', msg_list)


if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
    

