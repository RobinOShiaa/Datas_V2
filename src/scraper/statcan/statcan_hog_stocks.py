'''
Created on 3 Apr 2015

@author: Suzanne
'''
import sys
import os
from datas.function.function import save_error_to_log
from datetime import datetime
import time
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.web.scraper import WebScraper
from datas.web.path import WEB_STATCAN_PATH, DOWNLOAD_PATH
from datas.function.function import create_directory, unzip

def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()
    
        today = datetime.strftime(datetime.now(), '%Y_%m_%d')
        dir_path = create_directory(WEB_STATCAN_PATH+'hog_stocks\\', today)
        url = ('http://www5.statcan.gc.ca/access_acces/alternative_alternatif?l=eng&keng=11.8&kfra=11.8&teng='
               'Download%20file%20from%20CANSIM&tfra=Fichier%20extrait%20de%20CANSIM&loc=http://www20.statcan.'
               'gc.ca/tables-tableaux/cansim/csv/00030103-eng.zip&dispext=CSV')
    
        scraper = WebScraper('Chrome')
        scraper.open(url)
        
        scraper.click_button('xpath', '//ul[@class="noBullet"]/li/a')
        time.sleep(5)
        
        scraper.close()
        
        unzip(DOWNLOAD_PATH+'\\00030103-eng.zip', dir_path)
        
        print "Finished at %s." % datetime.now()
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['statcan_hog_stocks'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('monthly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['statcan_hog_stocks'],[success_msg]]
        save_error_to_log('monthly', msg_list)


if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
    
