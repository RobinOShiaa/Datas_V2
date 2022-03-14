'''
Created on 2 Nov 2015

@author: Suzanne
'''
import sys
import os
from datas.function.function import save_error_to_log
from selenium import webdriver
import time
from datetime import datetime
from datas.db.manager import DBManager
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import unzip
from datas.web.path import WEB_USDA_PATH, DOWNLOAD_PATH


def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()
        
        # get the latest data date from DB
        dbm = DBManager(db_params[0], db_params[1], db_params[2], db_params[3])
        sql = ('select max(market_yearmonth) as max_date from usda_psd_grain '
               'group by type order by max_date asc limit 1;')
        date_from = dbm.get_latest_date_record(sql)
        #date_from = ['200001','']
        date_from = datetime.strptime(date_from[0], '%Y%m').date()
        del dbm
        
        url = 'http://apps.fas.usda.gov/psdonline/psdDownload.aspx'
        browser = webdriver.Chrome()
        browser.get(url)
        
        # get the last updated date from website
        last_updated_date = browser.find_element_by_xpath('//td[contains(text(), "Grains")]/..//td[@align="right"]').text
        last_updated_date = datetime.strptime(last_updated_date, '%m/%d/%Y').date()
        
        # don't download file if the file isn't updated
        if date_from > last_updated_date:
            browser.quit()
            print 'No new data found, terminated at %s...' % datetime.now()
            return
        
        file = browser.find_element_by_link_text('psd_grains_pulses_csv.zip').click()
        time.sleep(8)
        browser.quit()
        
        today = datetime.now().strftime("%Y_%m_%d")
        src_file = DOWNLOAD_PATH+'\\psd_grains_pulses_csv.zip'
        dest_dir = WEB_USDA_PATH+'psd_grain\\'+today
        unzip(src_file, dest_dir)

        print 'Finish scraping at %s.' % datetime.now()

    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['usda.psd_grain.py'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('monthly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['usda.psd_grain.py'],[success_msg]]
        save_error_to_log('monthly', msg_list)


if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
    
