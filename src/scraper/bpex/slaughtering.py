'''
Created on 11 Nov 2014

@author: Suzanne

08/01/2015(Wenchong): Automation completed.
27/01/2015(Wenchong): Website rebuilt, adapted the changes.
11/02/2015(Wenchong): Fixed sql query to get the correct date as a new scraping point.
Note that this scraper must use chrome as the browser, not firefox
'''

import pandas as pd
import time
import os
from datetime import datetime
from datas.db.manager import DBManager
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import create_directory
import sys
from datas.function.function import save_error_to_log
from datas.web.path import DOWNLOAD_PATH
from datas.web.path import WEB_BPEX_PATH
from datas.web.scraper import WebScraper


def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()
        
        # get the latest data date from DB
        dbm = DBManager(db_params[0], db_params[1], db_params[2], db_params[3])
        sql = ('select max(week_end_date) as max_date from bpex_weekly_slaughtering '
               'group by member_state, type order by max_date asc limit 1;')
        date_from = dbm.get_latest_date_record(sql)
        date_from = date_from[0]
        del dbm
        
        url = 'http://www.bpex.org.uk/prices-stats/production/eu-weekly-pig-slaughterings/'
        
        # store the dataset into the file
        dir_title = datetime.now().strftime('%Y_%m_%d')
        dir_path = '%sslaughtering\\' % WEB_BPEX_PATH
        dir_path = create_directory(dir_path, dir_title)
        file_path = '%seu_weekly_slaughter.xls' % dir_path
        
        wscraper = WebScraper('Chrome')
        wscraper.open(url)
        wscraper.click_button('xpath', '//a[@title="EU Weekly Pig Slaughterings"]')
        time.sleep(3)
        
        os.chdir(DOWNLOAD_PATH)
        files = filter(os.path.isfile, os.listdir(DOWNLOAD_PATH))
        files = [os.path.join(DOWNLOAD_PATH, f) for f in files] # add path to each file
        files.sort(key=lambda x: os.path.getmtime(x))
        newest_file = files[-1]
        
        
        xls = pd.ExcelFile(newest_file)
        df = xls.parse('Clean Pigs', index_col=None, na_values=['NA'])
        df.to_csv('%sclean pigs_head.csv' % dir_path)
        
        df = xls.parse('Sows', index_col=None, na_values=['NA'])
        df.to_csv('%ssows_head.csv' % dir_path)
        
        wscraper.close()
        
        print 'Finish scraping at %s.' % datetime.now()
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['bpex.slaughtering.py'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('weekly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['bpex.slaughtering.py'],[success_msg]]
        save_error_to_log('weekly', msg_list)


if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
    
