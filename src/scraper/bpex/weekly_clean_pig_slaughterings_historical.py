'''
Created on 20 Nov 2014

@author: Suzanne
'''
import os
import time
from datetime import datetime
from datas.db.manager import DBManager
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.web.scraper import * 
from datas.web.path import WEB_BPEX_PATH


def scrape(db_params):
    print 'Start scraping at %s...' % datetime.now()
    
    url = 'http://www.bpex.org.uk/prices-facts-figures/production/GBCleanPigSlaughterings.aspx'
    
    source_file = '/users/suzanne/downloads/Export.xls'
    dest_file = WEB_BPEX_PATH + 'historical/weekly_clean_pig_slaughterings_historical.xls'
    
    scraper = WebScraper('Firefox')
    scraper.open(url)  
    time.sleep(2)
    scraper.load_field('select','id', 'ddlDuration', '5')
    element = scraper.find_element('id', 'lnkbtnExportToCsv')
    element.click() 
    time.sleep(3)
    os.rename(source_file, dest_file)
    scraper.close()
    
    print 'Finish scraping at %s.' % datetime.now()


if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)