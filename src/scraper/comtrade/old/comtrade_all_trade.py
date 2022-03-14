'''
Created on 16 Apr 2015

@author: Suzanne
'''
from datetime import datetime, timedelta
from datas.db.manager import DBManager
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import create_directory
from datas.web.path import WEB_COMTRADE_PATH
from datas.web.scraper import WebScraper
from dateutil.relativedelta import relativedelta
import time


def scrape(db_params):
    print 'Start scraping at %s...' % datetime.now()
        
    # see http://comtrade.un.org/data/cache/reporterAreas.json for full list of reporters
    reporters = {'32':'Argentina', '36':'Australia','156':'China', '484':'Mexico', '554':'New Zealand', 
                 '152':'Chile','804':'Ukraine','699':'India','643':'Russian Federation','410':'Rep. of Korea','360':'Indonesia', '76':'Brazil'}
       
    dir_title = datetime.now().strftime('%Y_%m_%d')
    dir_path = '%strade_api\\' % WEB_COMTRADE_PATH
    dest_path = create_directory(dir_path, dir_title)
    
    for k, v in reporters.items():
        # get the latest data date from DB for each reporting country
        dbm = DBManager(db_params[0], db_params[1], db_params[2], db_params[3])
        sql = ('select max(yearmonth) as max_yearmonth from comtrade_all_trade '
               'where reporter = "%s";' % v)
        date_from = dbm.get_latest_date_record(sql)
        del dbm
        
        try:
            date_from = datetime.strptime(date_from[0], '%Y%m')
        except:
            date_from = datetime.strptime('201401', '%Y%m')
        
        while date_from < datetime.now():
            date_from = date_from + relativedelta(months=+1)
            yearmonth = datetime.strftime(date_from, '%Y%m')
                
            url = 'http://comtrade.un.org/api/get?max=50000&type=C&freq=M&px=HS&ps='+yearmonth+'&r='+k+'&p=0&rg=all&cc=ALL&fmt=csv'
        
            wscraper = WebScraper('urllib2')
        
            print 'scraping %s...' % (url)
            file_path = '%s%s%s.csv' % (dest_path, v, yearmonth)
            #wscraper.download_file(url, file_path)
            count = 0
            while count < 4:
                try:
                    wscraper.download_file(url, file_path)
                    time.sleep(1)
                except:
                    print 'failed to download file for %s for %s at count %s' % (v, yearmonth, count)
                    count = count + 1
                else:
                    print 'succeeded in downloading file for %s for %s at count %s' % (v, yearmonth, count)
                    break
            
            wscraper.close()
    
    print 'Finish scraping at %s...' % datetime.now()
    

if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
        
