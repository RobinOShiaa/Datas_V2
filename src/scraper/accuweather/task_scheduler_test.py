'''
Created on 18 Nov 2015

@author: Sue
'''
from datas.function.function import create_directory
from datetime import datetime
from datas.web.path import WEB_ACCUWEATHER_PATH
from scraper.bordbia.cereal_price import scrape

def create():
    
    dir_path =  WEB_ACCUWEATHER_PATH
    today = datetime.strftime(datetime.now(), '%Y_%m_%d')
    dir_title = today
    test_dir = create_directory(dir_path, dir_title)
    
    scrape()

if __name__ == '__main__':
    create()