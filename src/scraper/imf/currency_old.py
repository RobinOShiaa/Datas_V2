'''
Created on 14 Nov 2014

@author: Suzanne

29/01/2015(Wenchong): Automation completed.
12/02/2015(Wenchong): Fixed sql query to get the correct date as a new scraping point.
'''

from datas.function.function import save_error_to_log
import os
import csv
import sys
import time
from datetime import datetime
from datetime import timedelta
from datas.db.manager import DBManager
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import create_directory
from datas.web.path import DOWNLOAD_PATH
from datas.web.path import WEB_IMF_PATH
from datas.web.scraper import WebScraper
import pandas as pd


def scrape(db_params):
    #try:
        print 'Start scraping at %s...' % datetime.now()
         
        # get the latest data date from DB
        dbm = DBManager(db_params[0], db_params[1], db_params[2], db_params[3])
        sql = ('select max(date) as max_date from imf_currency '
               'group by currency order by max_date asc limit 1;')
        date_from = dbm.get_latest_date_record(sql)
         
         
        if not date_from:
            date_from = "01/01/1994"
            date_from = datetime.strptime(date_from, '%d/%m/%Y')
        else:
         
            date_from = date_from[0]
            date_from += timedelta(days=1)
        del dbm
         
        scraper = WebScraper('Chrome')
        url = 'http://www.imf.org/external/np/fin/ert/GUI/Pages/CountryDataBase.aspx'
        date_to = datetime.now() #important to avoid zero-padding, which will make program crash on certain dates
        #date_to = datetime.strptime(date_to, '%d/%m/%Y')
         
        '''--------------Start scrape---------------'''
        scraper.open(url)
         
        '''Page 1'''
        scraper.click_button('id','ctl00_ContentPlaceHolder1_countryid') #Select by country
        SDR = scraper.web_driver.find_element_by_xpath('//*[@id="content1"]/table/tbody/tr/td/table/tbody/tr[2]/td/div/table/tbody/tr/td/table[2]/tbody/tr[2]/td/table/tbody/tr[1]/td[1]/input')
        SDR.click()
        scraper.click_button('id','ctl00_ContentPlaceHolder1_RadioDateRange') #Select by date range
        scraper.load_field('select', 'id', 'ctl00_ContentPlaceHolder1_SelectFromMonth', str(date_from.month))
        scraper.load_field('select', 'id', 'ctl00_ContentPlaceHolder1_SelectFromDay', str(date_from.day))
        scraper.load_field('select', 'id', 'ctl00_ContentPlaceHolder1_SelectFromYear', str(date_from.year))
        scraper.load_field('select', 'id', 'ctl00_ContentPlaceHolder1_SelectToMonth', str(date_to.month))
        scraper.load_field('select', 'id', 'ctl00_ContentPlaceHolder1_SelectToDay', str(date_to.day))
        scraper.load_field('select', 'id', 'ctl00_ContentPlaceHolder1_SelectToYear', str(date_to.year))
        scraper.click_button('id','ctl00_ContentPlaceHolder1_BtnContinue') #First continue
        time.sleep(2)
         
        '''Page 2'''
        scraper.click_button('id','ctl00_ContentPlaceHolder1_BtnSelect') #Select all countries
        time.sleep(2)
        scraper.click_button('id','ctl00_ContentPlaceHolder1_BtnContinueTwo') #Second continue
        time.sleep(2)
         
        '''Page 3'''
        scraper.click_button('id','ctl00_ContentPlaceHolder1_rdoDateSortOrderAscending') #Sort dates
        scraper.click_button('id','ctl00_ContentPlaceHolder1_rdoDecimalSymbolPeriod') #Important - sets decimal symbol as full stop rather than comma
        scraper.click_button('id','ctl00_ContentPlaceHolder1_rdoDispFormatNA') #Sets empty cells as 'n/a'
        scraper.click_button('id','ctl00_ContentPlaceHolder1_rdoCompFormatUnCompressed') #Shows data uncompressed
        scraper.click_button('id','ctl00_ContentPlaceHolder1_imgBtnPrepareReport') #Prepare report
        time.sleep(40)
        #time.sleep(30)
#         #scraper.wait(30, 'xpath', '//a[@href="ReportData.aspx?Type=TSV"]')
#         #scraper.click_button('xpath', '//a[@href="ReportData.aspx?Type=TSV"]') # downloads as .tsv
#         time.sleep(10)
#         
#         scraper.close()
#         
#         dir_title = datetime.now().strftime('%Y_%m_%d')
#         dir_path = '%scurrency\\' % WEB_IMF_PATH
#         dir_path = create_directory(dir_path, dir_title)
#         dest_file = '%sExchange_Rate_Report.csv' % (dir_path)
#         
#         #source_file = '%s\\Exchange_Rate_Report.tsv' % DOWNLOAD_PATH
#         source_file = '%s\\Exchange_Rate_Report.xls' % DOWNLOAD_PATH
#         
#         #csv.writer(file(dest_file, 'wb')).writerows(csv.reader(open(source_file), delimiter="\t"))
#         #os.remove(DOWNLOAD_PATH+'Exchange_Rate_Report.tsv')
#         xl = pd.ExcelFile(source_file)
#         xl.to_csv(dest_file)
#         
#         print 'Finish scraping at %s.' % datetime.now()
#     except Exception as err:
#         exc_info = sys.exc_info()
#         error_msg = 'auto_run() scrape error:\n'
#         msg_list = [['imf.currency.py'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
#         print msg_list
#         save_error_to_log('daily', msg_list)
#     else:
#         success_msg = 'auto_run() scraped successfully\n'
#         msg_list = [['imf.currency.py'],[success_msg]]
#         save_error_to_log('daily', msg_list)


if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
    