'''
Created on 13 Apr 2016

@author: Suzanne
'''
from datetime import datetime
from datas.function.function import create_directory, chunck_list,save_error_to_log
from datas.web.path import WEB_COMTRADE_PATH
from datas.db.manager import DBManager, RAW_DB_NAME, HOST, USERNAME, PASSWORD
import pandas as pd
import time
import sys

def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()
    
        dbm = DBManager(db_params[0], db_params[1], db_params[2], db_params[3])

        sql = 'select max(year) from comtrade_all_trade;'
    
        date_from = dbm.get_latest_date_record(sql)[0]
        print date_from
        #date_from = str(int(date_from) + 1)
        #date_from = '2015'
        data = pd.DataFrame()
        
        # read product codes and reporters from json
        all_hs_codes = 'http://comtrade.un.org/data/cache/classificationHS.json'
        all_hs_codes = pd.read_json(all_hs_codes)['results'] 
        hs_codes = []
        
        all_reporters = 'http://comtrade.un.org/data/cache/reporterAreas.json'
        all_reporters = pd.read_json(all_reporters)['results'] 
        reporters = []
        
        # remove reporters we are scraping elsewhere
        #[all, Austria, Belgium,Belgium-Luxembourg, Bulgaria, Croatia, Republic of Cyprus, Czech Republic, Denmark, Estonia, Finland,France,Germany,Greece,Hungary,Ireland,Italy,Latvia,
        #Lithuania,Luxembourg,Malta,Netherlands,Poland,Portugal,Romania,Slovakia,Slovenia,Spain,Sweden,United Kingdom,Fmr Yugoslavia, USA, Canada, New Zealand]
        exclude_reporters = ["all","40","56","58","100","191","196","203","200","208","233","246","251","276","300","348","372","381","428",
                             "440","442","470","528","616","620","642","703","705","724","752","826","890","842","124","554"]
        
        i = 0
        while i < len(all_reporters):
            if all_reporters[i]['id'] not in exclude_reporters:
                reporters.append(all_reporters[i]['id'])
            i = i + 1
        
        # get just meat and dairy data
        m = 0
        while m < len(all_hs_codes):
            if all_hs_codes[m]['id'][:2] in ['02','04']:
            #if all_hs_codes[m]['id'][:4] == '3501':
                hs_codes.append(all_hs_codes[m]['id'])
            m = m + 1

        reporters = chunck_list(reporters, 5)
        hs_codes = chunck_list(hs_codes, 10)
    
        # dynamically generate urls
        for reps in reporters:
            for codes in hs_codes:
                # for testing
                #url = 'http://comtrade.un.org/api/get?max=50000&type=C&freq=M&px=HS&ps=%s&r=%s&p=all&rg=all&cc=%s&fmt=csv' % ('2015','858',','.join(codes))
                #for full scrape
                url = 'http://comtrade.un.org/api/get?max=50000&type=C&freq=M&px=HS&ps=%s&r=%s&p=all&rg=all&cc=%s&fmt=csv' % (date_from, ','.join(reps), ','.join(codes))

                print url
                try:
                    df = pd.read_csv(url)
                    if 'No data matches your query' not in df['Classification']:
                        data = data.append(df)

                except:
                    print 'url returned error'
                    continue
                else:
                    print codes, reps
                 
                time.sleep(40)
        
        today = datetime.strftime(datetime.now(), '%Y_%m_%d')
        dir_path = create_directory(WEB_COMTRADE_PATH, today)
        data.to_csv('%scomtrade_%s.csv' % (dir_path, date_from))
        
        print 'Finished scraping at %s.' % datetime.now()
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['comtrade_api.py'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('monthly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['comtrade_api.py'],[success_msg]]
        save_error_to_log('monthly', msg_list)

if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
