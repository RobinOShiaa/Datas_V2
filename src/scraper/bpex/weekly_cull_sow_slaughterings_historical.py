'''
Created on 20 Nov 2014

@author: Suzanne
'''

import os
import time
from datetime import datetime
from datas.db.manager import DBManager
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.web.path import WEB_BPEX_PATH
from datas.web.scraper import *


def scrape(db_params):
    print 'Start scraping at %s...' % datetime.now()
    
    url = 'http://www.bpex.org.uk/prices-facts-figures/production/PublishedSSI.aspx'
    
    source_file = '/users/suzanne/downloads/Export.csv'
    dest_file = WEB_BPEX_PATH + 'historical/weekly_cull_sow_slaughterings_historical.csv'
    
    scraper = WebScraper('Chrome') 
    scraper.open(url)       
    scraper.click_button('link_text','Download as Excel')
    time.sleep(3)
    os.rename(source_file, dest_file)
    scraper.close()

    print 'Finish scraping at %s.' % datetime.now()


if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)