'''
Created on 3 Dec 2014

@author: Wenchong
ABANDONED
'''


import time
from datetime import datetime
from selenium import webdriver
from datas.function.function import *
from datas.web.path import DOWNLOAD_PATH
from datas.web.path import WEB_USDA_PATH
from datas.web.scraper import WebScraper


if __name__ == '__main__':
    
    file_name = 'dairy_data'
    dir_title = datetime.now().strftime('%Y_%m_%d')
    dest_path = '%s%s\\' % (WEB_USDA_PATH, file_name)
    dest_path = create_directory(dest_path, dir_title)
    
    url = 'http://www.ers.usda.gov/data-products/dairy-data.aspx'
    
    # open parent window by url
    wscraper = WebScraper('Chrome')
    wscraper.open(url)
    time.sleep(10)
    
    # save file to the given file dest_file
    print 'start downloading...'
    links = wscraper.find_elements('xpath', '//a[@alt="Download File"]')
    
    for link in links:
        link.click()
        time.sleep(5)
        
        move_download_file(DOWNLOAD_PATH, dest_path)
        time.sleep(2)
    
    # save url to the given folder dest_path
    save_to_file(dest_path + 'bookmark_url.txt', [['url', url]])
    
    wscraper.close()
    
    print 'finished...'
    


