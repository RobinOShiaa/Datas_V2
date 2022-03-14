'''
Created on 10 Jun 2016

@author: Suzanne
'''
from datas.web.scraper import WebScraper
from datetime import datetime
import sys
import time
from datas.web.path import DOWNLOAD_PATH, WEB_USDA_PATH
from datas.function.function import save_error_to_log, create_directory,\
    unzip, get_download_file_name
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD

def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()
        url = 'http://usda.mannlib.cornell.edu/MannUsda/viewDocumentInfo.do?documentID=1002'
        scraper = WebScraper('Chrome')
        scraper.open(url)
        scraper.click_button('xpath', '//*[@id="latest"]/div[3]/a/span')
        time.sleep(10)
        
        dir_title = datetime.now().strftime('%Y_%m_%d')
        dir_path = '%sincome_over_feed_costs\\' % WEB_USDA_PATH
        dest_path = create_directory(dir_path, dir_title)

        source_file = get_download_file_name(DOWNLOAD_PATH)
        unzip(source_file, dest_path)
        
        print 'Finished scraping at %s.' % datetime.now()
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['usda.income_over_feed_costs.py'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('monthly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['usda.income_over_feed_costs.py'],[success_msg]]
        save_error_to_log('monthly', msg_list)
        
if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
