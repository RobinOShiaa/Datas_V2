'''
Created on 14 Nov 2014

@author: Wenchong

26/11/2014: Fixed excluding some areas problem found during
the QA on 25/11/2014 by downloading all contents from website
instead of scraping. All symbols in the data remain the same.
07/10/2015: Fixed problem where it only downloaded oldest data
by moving all of download process to under the 'if'.
'''

from datas.db.manager import DBManager, RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datetime import datetime
import time
from datas.function.function import get_valid_chunck_length, chunck_list, read_from_file
from datas.web.path import WEB_EUROSTAT_PATH
from datas.web.scraper import WebScraper
from scraper.eurostat.milk_prod_util_annual_titles import get_titles
import sys
from datas.function.function import save_error_to_log


def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()
        
        file_name = 'milk_prod_util_annual'
        
        # get the latest data date from DB
        dbm = DBManager(db_params[0], db_params[1], db_params[2], db_params[3])
        sql = ('select max(year) as max_date from eurostat_milk_prod_util_annual '
               'group by type order by max_date asc limit 1;')
        date_from = dbm.get_latest_date_record(sql)
        date_from = date_from[0]
        del dbm
        
        #date_to = datetime.now().strftime('%d/%m/%Y')
        get_titles('time')
        #return
        time_ids = read_from_file('%s%s\\title_options\\time.csv' % (WEB_EUROSTAT_PATH, file_name))
        
        time_ids = time_ids[2:]
        time_ids = [t[0] for t in time_ids]
        n = get_valid_chunck_length(len(time_ids), 30)
        time_ids = chunck_list(time_ids, n)
    
        #date_to = datetime.now().strftime('%d/%m/%Y')
    
        # this bookmark_url selects all geo, milkitem, prodmilk and default time
        bookmark_url = 'http://appsso.eurostat.ec.europa.eu/nui/show.do?query=BOOKMARK_DS-052668_QID_6BFE3BD7_UID_-3F171EB0&layout=TIME,C,X,0;GEO,L,Y,0;PRODMILK,L,Z,0;MILKITEM,L,Z,1;INDICATORS,C,Z,2;&zSelection=DS-052668PRODMILK,MF000;DS-052668MILKITEM,PRO;DS-052668INDICATORS,OBS_FLAG;&rankName1=INDICATORS_1_2_-1_2&rankName2=MILKITEM_1_2_-1_2&rankName3=PRODMILK_1_2_-1_2&rankName4=TIME_1_0_0_0&rankName5=GEO_1_2_0_1&sortC=ASC_-1_FIRST&rStp=&cStp=&rDCh=&cDCh=&rDM=true&cDM=true&footnes=false&empty=false&wai=false&time_mode=NONE&time_most_recent=false&lang=EN&cfo=%23%23%23%2C%23%23%23.%23%23%23'
        #bookmark_url = 'http://appsso.eurostat.ec.europa.eu/nui/show.do?query=BOOKMARK_DS-052668_QID_467A1D8D_UID_-3F171EB0&layout=TIME,C,X,0;GEO,L,Y,0;PRODMILK,L,Z,0;MILKITEM,L,Z,1;INDICATORS,C,Z,2;&zSelection=DS-052668PRODMILK,MF000;DS-052668MILKITEM,PRO;DS-052668INDICATORS,OBS_FLAG;&rankName1=INDICATORS_1_2_-1_2&rankName2=MILKITEM_1_2_-1_2&rankName3=PRODMILK_1_2_-1_2&rankName4=TIME_1_0_0_0&rankName5=GEO_1_2_0_1&sortC=ASC_-1_FIRST&rStp=&cStp=&rDCh=&cDCh=&rDM=true&cDM=true&footnes=false&empty=false&wai=false&time_mode=NONE&time_most_recent=false&lang=EN&cfo=%23%23%23%2C%23%23%23.%23%23%23'
    
        wscraper = WebScraper('Chrome')
        
        is_default_unselected = False
    
        for time_id in time_ids:
            wscraper.open(bookmark_url)
            time.sleep(5)
            
            # open option window
            wscraper.click_button('class', 'selectDataButton')
            
            time.sleep(4)
            # get control of the popup option window
            wscraper.switch_to_popup_window()
            time.sleep(2)
            
            
            # open TIME tag to select time
            wscraper.click_button('xpath', '//div/a/span[contains(text(),"TIME")]')
            time.sleep(1)
            wscraper.click_button('xpath', '//input[@id="%s"]' % (time_ids[-1][-1]))
            # select all given time
            for id in time_id:
                
                if id[3:] >= date_from:
                    #print id, date_from
                    try:
                        wscraper.click_button('xpath', '//input[@id="%s"]' % (id))
                    except:
                        continue
                    time.sleep(1)
            
    #         # unselect the default time
    #         if not is_default_unselected:
    #             wscraper.click_button('xpath', '//input[@id="%s"]' % (time_ids[-1][-1]))
    #             time.sleep(1)
    #             is_default_unselected = True
            
                    # update the statistics
                    wscraper.click_button('id', 'updateExtractionButton')
                    time.sleep(15)
                    
                    # get control of the updated parent window
                    wscraper.switch_to_parent_window()
                    time.sleep(2)
                    
                    # download file to the given folder
                    part = '\\part1'
                    print 'start downloading %s...' % part
                    
                    try:
                        wscraper.download_eurostat_file(file_name, bookmark_url, 30, '')
                    except Exception as err:
                        exc_info = sys.exc_info()
                        raise Exception('datas.web.scraper.download_eurostat_file() error:', exc_info[0], exc_info[1], exc_info[2])
            
        wscraper.close()
        
        print 'finished scraping at %s...' % datetime.now()
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['eurostat.milk_prod_util_annual'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n\n']]
        print msg_list
        save_error_to_log('monthly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['eurostat.milk_prod_util_annual'],[success_msg]]
        save_error_to_log('monthly', msg_list)

if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
    