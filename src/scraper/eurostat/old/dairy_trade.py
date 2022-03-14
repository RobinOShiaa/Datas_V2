'''
Created on 28 Jan 2015

@author: Suzanne
13/02/2015(Sue): changed scrape so all partners are pre-selected, reporters_needed are put in a loop
15/04/2015(Wenchong): bookmark_url parsing error, same error in dairy_trade_titles. Can't fix this problem
because the bookmark_url described in the scraping template document is not for dairy trade.
'''

import time
from datetime import datetime
from dairy_trade_titles import get_titles
from datas.db.manager import DBManager, RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import chunck_list
from datas.function.function import get_valid_chunck_length
from datas.function.function import read_from_file
from datas.web.path import WEB_EUROSTAT_PATH
from datas.web.scraper import WebScraper


NUM_PART = 1
REPORTER_IDS = []
TIME_IDS = []


def recover_scrape(reporter_brk_point=0, time_brk_point=0):
    global NUM_PART
    global REPORTER_IDS
    global TIME_IDS
    
    file_name = 'dairy_trade'
    
    # this url selects all dairy products to 6 digit hs codes, all partners, time id 198801, reporter code ck_AT.
    # No it doesn't, it selects milk collection and dairy products obtained. 07/05/2015
    #bookmark_url = 'http://appsso.eurostat.ec.europa.eu/nui/show.do?query=BOOKMARK_DS-052400_QID_-DAECD00_UID_-3F171EB0&layout=TIME,C,X,0;GEO,L,Y,0;PRODMILK,L,Z,0;MILKITEM,L,Z,1;INDICATORS,C,Z,2;&zSelection=DS-052400MILKITEM,PRO;DS-052400PRODMILK,MC000;DS-052400INDICATORS,OBS_FLAG;&rankName1=INDICATORS_1_2_-1_2&rankName2=MILKITEM_1_2_-1_2&rankName3=PRODMILK_1_2_-1_2&rankName4=TIME_1_0_0_0&rankName5=GEO_1_2_0_1&sortC=ASC_-1_FIRST&rStp=&cStp=&rDCh=&cDCh=&rDM=true&cDM=true&footnes=false&empty=false&wai=false&time_mode=NONE&time_most_recent=false&lang=EN&cfo=%23%23%23%2C%23%23%23.%23%23%23'

    bookmark_url='http://appsso.eurostat.ec.europa.eu/nui/show.do?query=BOOKMARK_DS-016893_QID_7E3AD81F_UID_-3F171EB0&layout=PERIOD,L,X,0;REPORTER,L,Y,0;PARTNER,L,Z,0;PRODUCT,L,Z,1;FLOW,L,Z,2;INDICATORS,C,Z,3;&zSelection=DS-016893PARTNER,EU28_EXTRA;DS-016893INDICATORS,VALUE_IN_EUROS;DS-016893FLOW,1;DS-016893PRODUCT,040110;&rankName1=PARTNER_1_2_-1_2&rankName2=INDICATORS_1_2_-1_2&rankName3=FLOW_1_2_-1_2&rankName4=PRODUCT_1_2_-1_2&rankName5=PERIOD_1_0_0_0&rankName6=REPORTER_1_2_0_1&sortC=ASC_-1_FIRST&rStp=&cStp=&rDCh=&cDCh=&rDM=true&cDM=true&footnes=false&empty=false&wai=false&time_mode=NONE&time_most_recent=false&lang=EN&cfo=%23%23%23%2C%23%23%23.%23%23%23'
    
    
    # This one gives a parsing error 07/05/2015
    #bookmark_url = 'http://appsso.eurostat.ec.europa.eu/nui/show.do?query=BOOKMARK_DS-016893_QID_-366E042E_UID_-3F171EB0&layout=PERIOD,L,X,0;REPORTER,L,Y,0;reporter,L,Z,0;PRODUCT,L,Z,1;FLOW,L,Z,2;INDICATORS,C,Z,3;&zSelection=DS-016893reporter,ZZ;DS-016893INDICATORS,QUANTITY_IN_100KG;DS-016893FLOW,1;DS-016893PRODUCT,TOTAL;&rankName1=reporter_1_2_-1_2&rankName2=INDICATORS_1_2_-1_2&rankName3=FLOW_1_2_-1_2&rankName4=PRODUCT_1_2_-1_2&rankName5=PERIOD_1_0_0_0&rankName6=REPORTER_1_2_0_1&sortC=ASC_-1_FIRST&rStp=&cStp=&rDCh=&cDCh=&rDM=true&cDM=true&footnes=false&empty=false&wai=false&time_mode=NONE&time_most_recent=false&lang=EN&cfo=%23%23%23%2C%23%23%23.%23%23%23'
    
    # This url selects total EU countries, sitco6 all products, all flows
    # http://appsso.eurostat.ec.europa.eu/nui/show.do?query=BOOKMARK_DS-054634_QID_-5E12B45B_UID_-3F171EB0&layout=TIME,C,X,0;STK_FLOW,L,Y,0;SITC06,L,Z,0;PARTNER,L,Z,1;GEO,L,Z,2;INDIC_ET,L,Z,3;INDICATORS,C,Z,4;&zSelection=DS-054634GEO,EU28;DS-054634INDICATORS,OBS_FLAG;DS-054634PARTNER,EXT_EU28;DS-054634INDIC_ET,IVU;DS-054634SITC06,TOTAL;&rankName1=STK-FLOW_1_2_0_1&rankName2=PARTNER_1_2_-1_2&rankName3=TIME_1_0_0_0&rankName4=SITC06_1_2_-1_2&rankName5=INDIC-ET_1_2_-1_2&rankName6=GEO_1_2_-1_2&rankName7=INDICATORS_1_2_-1_2&sortC=ASC_-1_FIRST&rStp=&cStp=&rDCh=&cDCh=&rDM=true&cDM=true&footnes=false&empty=false&wai=false&time_mode=ROLLING&time_most_recent=false&lang=EN&cfo=%23%23%23%2C%23%23%23.%23%23%23
    
    # this url selects all dairy products to 6 digit hs codes, all reporters, time id 198801, partner code zz
    # This url gives a parsing error 07/05/2015
    #bookmark_url = 'http://appsso.eurostat.ec.europa.eu/nui/show.do?query=BOOKMARK_DS-016893_QID_49932F64_UID_-3F171EB0&layout=PERIOD,L,X,0;REPORTER,L,Y,0;reporter,L,Z,0;PRODUCT,L,Z,1;FLOW,L,Z,2;INDICATORS,C,Z,3;&zSelection=DS-016893reporter,ZZ;DS-016893INDICATORS,QUANTITY_IN_100KG;DS-016893FLOW,1;DS-016893PRODUCT,TOTAL;&rankName1=reporter_1_2_-1_2&rankName2=INDICATORS_1_2_-1_2&rankName3=FLOW_1_2_-1_2&rankName4=PRODUCT_1_2_-1_2&rankName5=PERIOD_1_0_0_0&rankName6=REPORTER_1_2_0_1&ppcRK=FIRST&ppcSO=ASC&sortC=ASC_-1_FIRST&rStp=&cStp=&rDCh=&cDCh=&rDM=true&cDM=true&footnes=false&empty=false&wai=false&time_mode=NONE&time_most_recent=false&lang=EN&cfo=%23%23%23%2C%23%23%23.%23%23%23'    
    
    tmp_reporter_ids = REPORTER_IDS[reporter_brk_point:]
    
    for reporter_id in tmp_reporter_ids:
        if tmp_reporter_ids.index(reporter_id) == 0:
            tmp_time_ids = TIME_IDS[time_brk_point:]
        else:
            tmp_time_ids = TIME_IDS[0:]
        
        for time_id in tmp_time_ids:
            try:
                wscraper = WebScraper('Chrome')
                
                # open parent window by bookmark url
                wscraper.open(bookmark_url)
                
                wscraper.wait(30, 'class', 'selectDataButton')
                
                # open option window
                wscraper.click_button('class', 'selectDataButton')
                
                # get control of the popup option window
                wscraper.switch_to_popup_window()
                time.sleep(2)
                
                # select all given time and unselect default time
                wscraper.click_eurostat_checkbox('//div/a/span[contains(text(),"PERIOD")]',
                                                 '//input[@id="%s"]', time_id, 'ck_198801')
                
                # select all given reporters and unselect default reporter
                wscraper.click_eurostat_checkbox('//div/a/span[contains(text(),"REPORTER")]',
                                                 '//input[@id="%s"]', reporter_id, 'ck_AT')
                
                # update the statistics
                wscraper.click_button('id', 'updateExtractionButton')
                time.sleep(20)
                
                # get control of the updated parent window
                wscraper.switch_to_parent_window()
                time.sleep(2)
                
                # download file to the given folder
                part = '\\part%s' % (NUM_PART)
                print 'start downloading %s...' % part
                
                wscraper.download_eurostat_file(file_name, bookmark_url, 30, part)
            except Exception as e:
                print 'scrape() error: %s\nat reporter %s, time %s\nresuming from break point...' % (e, reporter_id, time_id)
                
                wscraper.close()
                del wscraper
                
                recover_scrape(REPORTER_IDS.index(reporter_id), TIME_IDS.index(time_id))
                return
            else:
                NUM_PART += 1
                wscraper.close()
                del wscraper
        # end of inner for-loop
    # end of outter for-loop


