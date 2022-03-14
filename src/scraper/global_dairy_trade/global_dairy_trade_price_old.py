'''
Created on 11 Mar 2015

@author: Suzanne
'''
import time
from datetime import datetime
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import create_directory
from datas.web.scraper import WebScraper
from datas.web.path import DOWNLOAD_PATH, WEB_GLOBALDAIRYTRADE_PATH
import pandas as pd
import sys
from datas.function.function import save_error_to_log
import os


def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()
        
        #url = 'https://www.globaldairytrade.info/en/product-results/rennet-casein/'
        #url = 'https://www.globaldairytrade.info/en/product-results/download-historical-data/?cb=1426764801040'
        url = 'https://www.globaldairytrade.info/en/product-results/download-historical-data-for-gdt-events/?cb=1464951368621'
        today = datetime.strftime(datetime.now(), '%Y_%m_%d')
        
        scraper = WebScraper('Chrome')
        scraper.open(url)
        time.sleep(5)
        
        scraper.click_button('class', 'btn-call-action')
        time.sleep(15)
        scraper.close()
        
        # convert to csv and move to output directory
        path = create_directory(WEB_GLOBALDAIRYTRADE_PATH,today)
        input_casein = pd.read_excel('%s/Trading Events Historical Data.xls' % DOWNLOAD_PATH, 'RenCas', skiprows = 9)
        input_casein.to_csv('%sTrading_Events_Casein_Historical_Data.csv' % (path), index=False)
        
        input_casein = pd.read_excel('%s/Trading Events Historical Data.xls' % DOWNLOAD_PATH, 'Butter', skiprows = 9)
        input_casein.to_csv('%sTrading_Events_Butter_Historical_Data.csv' % (path), index=False)
        
        input_casein = pd.read_excel('%s/Trading Events Historical Data.xls' % DOWNLOAD_PATH, 'Ched', skiprows = 9)
        input_casein.to_csv('%sTrading_Events_Ched_Historical_Data.csv' % (path), index=False)
        
        input_casein = pd.read_excel('%s/Trading Events Historical Data.xls' % DOWNLOAD_PATH, 'SMP', skiprows = 9)
        input_casein.to_csv('%sTrading_Events_SMP_Historical_Data.csv' % (path), index=False)
        
        input_casein = pd.read_excel('%s/Trading Events Historical Data.xls' % DOWNLOAD_PATH, 'WMP', skiprows = 9)
        input_casein.to_csv('%sTrading_Events_WMP_Historical_Data.csv' % (path), index=False)
    
        print 'Finish scraping at %s...' % datetime.now()
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['global_dairy_trade_price'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('weekly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['global_dairy_trade_price'],[success_msg]]
        save_error_to_log('weekly', msg_list)


if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
    

