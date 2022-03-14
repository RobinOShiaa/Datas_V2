'''
Created on 8 Nov 2016

@author: Suzanne
'''
import time
from datetime import datetime
import sys
import os
from bs4 import BeautifulSoup
from datas.function.function import save_error_to_log
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import get_file_name, create_directory
from datas.web.scraper import WebScraper
from datas.web.path import DOWNLOAD_PATH, WEB_ZMB_PATH
import pandas as pd
import urllib2

def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()
        
        today = datetime.strftime(datetime.now(), '%Y_%m_%d\\')
        dir_path = create_directory(WEB_ZMB_PATH, today)
        
        url='http://www.milk.de/'
        html = urllib2.urlopen(url).read()
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find('table')
        row = table.find_all('tr')[2]
        week = table.find_all('tr')[1].find_all('td')[0]#.text#.split('.')[0]#.lstrip()
        week = week.text.split('.')[0].lstrip()
        data = row.find_all('td')[1].text
        
        with open(dir_path + 'german_milk_delivery_tonnes.csv','wb') as out_file:
            out_file.write(week+','+data)

        print 'Finish scraping at %s.' % datetime.now()

    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['zmb.german_milk_production_weekly.py'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('weekly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['zmb.german_milk_production_weekly.py'],[success_msg]]
        save_error_to_log('weekly', msg_list)
        
if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)