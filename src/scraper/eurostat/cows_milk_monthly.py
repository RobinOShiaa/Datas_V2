'''
Created on 14 Nov 2014

@author: Wenchong

26/11/2014: Fixed excluding some areas problem found during
the QA on 25/11/2014 by downloading all contents from website
instead of scraping. All symbols in the data remain the same.
07/10/2015: Fixed problem where it always downloaded data for 1968
by moving all of download process to under the 'if'.
'''

from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datetime import datetime
from datas.web.scraper import WebScraper
import time
import sys
from datas.function.function import save_error_to_log


def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()
        
        dir_name = 'cows_milk_monthly'
        
        # get the latest data date from DB
#         dbm = DBManager(db_params[0], db_params[1], db_params[2], db_params[3])
#         sql = ('select max(yearmonth) as max_date from eurostat_cows_milk_monthly '
#                'group by type order by max_date asc limit 1;')
#         date_from = dbm.get_latest_date_record(sql)
#         date_from = date_from[0][:4]
#         #print date_from
#         del dbm
        
        #date_to = datetime.now().strftime('%d/%m/%Y')
        
#         get_titles('time')
#         time_ids = read_from_file('%s%s\\title_options\\time.csv' % (WEB_EUROSTAT_PATH, dir_name))
#         time_ids = time_ids[2:]
#         time_ids = [t.split(',')[1] for t in time_ids]
#         n = get_valid_chunck_length(len(time_ids), 30)
#         time_ids = chunck_list(time_ids, n)
#         
        # this bookmark_url selects all geo, prodmilk and unit, time 1968 selected
        #bookmark_url = 'http://appsso.eurostat.ec.europa.eu/nui/show.do?query=BOOKMARK_DS-055514_QID_-210671E6_UID_-3F171EB0&layout=TIME,C,X,0;GEO,L,Y,0;PRODMILK,L,Z,0;UNIT,L,Z,1;INDICATORS,C,Z,2;&zSelection=DS-055514PRODMILK,MM001;DS-055514UNIT,THS_T;DS-055514INDICATORS,OBS_FLAG;&rankName1=UNIT_1_2_-1_2&rankName2=INDICATORS_1_2_-1_2&rankName3=PRODMILK_1_2_-1_2&rankName4=TIME_1_0_0_0&rankName5=GEO_1_2_0_1&sortC=ASC_-1_FIRST&rStp=&cStp=&rDCh=&cDCh=&rDM=true&cDM=true&footnes=false&empty=false&wai=false&time_mode=NONE&time_most_recent=false&lang=EN&cfo=%23%23%23%2C%23%23%23.%23%23%23'
        # this bookmark_url uses rolling time to get the most recent 9 months
        bookmark_url='http://appsso.eurostat.ec.europa.eu/nui/show.do?query=BOOKMARK_DS-055514_QID_31682DD9_UID_-3F171EB0&layout=TIME,C,X,0;GEO,L,Y,0;DAIRYPROD,L,Z,0;UNIT,L,Z,1;INDICATORS,C,Z,2;&zSelection=DS-055514INDICATORS,OBS_FLAG;DS-055514DAIRYPROD,D3113;DS-055514UNIT,THS_T;&rankName1=DAIRYPROD_1_2_-1_2&rankName2=UNIT_1_2_-1_2&rankName3=INDICATORS_1_2_-1_2&rankName4=TIME_1_0_0_0&rankName5=GEO_1_0_0_1&sortR=ASC_-1_FIRST&sortC=ASC_-1_FIRST&rStp=&cStp=&rDCh=&cDCh=&rDM=true&cDM=true&footnes=false&empty=false&wai=false&time_mode=ROLLING&time_most_recent=true&lang=EN&cfo=%23%23%23%2C%23%23%23.%23%23%23'

        # open parent window by bookmark url
        wscraper = WebScraper('Chrome')

    #     is_default_unselected = False
    #     #print 'time ids',time_ids
    #     for time_id in time_ids: 
    #         #print 'time', time
        wscraper.open(bookmark_url)
        time.sleep(5)
    #         
    #         # open option window
    #         wscraper.click_button('class', 'selectDataButton')
    #         time.sleep(5)
    #         # get control of the popup option window
    #         wscraper.switch_to_popup_window()
    #         time.sleep(2)
    #         
    #         # open TIME tag to select time
    #         wscraper.click_button('xpath', '//div/a/span[contains(text(),"TIME")]')
    #         time.sleep(1)
    #         
    #         # select all given time
    #         for id in time_id:
    #             #print 'id', id
    #             if id >= date_from:
    #                 #print 'true'
    # #                 alert = wscraper.web_driver.switch_to_alert()
    # #                 alert.accept()
    #                 time.sleep(5)
    #                 wscraper.click_button('xpath', '//li/a[contains(text(), "%s")]' % (id))
    #                 print 'clicked button'
    #                 time.sleep(1)
    #                 
    #                 wscraper.click_button('xpath', '//li[@id="TIME%s"]' % (time_ids[-1][-1]))
    #         # unselect the default time
    # #         print (wscraper.find_element('xpath', '//li[@id="TIME%s"]' % (time_ids[-1][-1])).is_selected())
    # #         if wscraper.find_element('xpath', '//li[@id="TIME%s"]' % (time_ids[-1][-1])).is_selected():
    # #             print 'entered if statement'
    # #             wscraper.click_button('xpath', '//li[@id="TIME%s"]' % (time_ids[-1][-1]))
    #             
    #         
    # #         
    # #         if not is_default_unselected:
    # #             wscraper.click_button('xpath', '//li[@id="TIME%s"]' % (time_ids[-1][-1]))
    # #             time.sleep(1)
    # #             is_default_unselected = True
    #         
    #         # update the statistics
    #                 wscraper.click_button('id', 'updateExtractionButton')
    #                 time.sleep(15)
    #                 
    #                 # get control of the updated parent window
    #                 wscraper.switch_to_parent_window()
    #                 time.sleep(2)
                    
                    # download file to the given folder
        part = '\\part1'#'\\part%s' % (time_ids.index(time_id) + 1)
        print 'start downloading %s...' % part
                    
        try:
            wscraper.download_eurostat_file(dir_name, bookmark_url, 25, part)
            
        except Exception as err:
            exc_info = sys.exc_info()
            raise Exception('datas.web.scraper.download_eurostat_file() error:', exc_info[0], exc_info[1], exc_info[2])
        
        wscraper.close()
        
        print 'Finished scraping at %s.' % datetime.now()
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['eurostat.cows_milk_monthly'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('monthly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['eurostat.cows_milk_monthly'],[success_msg]]
        save_error_to_log('monthly', msg_list)
    
if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)

    
