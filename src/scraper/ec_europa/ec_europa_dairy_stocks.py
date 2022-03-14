# -*- coding: utf-8 -*-
'''
Created on 13 Oct 2016

@author: Suzanne
'''
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import create_directory, save_error_to_log
from datas.web.path import WEB_EC_EUROPA_PATH
from datetime import datetime
import sys
import urllib
import subprocess
from bs4 import BeautifulSoup

def extract(dir_path, type, page_num, count):
    subprocess.call(['pdftohtml', '%sstocks.pdf' % dir_path, '-f', page_num, '-l',page_num]) # convert
    yearmonths = []
#     pattern=re.compile(r'[^0-9]{3}\s\d{2}$')
#     other_pattern= u"\xa0"
    eu_data = [type]
    
    with open(dir_path+'stockss.html','rb') as file:
        input = file.read()
    soup = BeautifulSoup(input)
    tags = soup.find_all('b')
    do_print=False # switch to start appending to list
    for tag in tags:
        if do_print==True:
            eu_data.append(tag.text.replace(' ','').replace(u"\xa0",''))
        if 'TOTAL' in tag.text:
            do_print = True
        if count==0:
            try:
                yearmonth = datetime.strptime(tag.text[:3],'%b')
                #yearmonth = pattern.search(tag.text).group()#datetime.strptime(tag.text,'%b %y')
            except:
                pass
            else:
                yearmonths.append(tag.text.replace(u"\xa0",' '))
    eu_data = eu_data[:-2]
    yearmonths = yearmonths[2:]
    with open(dir_path+'stocks.csv','ab') as out_file:
        if count==0:
            out_file.write(' ,'+','.join(yearmonths)+'\n')
        out_file.write(','.join(eu_data)+'\n')


def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()
        
        dir_path = '%sstocks' % WEB_EC_EUROPA_PATH
        today = datetime.strftime(datetime.now(), '%Y_%m_%d')
        dir_path = create_directory(dir_path, today)
        #dir_path='C:\\Users\\Suzanne\\workspace\\DATAS_Code\\output_web\\ec_europa\\stocks\\2016_10_14\\'
        url='http://ec.europa.eu/agriculture/market-observatory/milk/pdf/eu-stocks-butter-smp_en.pdf'
        #url='http://ec.europa.eu/agriculture/market-observatory/milk/latest-statistics/productions-stocks_en.htm'
        urllib.urlretrieve(url,dir_path+'stocks.pdf')
       
        extract(dir_path, 'SMP','14',0)
        extract(dir_path, 'Butter','16',1)
        extract(dir_path, 'Cheese','18',2)
        #extract(dir_path, 'Cheese','18',2)

        print 'Finished scraping at %s.' % datetime.now()
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['ec_europa_dairy_stocks.py'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('monthly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['ec_europa_dairy_stocks.py'],[success_msg]]
        save_error_to_log('monthly', msg_list)
        
if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)