def scrape(db_params):
    global reporter_IDS
    global TIME_IDS
    
    print 'Start scraping at %s...' % datetime.now()
    
    # get the latest data date from DB
    dbm = DBManager(db_params[0], db_params[1], db_params[2], db_params[3])
    sql = ('select max(yearmonth) as max_date from eurostat_dairy_trade '
           'group by product_code, flow order by max_date asc limit 1;')
    date_from = dbm.get_latest_date_record(sql)
    #year_from = int(date_from[0][:4])
    #month_from = int(date_from[0][4:])
    year_from = 2001
    month_from = 0
    del dbm
    
    file_name = 'dairy_trade'
    
    #get period ids
    get_titles('period') # should run this on a monthly basis
    all_time_ids = read_from_file('%s%s\\title_options\\periods.csv' % (WEB_EUROSTAT_PATH, file_name))
    all_time_ids = all_time_ids[2:]
    
    all_time_ids = [t[0].split(',')[0] for t in all_time_ids]
    #print all_time_ids
    # generate valid period ids
    TIME_IDS = []
    this_year = datetime.now().year
    for i in range(year_from, this_year + 1):
        month_start = 1
        if i == year_from:
            month_start = month_from + 1
        
        for j in range(month_start, 13):
            time_id = 'ck_%d%02d' % (i, j)
            if time_id in all_time_ids:
                TIME_IDS.append(time_id)
    #print TIME_IDS
    
    if not TIME_IDS:
        print 'No new data found'
        print 'Finish scraping at %s...' % datetime.now()
        return
    
    n = get_valid_chunck_length(len(TIME_IDS), 30)
    TIME_IDS = chunck_list(TIME_IDS, n)
    
    # get reporters
    REPORTER_IDS = read_from_file('%s%s\\title_options\\reporters_needed.csv' % (WEB_EUROSTAT_PATH, file_name))
    REPORTER_IDS = REPORTER_IDS[2:]
    REPORTER_IDS = [p[0] for p in REPORTER_IDS]
    n = get_valid_chunck_length(len(REPORTER_IDS), 2)
    n = 1
    REPORTER_IDS = chunck_list(REPORTER_IDS, n)
    
    #print len(TIME_IDS), TIME_IDS
    #print len(REPORTER_IDS), REPORTER_IDS
    #return
        
    recover_scrape(20, 4)
    
    print 'Finish scraping at %s...' % datetime.now()


if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
