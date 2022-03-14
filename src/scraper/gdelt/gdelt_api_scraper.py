'''
Created on 14 Oct 2016

@author: Suzanne
'''
import requests
import csv
import sys
from bs4 import BeautifulSoup
from urllib import urlretrieve
from urlparse import urljoin
from datetime import datetime
from datas.db.manager import DBManager
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import create_directory, save_error_to_log, unzip
from datas.web.path import WEB_GDELT_PATH
from datas.web.scraper import WebScraper

def scrape(db_params):
    print 'Start scraping at %s...' % datetime.now()

    dir_title = datetime.now().strftime('%Y_%m_%d')
    dir_path = '%sgdelt_data\\' % WEB_GDELT_PATH
    newdir_path = create_directory(dir_path, dir_title)
    links_url = 'http://api.gdeltproject.org/api/v1/search_ftxtsearch/search_ftxtsearch?query=agriculture&output=artimglist&dropdup=false&trans=googtrans'
    browser = WebScraper('Chrome')
    browser.web_driver.maximize_window()
    browser.open(links_url)
    r = requests.get(url=links_url, verify=False)
    links_soup = BeautifulSoup(r.content, "html.parser")
    all_links = links_soup.find_all('a')
    urls = []
    for link in all_links:
        urls.append(link.get('href'))
    out_file = open(newdir_path + '\\gdelt_api_agriculture.csv', 'a')
    i = 0
    while i < len(urls):
        out_file.write(urls[i] + ",\n")
        i += 2
    browser.close()

    
if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
