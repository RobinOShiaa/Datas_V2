'''
Created on 12 Mar 2015

@author: Suzanne
'''
import sys
from datas.function.function import save_error_to_log
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import create_directory,move_download_file
from datas.web.path import DOWNLOAD_PATH, WEB_QUANDL_PATH
from datetime import datetime
import time
#import urllib
import os
from datas.web.scraper import WebScraper


def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()
        
        path = '%sveg_oils_price\\' % WEB_QUANDL_PATH
        today = datetime.strftime(datetime.now(), '%Y_%m_%d\\')

        urls = ['https://www.quandl.com/api/v1/datasets/GDT/REN_SU.csv', 
                'https://www.quandl.com/api/v1/datasets/WORLDBANK/WLD_SOYBEAN_OIL.csv',
                'https://www.quandl.com/api/v1/datasets/ODA/PSUNO_USD.csv', #sunflower oil
                'https://www.quandl.com/api/v1/datasets/ODA/PROIL_USD.csv',  #rapeseed oil
                'https://www.quandl.com/api/v1/datasets/WORLDBANK/WLD_COCONUT_OIL.csv', 
                'https://www.quandl.com/api/v1/datasets/WORLDBANK/WLD_PALM_OIL.csv',
                'https://www.quandl.com/api/v3/datasets/ODA/PPOIL_USD.csv',#palm oil
                'https://www.quandl.com/api/v3/datasets/ODA/PSOIL_USD.csv'#soybean oil
                #'https://www.quandl.com/api/v1/datasets/INDEXMUNDI/COMMODITY_SOYBEANOIL.csv', # out of date
                #'https://www.quandl.com/api/v1/datasets/INDEXMUNDI/COMMODITY_PALMOIL.csv'# out of date
                ]  
        
        
        #product_names = {'REN_SU.csv':'casein_rennet.csv', 'PSUNO_USD.csv':'sunflower_oil.csv', 'PROIL_USD.csv':'rapeseed_oil.csv'}
        
        for url in urls:
            
            scraper = WebScraper('Chrome')
            scraper.open(url)
            
            time.sleep(10)
            scraper.close()
            
    #         old_filename = url.split('/')[-1]
    #         filename = ''
    #         
    #         if old_filename in product_names:
    #             filename = product_names.get(old_filename)
    #             
    #         else:
    #             filename = old_filename.lower()    
    #         
    #         source_site = url.split('/')[-2]
            
            #download_file =  '%s\\%s-%s' % (DOWNLOAD_PATH, source_site, old_filename)
    
            new_path = create_directory(path, today)
            move_download_file(DOWNLOAD_PATH, new_path)
        
            ##os.rename(download_file, '%s%s-%s' % (new_path, source_site, filename))
        
        print 'Finish scraping at %s.' % datetime.now()
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['quandl.veg_oils_price.py'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('weekly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['quandl.veg_oils_price.py'],[success_msg]]
        save_error_to_log('weekly', msg_list)


if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
    