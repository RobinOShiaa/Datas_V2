'''
Created on 27 Apr 2015

@author: Suzanne
'''
import time
from datetime import datetime
import sys
from datas.function.function import save_error_to_log
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import get_file_name, create_directory
from datas.web.scraper import WebScraper
from datas.web.path import DOWNLOAD_PATH, WEB_EC_EUROPA_PATH
import pandas as pd

def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()
    
        today = datetime.strftime(datetime.now(), '%Y_%m_%d\\')
        url= 'http://ec.europa.eu/agriculture/milk-market-observatory/'
        
        scraper = WebScraper('Chrome')
        scraper.open(url)
         
        scraper.click_button('link_text', '> EU historical prices')
        time.sleep(7)
        scraper.close()
    
        f = get_file_name(DOWNLOAD_PATH, pattern='eu-historical-price-series_en', extension='.xls')
        new_path = create_directory(WEB_EC_EUROPA_PATH, today)
        xls = pd.ExcelFile(DOWNLOAD_PATH+f[0])
        df = xls.parse('Raw Milk Prices', index_col=None)
        df.to_csv('%sraw_milk_prices.csv' % new_path, index=False)
        df = xls.parse('Dairy Products Prices', index_col=None)
        df.to_csv('%sdairy_products_prices.csv' % new_path, index=False)
        
        print 'Finish scraping at %s...' % datetime.now()
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['ec_europa_dairy_prices.py'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('monthly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['ec_europa_dairy_prices.py'],[success_msg]]
        save_error_to_log('monthly', msg_list)


if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
    
