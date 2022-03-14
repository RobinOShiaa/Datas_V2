'''
Created on 18 May 2015

@author: Conor O'Sullivan
'''
import os
import time
from datetime import datetime
from datas.web.path import WEB_EUROSTAT_PATH
from datas.db.manager import DBManager
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.web.scraper import WebScraper
from datas.web.path import DOWNLOAD_PATH
from datas.function.function import create_directory, unzip,delete_file

def scrape(db_params):
    print 'Start scraping at %s...' % datetime.now()
    
    '''pig download'''
    wscraper = WebScraper('Chrome')
    url = "http://epp.eurostat.ec.europa.eu/newxtweb/"
    wscraper.open(url)
     
    email = "cosullivan@computing.dcu.ie"
    password = "DATASdcu1234#"
     
    wscraper.login_eurostat_query(email, password)
 
    completed_xpath = ".//*[@id='content']/table[1]/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr/td[12]/div/a"
    wscraper.click_button('xpath',completed_xpath)
    time.sleep(4)    
    download_str = wscraper.find_element('xpath',".//*[@id='download0']").get_attribute('onclick').split("'")[1]
     
    wscraper.click_button('xpath',".//*[@id='download0']")
    time.sleep(5)
     
    wscraper.close()
 
    download_dir = DOWNLOAD_PATH + download_str
    dir_title = datetime.now().strftime('%Y_%m_%d')
    dir_path = '%spig_meat_trade\\' % WEB_EUROSTAT_PATH
    dir_path = create_directory(dir_path, dir_title)
    unzip(download_dir,dir_path)
    delete_file(download_dir)
    
    '''dairy download'''
    wscraper = WebScraper('Chrome')
    wscraper.open(url)
    wscraper.login_eurostat_query(email, password)

    wscraper.click_button('xpath',".//*[@id='content']/table[1]/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr/td[12]/div/a") # Completed works

    download_str = wscraper.find_element('xpath',".//*[@id='download2']").get_attribute('onclick').split("'")[1]
    
    #wscraper.hover('xpath',".//*[@id='download2']")
    wscraper.click_button('xpath',".//*[@id='download2']")
    time.sleep(3)
    
    wscraper.delete_eurostat_queries()

    wscraper.close()

    download_dir = DOWNLOAD_PATH + download_str
    dir_title = datetime.now().strftime('%Y_%m_%d')
    dir_path = '%sdairy_trade\\' % WEB_EUROSTAT_PATH
    dir_path = create_directory(dir_path, dir_title)
    unzip(download_dir,dir_path)
    delete_file(download_dir)
    
    print 'finished scraping at %s...' % datetime.now()

if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)