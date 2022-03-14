'''
Created on 21 Apr 2015

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
    wscraper = WebScraper('Chrome')
    
    url = "http://epp.eurostat.ec.europa.eu/newxtweb/"
    
    wscraper.open(url)
    
    login_xpath = ".//*[@id='content']/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr/td[4]/div/a"
    
    wscraper.click_button('xpath', login_xpath)
    
    external_xpath = ".//*[@id='responsive-main-nav']/div[6]/a[2]"
    
    wscraper.click_button('xpath',external_xpath)
    
    email = "cosullivan@computing.dcu.ie"
    password = "DATASdcu1234#"
    
    wscraper.load_field('input', 'name', 'username', email)
    wscraper.load_field('input','name','password',password)
    
    submit_xpath = ".//*[@id='loginForm']/input[11]"
    
    wscraper.click_button('xpath',submit_xpath)
    
    completed_xpath = ".//*[@id='content']/table[1]/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr/td[12]/div/a"
    
    wscraper.click_button('xpath',completed_xpath)
    
    
    download_str = wscraper.find_element('xpath',".//*[@id='download0']").get_attribute('onclick')
    download_str = download_str.split("'")[1]
    
    wscraper.hover(".//*[@id='download0']")
    wscraper.click_button('xpath',".//*[@id='download0']")
    time.sleep(3)
    
    
    wscraper.hover(".//*[@id='selectAll1']")
    time.sleep(2)
    wscraper.click_button('xpath',".//*[@id='selectAll1']")
    
    wscraper.hover(".//*[@id='deletes1']")
    time.sleep(2)
    wscraper.click_button('xpath',".//*[@id='deletes1']")
    
    
    
    wscraper.accept_alert()
    
    
    time.sleep(10)
    
    wscraper.close()
    
    
    
    download_dir = DOWNLOAD_PATH + download_str
    
    
    dir_title = datetime.now().strftime('%Y_%m_%d')
    dir_path = '%spig_meat_trade\\' % WEB_EUROSTAT_PATH
    dir_path = create_directory(dir_path, dir_title)
    
    
    unzip(download_dir,dir_path)
    
    delete_file(download_dir)


if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)