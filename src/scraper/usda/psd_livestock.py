'''
Created on 18 Nov 2014

@author: Suzanne

29/01/2015(Wenchong): Automation completed, but haven't tested the db part.
12/02/2015(Wenchong): Fixed sql query to get the correct date as a new scraping point.
'''
import sys
import os
from datas.function.function import save_error_to_log
import time
from datetime import datetime
#from itertools import groupby
from selenium import webdriver
from datas.db.manager import DBManager
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import create_directory
from datas.function.function import unzip
from datas.web.path import DOWNLOAD_PATH
from datas.web.path import WEB_USDA_PATH


def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()
        
        # TODO(Wenchong): 29/01/2015 need to add a last_updated_date column in the db
        # get the latest data date from DB
        dbm = DBManager(db_params[0], db_params[1], db_params[2], db_params[3])
        sql = ('select max(market_yearmonth) as max_date from usda_psd_livestock '
               'group by type order by max_date asc limit 1;')
        date_from = dbm.get_latest_date_record(sql)
        
        date_from = datetime.strptime(date_from[0], '%Y%m').date()
        del dbm
        
        url = 'http://apps.fas.usda.gov/psdonline/psdDownload.aspx'
        
        browser = webdriver.Chrome()
        
        '''Web scraping'''
        browser.get(url)
        
        # get the last updated date from website
        last_updated_date = browser.find_element_by_xpath('//td[contains(text(), "Livestock")]/..//td[@align="right"]').text
        last_updated_date = datetime.strptime(last_updated_date, '%m/%d/%Y').date()
        
        # don't download file if the file isn't updated
        if date_from > last_updated_date:
            browser.quit()
            print 'No new data found, terminated at %s...' % datetime.now()
            return
        
        dir_title = datetime.now().strftime('%Y_%m_%d')
        dir_path = '%spsd_livestock\\' % WEB_USDA_PATH
        dir_path = create_directory(dir_path, dir_title)
        src_file = '%s\\psd_livestock_csv.zip' % DOWNLOAD_PATH
        
        download_file = browser.find_element_by_link_text('psd_livestock_csv.zip')
        download_file.click()
        time.sleep(3)
        browser.quit()
        
        # store the last_updated_date
        out_file = open('%slast_updated_date.csv' % dir_path, 'w')
        out_file.write(last_updated_date.strftime('%d/%m/%Y'))
        out_file.close()
        
        # unzip the file and move it to the dest_dir
        unzip(src_file, dir_path)
        '''
        r = csv.reader(open(dest_dir+"psd_livestock.csv"))
        headers=r.next()
        
        for key, rows in groupby(csv.reader(open(dest_dir+"psd_livestock.csv")),
                                 lambda row: row[3].replace('/', '-').replace('>', 'pre')):
            with open("%s%s%s.csv" % (dest_dir, dir_title, key), "w") as output:
                output.write('url,'+url + "\n")
                output.write(",".join(headers) + "\n")
                for row in rows:
                    output.write(",".join(row).replace('Meat,', 'Meat -') + "\n")
        '''
        print 'Finish scraping at %s.' % datetime.now()
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['usda.psd_livestock.py'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('monthly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['usda.psd_livestock.py'],[success_msg]]
        save_error_to_log('monthly', msg_list)


if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)

