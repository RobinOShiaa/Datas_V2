'''
Created on 20 Jan 2015

@author: Suzanne
This program only works correctly if your downloads folder has no .csv files in it at beginning of runtime
'''
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
    print 'Start scraping at %s...' % datetime.now()
    
    url = 'http://quickstats.nass.usda.gov/'

        # get the latest data date from DB
    dbm = DBManager(db_params[0], db_params[1], db_params[2], db_params[3])
    date_from = dbm.get_latest_date_record('select max(year) from usda_dairy_quickstats;')
    date_from = date_from[0]
    del dbm
    
    this_year = datetime.now().year
    usda_dairy_quickstats_path = create_directory(WEB_USDA_PATH, 'dairy_quickstats')
    today = datetime.strftime(datetime.now(),'%Y_%m_%d')
    
    for i in range(date_from, this_year + 1):
            
        wscraper = WebScraper('Chrome')
        wscraper.open(url)
        wscraper.web_driver.maximize_window()
         
        wscraper.click_button('xpath', '//*[text()="DAIRY"]')
        time.sleep(10)
            
        #wscraper.wait(20,'xpath', '//*[text()="NATIONAL"]')
        wscraper.click_button('xpath', '//*[text()="NATIONAL"]')
        
        #wscraper.click_button('xpath', '//*[text()="DAIRY"]')
            
            
        wscraper.wait(20,'xpath', '//*[text()="2014"]')
        wscraper.click_button('xpath', '//*[text()="'+str(i)+'"]')
            
        wscraper.wait(20,'xpath', '//*[text()="MONTHLY"]')
        wscraper.click_button('xpath', '//*[text()="MONTHLY"]')
            
    
        wscraper.click_button('id', 'submit001_label')
        wscraper.wait(20,'xpath', '//*[text()="Spreadsheet"]')
        wscraper.click_button('xpath', '//*[text()="Spreadsheet"]')   
        time.sleep(10)
            
        wscraper.close()
        print 'scraped '+str(i)

        output = find_csv_filenames(DOWNLOAD_PATH, suffix='.csv')

        for o in output:
            count=0
            os.rename(DOWNLOAD_PATH+'/'+o, '%s/%s/'+str(i)+str(count)+'.csv' % (usda_dairy_quickstats_path, today)) 
            count+=1
   
    print 'Finish scraping at %s...' % datetime.now()
    

if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)