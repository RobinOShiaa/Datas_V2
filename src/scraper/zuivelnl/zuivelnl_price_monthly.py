'''
Created on 22 Jun 2015

@author: Suzanne
'''
from datetime import datetime
import time
import subprocess
import urllib
from datas.web.scraper import WebScraper
from datas.web.path import WEB_ZUIVELNL_PATH
from datas.function.function import create_directory
from datas.db.manager import DBManager, RAW_DB_NAME, TEST_DB_NAME, USERNAME, PASSWORD, HOST


def scrape():

    scraper = WebScraper('Chrome')
    url='http://www.zuivelnl.org/wp-content/uploads/2015/06/Prijzen-2015-en-2014.pdf'
    scraper.open(url) 
    #scraper.web_driver.maximize_window()
    
    elems = scraper.find_element('xpath', '*//html')
    print elems
    
    for e in elems:
        print e.text
        
    scraper.close()

    dir_path = '%sprices' % WEB_ZUIVELNL_PATH
    today = datetime.strftime(datetime.now(), '%Y_%m_%d')
    dir_path = create_directory(dir_path, today)
    url='http://www.zuivelnl.org/wp-content/uploads/2015/06/Prijzen-2015-en-2014.pdf'
    urllib.urlretrieve(url,dir_path+'prices.pdf')
    #subprocess.call(['pdftohtml', '%sprices.pdf' % dir_path, '-f', '16' ]) # convert
#     scraper = WebScraper('Chrome')
#     url='http://www.zuivelnl.org/wp-content/uploads/2015/06/Prijzen-2015-en-2014.pdf'
#     scraper.open(url) 
#     #scraper.web_driver.maximize_window()
#     
#     elems = scraper.find_element('xpath', '*//html')
#     print elems
#     
#     for e in elems:
#         print e.text
#         
#     scraper.close()
        
if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape()