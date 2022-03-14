'''
Created on 19 Jan 2016

@author: Suzanne
'''
import pandas as pd
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datetime import datetime
from datas.function.function import save_error_to_log
#import os
from datas.web.scraper import WebScraper
from datas.web.path import WEB_AUS_BUREAU_STATS_PATH, DOWNLOAD_PATH
import time
import sys
from datas.function.function import move_download_file, create_directory,\
    get_download_file_name, delete_file

def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()
        #'http://www.abs.gov.au/ausstats/abs@.nsf/mf/7218.0.55.001'
        url = 'http://www.abs.gov.au/AUSSTATS/abs@.nsf/DetailsPage/7218.0.55.001Nov%202015?OpenDocument#Time'
        today = datetime.now().strftime('%Y_%m_%d')
        dir_path = create_directory(WEB_AUS_BUREAU_STATS_PATH, today)
        scraper = WebScraper('Chrome')
        scraper.open(url)
        #xpath = '//*[@id="details"]/table/tbody/tr[@class="listentry"]'
        #rows = scraper.find_elements('xpath', xpath)
        #print len(rows)
        for i in xrange(4,10):
            product_name = scraper.find_element('xpath', '//*[@id="details"]/table/tbody/tr[%s]' % i).text.split('- ')[1].replace(' ','_').replace(':','')
            #print product_name
            scraper.click_button('xpath', '//*[@id="details"]/table/tbody/tr[%s]/td[2]/a[1]/img' % i)
            time.sleep(10)
            
            filename = get_download_file_name(DOWNLOAD_PATH)
            filename = filename.split('\\')[-1]
        
            try:
                move_download_file(DOWNLOAD_PATH, dir_path)
            except:
                continue
            
            df = pd.read_excel(dir_path+filename, 'Data1')
            df.to_csv('%s%s.csv' % (dir_path, product_name), index=False)
            delete_file(dir_path+filename)

        scraper.close()
        print 'Finished scraping at %s.' % datetime.now()

    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['aus_livestock_slaughters.py'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('monthly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['aus_livestock_slaughters.py'],[success_msg]]
        save_error_to_log('monthly', msg_list)
    
if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)

