'''
Created on 18 Mar 2016

@author: Suzanne
abandoned
'''
from datetime import datetime
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import create_directory, chunck_list
from datas.web.scraper import WebScraper
from datas.web.path import WEB_OECD_PATH
import time

identifier = '??'
year = '' #TODO: get year
filters = ''
url = 'http://stats.oecd.org/sdmx-json/data/'+identifier+'/.'+filters+'/all?startTime='+year+'-Q1'
scraper = WebScraper('Chrome')
scraper.open(url)