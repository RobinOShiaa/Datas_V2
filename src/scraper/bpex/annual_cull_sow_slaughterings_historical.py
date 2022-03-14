'''
Created on 20 Nov 2014

@author: Suzanne
4. annual_cull_sow_slaughterings_historical.xls year 2009 data incorrect
'''
import os
import time
from datetime import datetime
from selenium import webdriver
from datas.db.manager import DBManager
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.web.path import WEB_BPEX_PATH
from datas.function.function import chunck_list, create_directory
import BeautifulSoup
import urllib2


def scrape(db_params):
    print 'Start scraping at %s...' % datetime.now()
    
    url = 'http://pork.ahdb.org.uk/prices-stats/production/gb-slaughterings/annual-cull-sow/'
    data = []
    
    '''Start scrape'''
    req = urllib2.Request(url)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page)
    table = soup.find("table")
    
    rows = table.findAll('tr')
    for tr in rows[2:]:
        cols = tr.findAll('td')
        for td in cols:
            data.append(td.text.encode('ascii', 'ignore').replace(',', '').replace('&nbsp;',' '))
    
    dir = create_directory(WEB_BPEX_PATH + 'slaughtering/historical_annual', str(datetime.now().date()))
    file_path = '%sannual_cull_sow_slaughterings_historical.csv' % dir
            
    out_file = open(file_path, 'w')
    out_file.write('url, %s' % (url))
    out_file.write('\n')
    data = chunck_list(data, 2)
         
    for d in data:
        out_file.write(', '.join(d))
        out_file.write('\n')
             
    out_file.close()
    
    '''Alternative to download file'''        
    # source_file = '/users/suzanne/downloads/GBcullsowslaughterings_000.xls'
    # dest_file = BPEX_PATH + 'historical/annual_cull_sow_slaughterings_historical.xls'
    # browser = webdriver.Chrome()
    # browser.get(url)  
    # time.sleep(2)     
    # element = browser.find_element_by_link_text('Click here to download excel')
    # element.click() 
    # time.sleep(3)
    # os.rename(source_file, dest_file)
    # browser.quit()
    
    print 'Finished...'


if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)