'''
Created on 7 Jan 2015

@author: Suzanne

07/01/2015(Suzanne): This programme only works correctly if your downloads folder
has no .csv files in it at beginning of runtime.
03/02/2015(Wenchong): Fixed a few bugs.
03/02/2015(Wenchong): Automation completed.
12/02/2015(Wenchong): Fixed sql query to get the correct date as a new scraping point.
'''

import time
from datetime import datetime
from datas.db.manager import DBManager
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import create_directory
from datas.function.function import save_download_file
from datas.web.path import DOWNLOAD_PATH
from datas.web.path import WEB_USDA_PATH
from datas.web.scraper import WebScraper


def scrape():
    print 'Start scraping at %s...' % datetime.now()
    
    # get the latest data date from DB
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    dbm = DBManager(db_params[0], db_params[1], db_params[2], db_params[3])
    sql = ('select max(year) as max_date from usda_pork_production_stocks '
           'group by data_item order by max_date asc limit 1;')
    date_from = dbm.get_latest_date_record(sql)
    year_from = int(date_from[0][:4])
    del dbm
    print year_from
    
    url = 'http://quickstats.nass.usda.gov/'
    this_year = datetime.now().year
    
    dir_title = datetime.now().strftime('%Y_%m_%d')
    dir_path = '%spork_production_stocks\\' % WEB_USDA_PATH
    dest_path = create_directory(dir_path, dir_title)
    
    # since there are more problems selecting weeks, we simply download
    # all data in this year, then the latest data will be picked up
    # in the db loader
    for i in range(year_from, this_year + 1):
        wscraper = WebScraper('Chrome')
        wscraper.open(url)
        wscraper.web_driver.maximize_window()
        
        # select commodity
        wscraper.wait(20, 'xpath', '//*[text()="PORK"]')
        wscraper.click_button('xpath', '//*[text()="PORK"]')
        
        # wait for all data items to show up
        wscraper.wait(20,'xpath', '//*[text()="PORK, SLAUGHTER - PRODUCTION, MEASURED IN LB"]')
        
        # select year
        wscraper.wait(30, 'xpath', '//*[text()="2014"]')
        wscraper.click_button('xpath', '//*[text()="'+str(i)+'"]')
        
        # select period type
        try:
            wscraper.wait(20,'xpath', '//*[text()="POINT IN TIME"]')
        except Exception, e:
            print 'pork_production_stocks.scrape() error: datasets not ready yet for year %s' % i
            return
        wscraper.click_button('xpath', '//*[text()="POINT IN TIME"]')
        
        # click submit button
        time.sleep(2)
        wscraper.click_button('id', 'submit001_label')
        
        # download file
        wscraper.wait(20,'xpath', '//*[text()="Spreadsheet"]')
        wscraper.click_button('xpath', '//*[text()="Spreadsheet"]')   
        time.sleep(5)
        
        wscraper.close()
        
        print 'scraped ' + str(i)
        
        save_download_file(DOWNLOAD_PATH, '%s%s.csv' % (dest_path, str(i)))
    # end of for-loop      
    
    print 'Finish scraping at %s...' % datetime.now()
    
if __name__ == '__main__':
    scrape()
