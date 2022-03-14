'''
Created on 11 Mar 2015

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


def resume_scrape(url, file_path):
    try:
        wscraper = WebScraper('urllib2')
        wscraper.download_file(url, file_path)
        wscraper.close()
    except Exception, e:
        print 'resume_scrape() error: %s' % e
        return False
    else:
        return True


def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()
        
        # get the latest data date from DB
        dbm = DBManager(db_params[0], db_params[1], db_params[2], db_params[3])
        '''sql = ('select max(year) as max_date from usda_pig_crops '
               'group by region, data_item order by max_date asc limit 1;')'''
        sql = ('select max(year) as max_year from usda_pig_crops '
               'group by data_item order by max_year asc limit 1;')
        date_from = dbm.get_latest_date_record(sql)
        year_from = str(date_from[0])
        del dbm
        
        # url checked, correct
        url = 'http://quickstats.nass.usda.gov/api/api_GET/?key=872CA637-FC03-33B0-8917-3E1972173A4A&format=CSV&source_desc=SURVEY&sector_desc=ANIMALS%20%26%20PRODUCTS&group_desc=LIVESTOCK&commodity_desc=HOGS&statisticcat_desc=PIG%20CROP&freq_desc=MONTHLY&year__GE='
        url += year_from
        
        dir_title = datetime.now().strftime('%Y_%m_%d')
        dir_path = '%spig_crops\\' % WEB_USDA_PATH
        dest_path = create_directory(dir_path, dir_title)
        file_path = '%spig_crops.csv' % dest_path
        
        counter = 0
        while not resume_scrape(url, file_path):
            if counter >= 5:
                raise Exception('web communication error, exceeds max number of attempts, stop scraping')
            else:
                print 'at counter %s scraping %s...' % (counter, url)
                counter += 1
        
        print 'Finish scraping at %s.' % datetime.now()
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['usda.pig_crops.py'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        save_error_to_log('monthly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['usda.pig_crops.py'],[success_msg]]
        save_error_to_log('monthly', msg_list)
    

if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
    
