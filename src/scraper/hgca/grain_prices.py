'''
Created on 24 Mar 2015

@author: Suzanne
'''
import time
import sys
import os
from datas.function.function import save_error_to_log
from datetime import datetime
from datas.db.manager import DBManager, RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.web.path import WEB_HGCA_PATH, DOWNLOAD_PATH
from datas.web.scraper import WebScraper
from datas.function.function import create_directory, save_download_file

def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()
        
        # get the latest data date from DB
        dbm = DBManager(db_params[0], db_params[1], db_params[2], db_params[3])
        sql = ('select max(date) from hgca_grain_price;')
        date_from = dbm.get_latest_date_record(sql)
        try:
            date_from = datetime.strftime(date_from[0], '%Y')
        except:
            date_from = '1987'
            
        del dbm
        
        
        today = datetime.strftime(datetime.now(), '%Y_%m_%d')
        path = create_directory('%sgrain_prices' % WEB_HGCA_PATH, today)
        
        scraper = WebScraper('Chrome')
        url = 'http://data.hgca.com/demand/physical.asp'
        scraper.open(url)
        
        commodities = scraper.get_dropdown_list('name', 'commodity')
        
        for commodity in commodities:
            scraper.load_field('select','name', 'commodity', commodity)
            countries = scraper.get_dropdown_list('name', 'country')
            for country in countries:
                scraper.load_field('select','name', 'country', country)
                scraper.load_field('select','name', 'from', date_from)
                scraper.click_button('name', 'csv')
                time.sleep(5)
                            
                save_download_file(DOWNLOAD_PATH, path+commodity+'_'+country+'.csv')
        
        scraper.close()
        
        print 'Finish scraping at %s...' % datetime.now()
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['hgca.grain_prices'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('weekly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['hgca.grain_prices'],[success_msg]]
        save_error_to_log('weekly', msg_list)


if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
    
