'''
Created on 10 May 2016

@author: Suzanne
'''
import sys
import urllib
from datetime import datetime
from datas.function.function import create_directory
from datas.function.function import save_error_to_log
from datas.function.function import move_download_file
from datas.web.path import DOWNLOAD_PATH
from datas.web.path import WEB_DAIRYAUSTRALIA_PATH
from datas.db.manager import DBManager, RAW_DB_NAME, HOST, USERNAME, PASSWORD
from dateutil.relativedelta import relativedelta

def scrape(db_params):
    try:
        print 'Start scraping at %s... ' % (datetime.now())

        dbm = DBManager(db_params[0], db_params[1], db_params[2], db_params[3])
        sql = ('select max(yearmonth_to) as max_date from dairyaustralia_trade_total;')
        date_from = dbm.get_latest_date_record(sql)[0]
        month = datetime.strptime(date_from[4:],'%m') + relativedelta(months=1)
        month = datetime.strftime(month,'%B')

        year = date_from[:4]
        if month=='January':
            year = str(int(year)+1)

        url = 'http://www.dairyaustralia.com.au/~/media/Documents/Stats%20and%20markets/Exports%20and%20trade/Dairy%20markets/Dairy%20Export%20Report%20'+month+'%20'+year+'.xls' #% month
        urllib.urlretrieve(url, DOWNLOAD_PATH+'dairyaus_trade_%s.xls' % month)
        today = datetime.strftime(datetime.now(),'%Y_%m_%d')
        file_path = create_directory(WEB_DAIRYAUSTRALIA_PATH+'dairy_trade/',today)
        move_download_file(DOWNLOAD_PATH, file_path)
               
        print 'Finished scraping at %s.' % (datetime.now())
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['dairyaustralia_trade_monthly.py'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('monthly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['dairyaustralia_trade_monthly.py'],[success_msg]]
        save_error_to_log('monthly', msg_list)

if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
    
