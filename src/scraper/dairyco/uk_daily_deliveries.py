'''
Created on 8 Nov 2016

@author: Suzanne
'''
import time
from datetime import datetime
import sys
import os
from bs4 import BeautifulSoup
from datas.function.function import save_error_to_log
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import get_file_name, create_directory
from datas.web.scraper import WebScraper
from datas.web.path import DOWNLOAD_PATH, WEB_DAIRYCO_PATH
import pandas as pd
import urllib2

def scrape():
    try:
        print 'Start scraping at %s...' % datetime.now()
        
        path = '%sdeliveries//' % WEB_DAIRYCO_PATH
        today = datetime.strftime(datetime.now(), '%Y_%m_%d\\')
        
        url= 'https://dairy.ahdb.org.uk/resources-library/market-information/supply-production/daily-milk-deliveries/#.WCHTcS2LSJA'
        
        scraper = WebScraper('Chrome')
        scraper.open(url)
        
        scraper.click_button('xpath', '//*[@id="wrapper"]/div[6]/div[2]/div/div/a')
        time.sleep(35)
        scraper.close()
         
        new_path = create_directory(path, today)
        f = get_file_name(DOWNLOAD_PATH, pattern='*uk_daily_milk_deliveries*', extension='.xls')
        xls = pd.ExcelFile(DOWNLOAD_PATH+f[0])
        #df = xls.parse('2016-17', index_col=None)
        df = xls.parse('UK Daily deliveries', index_col=None)
        df.to_csv('%suk_daily_milk_deliveries.csv' % new_path, encoding='utf-8',index_label=None, index=False)
    
        
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
    scrape()
