'''
Created on 20 May 2015

@author: Conor O'Sullivan
'''
import sys
from datas.function.function import save_error_to_log
import time
from datetime import datetime
import os
from os import listdir
from datas.web.path import WEB_USDA_PATH, DOWNLOAD_PATH
from datas.web.scraper import WebScraper
from datas.function.function import create_directory
from datas.db.manager import DBManager, RAW_DB_NAME, HOST, USERNAME, PASSWORD

def find_csv_filenames( path_to_dir, suffix=".csv" ):
    filenames = listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]

def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()
    
        url = 'http://quickstats.nass.usda.gov/'

        wscraper = WebScraper('Chrome')
        wscraper.open(url)
        wscraper.web_driver.maximize_window()
        
        wscraper.click_button('xpath', '//*[text()="DAIRY"]')
        time.sleep(10)
        
        #wscraper.click_button('xpath', '//*[text()="BUTTER"]')
        #time.sleep(10)
        butter_xpath = '//*[text()="BUTTER"]'
        cheese_xpath = '//*[text()="CHEESE"]'
        milk_xpath = '//*[text()="MILK"]'
        
        commodity_lst = [butter_xpath,cheese_xpath,milk_xpath]
        
        wscraper.click_multiple(commodity_lst)
        time.sleep(10)
        
        wscraper.click_button('xpath', '//*[text()="STOCKS"]')
        time.sleep(10)
        
        #wscraper.click_button('xpath', ".//*[@id='year']/option[1]")
        
        current_year_xpath = ".//*[@id='year']/option[1]"
        last_year_xpath = ".//*[@id='year']/option[2]"
        
        year_lst = [current_year_xpath,last_year_xpath]
        
        wscraper.click_multiple(year_lst)    
        
        wscraper.click_button('xpath', ".//*[@id='submit001']")
        
        time.sleep(2)
        
        #wscraper.click_button('xpath',".//*[@id='rowCount2']/a[2]")
        csv_files = find_csv_filenames(DOWNLOAD_PATH, suffix='.csv')
        
        for csv_file in csv_files:
            os.remove(DOWNLOAD_PATH + csv_file)
    
        
        wscraper.wait(20,'xpath', '//*[text()="Spreadsheet"]')
        wscraper.click_button('xpath', '//*[text()="Spreadsheet"]')   
        time.sleep(10)
        
        output = find_csv_filenames(DOWNLOAD_PATH, suffix='.csv')
        
        
        dir_title = datetime.now().strftime('%Y_%m_%d')


        dir_path = '%sdairy_quickstats' % WEB_USDA_PATH

        dir_path = create_directory(dir_path, dir_title)
        file_path = dir_path + 'dairy_quickstats_cold_storage.csv'
        if not os.path.exists(file_path):    
            os.rename(DOWNLOAD_PATH + output[0],file_path) 
    
        wscraper.close()    

        print 'Finish scraping at %s.' % datetime.now()
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['usda.dairy_quickstats_cold_storage.py'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        save_error_to_log('monthly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['usda.dairy_quickstats_cold_storage.py'],[success_msg]]
        save_error_to_log('monthly', msg_list)
    
if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)

