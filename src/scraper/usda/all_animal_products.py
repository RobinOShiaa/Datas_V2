'''
Created on 1 Apr 2015

@author: Wenchong
'''
import sys
import os
from datas.function.function import save_error_to_log
from datetime import datetime
from datas.db.manager import DBManager
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import create_directory
from datas.web.path import WEB_USDA_PATH
from datas.web.scraper import WebScraper

def resume_scrape(counter):
    return


def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()
        
        # get the latest data date from DB
        dbm = DBManager(db_params[0], db_params[1], db_params[2], db_params[3])
        #TODO(Wenchong): 01/04/2015 need to create table for this data, sql needs to be adjusted
        sql = ('select max(week_ending) as max_year from usda_all_animal_products '
               'group by commodity order by max_year desc limit 1;')
        date_from = dbm.get_latest_date_record(sql)
        year_from = str(date_from[0].year)
        del dbm
        
        # url for historical data before year 2000
        #url = 'http://quickstats.nass.usda.gov/api/api_GET/?key=872CA637-FC03-33B0-8917-3E1972173A4A&format=CSV&source_desc=SURVEY&sector_desc=ANIMALS %26 PRODUCTS&agg_level_desc=NATIONAL&freq_desc=WEEKLY&year__LT=2000'
        # url for historical data from 2000 to now (01/04/2015)
        #url = 'http://quickstats.nass.usda.gov/api/api_GET/?key=872CA637-FC03-33B0-8917-3E1972173A4A&format=CSV&source_desc=SURVEY&sector_desc=ANIMALS %26 PRODUCTS&agg_level_desc=NATIONAL&freq_desc=WEEKLY&year__GE=2000'
        
        # url checked, correct
        url = 'http://quickstats.nass.usda.gov/api/api_GET/?key=872CA637-FC03-33B0-8917-3E1972173A4A&format=CSV&source_desc=SURVEY&sector_desc=ANIMALS%20%26%20PRODUCTS&agg_level_desc=NATIONAL&freq_desc=WEEKLY&year__GE='
        url += year_from
        wscraper = WebScraper('urllib2')
        dir_title = datetime.now().strftime('%Y_%m_%d')
        dir_path = '%sall_animal_products\\' % WEB_USDA_PATH
        dest_path = create_directory(dir_path, dir_title)
        file_path = '%sall_animal_products.csv' % dest_path
        
        #print 'scraping %s...' % (url)
        
        wscraper.download_file(url, file_path)
        
        print 'Finish scraping at %s.' % datetime.now()
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['usda.all_animal_products.py'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        save_error_to_log('weekly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['usda.all_animal_products.py'],[success_msg]]
        save_error_to_log('weekly', msg_list)
    

if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
    
