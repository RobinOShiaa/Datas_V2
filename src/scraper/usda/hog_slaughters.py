'''
Created on 10 Mar 2015

@author: Wenchong

12/03/2015(Wenchong): url checked, correct
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


def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()
        
        # get the latest data date from DB
        dbm = DBManager(db_params[0], db_params[1], db_params[2], db_params[3])
        sql = ('select max(year) as max_year from usda_hog_slaughters '
               'group by data_item order by max_year asc limit 1;')
        date_from = dbm.get_latest_date_record(sql)
        year_from = str(date_from[0])
        del dbm
        
        # weekly data
        url = 'http://quickstats.nass.usda.gov/api/api_GET/?key=872CA637-FC03-33B0-8917-3E1972173A4A&format=CSV&source_desc=SURVEY&sector_desc=ANIMALS%20%26%20PRODUCTS&group_desc=LIVESTOCK&commodity_desc=HOGS&statisticcat_desc=SLAUGHTERED&year__GE='
        url = url + year_from + '&freq_desc=WEEKLY&short_desc=HOGS%2C%20SLAUGHTER%2C%20COMMERCIAL%2C%20FI%20%2D%20SLAUGHTERED%2C%20MEASURED%20IN%20'
        
        measures = {'head':'HEAD', 'lb per head, dressed basis':'LB%20%2F%20HEAD%2C%20DRESSED%20BASIS'}
        #this_year = datetime.now().year
        
        wscraper = WebScraper('urllib2')
        
        dir_title = datetime.now().strftime('%Y_%m_%d')
        dir_path = '%shog_slaughters\\' % WEB_USDA_PATH
        dest_path = create_directory(dir_path, dir_title)       
        
        
        for key in measures:
            print 'scraping %s...' % (url + measures[key])
            file_path = '%shog_slaughters_%s.csv' % (dest_path, key)
            wscraper.download_file(url + measures[key], file_path)
        
        wscraper.close()
        
        print 'Finish scraping at %s.' % datetime.now()
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['usda.hog_slaughters.py'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('weekly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['usda.hog_slaughters.py'],[success_msg]]
        save_error_to_log('weekly', msg_list)
    

if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
    
