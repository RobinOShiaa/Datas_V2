'''
Created on 13 Mar 2015

@author: Suzanne

TODO(Wenchong): Need to create new table and write loader.
'''

import sys
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import create_directory
from datas.web.path import DOWNLOAD_PATH, WEB_QUANDL_PATH
from datetime import datetime
import time
from datas.function.function import save_error_to_log
import os
from datas.web.scraper import WebScraper


def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()
        
        path = '%sgrain_price\\' % WEB_QUANDL_PATH
        today = datetime.strftime(datetime.now(), '%Y_%m_%d\\')
        urls = ['https://www.quandl.com/api/v1/datasets/ODA/PWHEAMT_USD.csv', 'https://www.quandl.com/api/v1/datasets/WORLDBANK/WLD_BARLEY.csv']  
        
        
        product_names = {'PWHEAMT_USD.csv':'wheat.csv'}
        
        for url in urls:
            
            scraper = WebScraper('Chrome')
            scraper.open(url)
            
            time.sleep(5)
            scraper.close()
            
            old_filename = url.split('/')[-1]
            filename = ''
            
            if old_filename in product_names:
                filename = product_names.get(old_filename)
                
            else:
                filename = old_filename.lower()    
            
            source_site = url.split('/')[-2]
            
            download_file = '%s\\%s-%s' % (DOWNLOAD_PATH, source_site, old_filename)
            #print download_file
    
            new_path = create_directory(path, today)
        
            os.rename(download_file, '%s%s-%s' % (new_path, source_site, filename))
        
        print 'Finish scraping at %s.' % datetime.now()
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['quandl.grain_price.py'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('monthly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['quandl.grain_price.py'],[success_msg]]
        save_error_to_log('monthly', msg_list)


if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
    