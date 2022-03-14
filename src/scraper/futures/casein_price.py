'''
Created on 10 Mar 2015

@author: Suzanne
05/11/2015 ABANDONED
'''
import time
from datetime import datetime
#from datas.db.manager import DBManager
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import save_download_file, ROOT_PATH, create_directory
from datas.web.scraper import WebScraper
from datas.web.path import DOWNLOAD_PATH


def scrape(db_params):
    print 'Start scraping at %s...' % datetime.now()
    
    path = '%soutput_web\\futures\\' % ROOT_PATH
    today = datetime.strftime(datetime.now(), '%Y_%m_%d\\')
    
    scraper = WebScraper('Chrome')
#<<<<<<< HEAD
#<<<<<<< HEAD
    url= 'http://future.aae.wisc.edu/data/weekly_values/by_area/1615'
    scraper.open(url)
     
    scraper.click_button('link_text', 'Download data') #by default, pulls down only this year's data, no need to fiddle with dates in database til using loader
    time.sleep(20)
     
    scraper.close()
    new_path = create_directory(path, today)
    save_download_file(DOWNLOAD_PATH, '%sweekly_casein_rennet_price.csv' %(new_path))
#=======
#=======
#>>>>>>> server
    url='http://future.aae.wisc.edu/data/monthly_values/by_area/3574?tab=prices'
    #url= 'http://future.aae.wisc.edu/data/weekly_values/by_area/1615'
    scraper.open(url)
     
    #scraper.click_button('link_text', 'Download data') #by default, pulls down only this year's data, no need to fiddle with dates in database til using loader
    scraper.click_button('link_text', 'Show / Download Full Data')
    time.sleep(10)
    scraper.click_button('link_text', 'Year by Month')
     
    scraper.close()
    new_path = create_directory(path, today)
    save_download_file(DOWNLOAD_PATH, '%smonthly_casein_rennet_price.csv' %(new_path))
#<<<<<<< HEAD
#>>>>>>> f3e14f2d800be2ce2829ecd7364194ecc1f9bec7
#=======
#>>>>>>> server
    
    print 'Finish scraping at %s...' % datetime.now()


if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)