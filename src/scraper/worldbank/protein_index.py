'''
Created on 7 Jan 2015

@author: Suzanne
'''
import sys
import os
from datas.function.function import save_error_to_log
from datetime import datetime
import time
from datas.web.scraper import WebScraper
from datas.web.path import WEB_WORLDBANK_PATH, DOWNLOAD_PATH
from datas.function.function import create_directory, unzip
from datas.db.manager import DBManager, RAW_DB_NAME, USERNAME, PASSWORD, HOST

def resume_scrape(url, date_from, directory, counter):
    try:

        scraper = WebScraper('Chrome')

        scraper.open(url) 
        scraper.web_driver.maximize_window() #important
        
        scraper.click_button('xpath', '//*[@id="wrapper"]/div[1]/div/div[4]/div[1]/div[2]/div/p/a[1]')
        time.sleep(4)
        scraper.load_field('input', 'id', 'USER', 'smccarthy@computing.dcu.ie')
        scraper.load_field('input', 'id', 'PASSWORD', '123piggy')
        scraper.click_button('xpath', '/html/body/table[3]/tbody/tr[1]/td[3]/table/tbody/tr[5]/td/table/tbody/tr[5]/td/div/input')
        time.sleep(4)
        
        # load a pre-made report
        scraper.click_button('xpath', '//*[@id="aReports"]')
        scraper.click_button('id', 'lblReportName1')
        time.sleep(4)
        
        # get most recent dates - NB this will need to be checked  
        scraper.click_button('xpath', '//*[@id="panel_MID_Time"]/div[1]/h4/a')
        time.sleep(4)
        scraper.click_button('xpath', '//*[@id="rowTimeDim"]/div/div/div[2]/div[2]/div[1]/div[4]/ul/li[2]/a')
        #scraper.click_button('xpath', '//*[@id="rowTimeDim"]/div/div/div[7]/a')
        
        time.sleep(4)
    
        
        
        scraper.web_driver.switch_to_active_element()#(scraper.find_element('class', 'selectionModifyTxt'))
        scraper.click_button('xpath', '//*[@id="divReportContent"]/div[5]/a[2]')
        #scraper.click_button('xpath', '//*[@id="divReportContent"]/div[5]/a[2]')
        #scraper.click_button('xpath', '//*[@id="divReportContent"]//div[@class="selectionModifyTxt"]//a[2]')
        
        # download file
        scraper.click_button('xpath','//*[@id="upReportLinks"]/div/ul/li[5]/a')
        time.sleep(2)
        scraper.click_button('xpath','//*[@id="liCSVDownload"]/a')
        #scraper.click_button('xpath','//*[@id="upReportLinks"]/div/ul/li[5]/ul/li[2]/a')
        time.sleep(4)
        today = datetime.now().strftime('%Y_%m_%d')
        unzip(DOWNLOAD_PATH + 'protein index.zip', WEB_WORLDBANK_PATH+'protein_index/'+today)
  
    except Exception, e:
        scraper.close()
        print 'scrape() --> resume_scrape() error: %s' % e
        return False
    else:
        scraper.close()
        return True


def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()
        
        #get the latest data date from DB
        dbm = DBManager(db_params[0], db_params[1], db_params[2], db_params[3])
        date_from = dbm.get_latest_date_record('select max(yearmonth) from worldbank_protein_index;')
        date_from = datetime.strptime(date_from[0], '%Y%m')
        #date_from = datetime.strftime(date_from, '%YM%m')
        if not date_from:
            date_from = '2000-01-01'
        del dbm
        
        #url= 'http://databank.worldbank.org/data/views/variableselection/selectvariables.aspx?source=global-economic-monitor-(gem)-commodities#'
        url='http://databank.worldbank.org/data/home.aspx'
        
        path = '%sprotein_index\\' % WEB_WORLDBANK_PATH
        today = datetime.now().strftime("%Y_%m_%d")
        directory = create_directory(path, today)
        
        counter = 0
        while not resume_scrape(url, date_from, directory, counter):
            if counter >= 5:
                raise Exception('web communication error, exceeds max number of attempts, stop scraping')
            else:
                print 'scrape %s at counter %s...' % (date_from, counter)
                counter += 1
    
        print "Finished scraping at %s" % datetime.now()
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['worldbank.protein_index.py'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('monthly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['worldbank.protein_index.py'],[success_msg]]
        save_error_to_log('monthly', msg_list)


if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
    