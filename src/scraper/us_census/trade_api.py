'''
Created on 17 Jan 2017

@author: Suzanne
'''
from datas.web.scraper import WebScraper

def scrape():
    scraper = WebScraper('urllib2')
    exports_url = 'http://api.census.gov/data/timeseries/intltrade/exports?get=usda&key=9a398381359d637f63bc98a674667714fe75e04d&year=2016&month=01'
    scraper.open(exports_url)

if __name__ == '__main__':
    scrape()