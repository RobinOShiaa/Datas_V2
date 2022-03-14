'''
Created on 7 Oct 2014

@author: Wenchong

28/11/2014: Fixed excluding some areas problem found during
the QA on 25/11/2014 by downloading all contents from website
instead of scraping. All symbols in the data remain the same.
04/02/2015(Wenchong): Automation completed.
12/02/2015(Wenchong): Fixed sql query to get the correct date as a new scraping point.
'''


import time
from datetime import datetime
from datas.db.manager import DBManager
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import chunck_list
from datas.function.function import get_valid_chunck_length
from datas.function.function import read_from_file
from datas.web.path import WEB_EUROSTAT_PATH
from datas.web.scraper import WebScraper
from pig_meat_trade_titles import get_titles


NUM_PART = 0
PARTNER_IDS = []
TIME_IDS = []


def resume_scrape(partner_brk_point=0, time_brk_point=0):
    global NUM_PART
    global PARTNER_IDS
    global TIME_IDS
    
    file_name = 'pig_meat_trade_hs2'
    
    # this bookmark_url selects all flows, indicators, HS2 products and reporters, partner ZZ and period 198801 selected
    bookmark_url = 'http://appsso.eurostat.ec.europa.eu/nui/show.do?query=BOOKMARK_DS-016894_QID_1B958ED1_UID_-3F171EB0&layout=PERIOD,L,X,0;REPORTER,L,Y,0;PARTNER,L,Z,0;PRODUCT,L,Z,1;FLOW,L,Z,2;INDICATORS,C,Z,3;&zSelection=DS-016894FLOW,2;DS-016894INDICATORS,QUANTITY_IN_100KG;DS-016894PARTNER,AD;DS-016894PRODUCT,0203;&rankName1=PARTNER_1_2_-1_2&rankName2=INDICATORS_1_2_-1_2&rankName3=FLOW_1_2_-1_2&rankName4=PRODUCT_1_2_-1_2&rankName5=PERIOD_1_0_0_0&rankName6=REPORTER_1_2_0_1&sortC=ASC_-1_FIRST&rStp=&cStp=&rDCh=&cDCh=&rDM=true&cDM=true&footnes=false&empty=false&wai=false&time_mode=NONE&time_most_recent=false&lang=EN&cfo=%23%23%23%2C%23%23%23.%23%23%23'
    
    tmp_partner_ids = PARTNER_IDS[partner_brk_point:]
    
    for partner_id in tmp_partner_ids:
        if tmp_partner_ids.index(partner_id) == 0:
            tmp_time_ids = TIME_IDS[time_brk_point:]
        else:
            tmp_time_ids = TIME_IDS[0:]
        
        for time_id in tmp_time_ids:
            try:
                wscraper = WebScraper('Chrome')
                
                # open parent window by bookmark url
                wscraper.open(bookmark_url)
                #time.sleep(10)
                wscraper.wait(30, 'class', 'selectDataButton')
                
                # open option window
                wscraper.click_button('class', 'selectDataButton')
                
                # get control of the popup option window
                wscraper.switch_to_popup_window()
                time.sleep(2)
                
                # select all given time and unselect default time
                wscraper.click_eurostat_checkbox('//div/a/span[contains(text(),"PERIOD")]',
                                                 '//input[@id="%s"]', time_id, 'ck_198801')
                
                # select all given partners and unselect default partner
                wscraper.click_eurostat_checkbox('//div/a/span[contains(text(),"PARTNER")]',
                                                 '//input[@id="%s"]', partner_id, 'ck_ZZ')
                
                # update the statistics
                wscraper.click_button('id', 'updateExtractionButton')
                time.sleep(25)
                
                # get control of the updated parent window
                wscraper.switch_to_parent_window()
                time.sleep(2)
                
                # download file to the given folder
                part = '\\part%s' % (NUM_PART)
                print 'start downloading %s...' % part
                
                wscraper.download_eurostat_file(file_name, bookmark_url, 30, part)
            except Exception as e:
                print 'scrape() error: %s\nat partner %s, time %s\nresuming from break point...' % (e, partner_id, time_id)
                
                wscraper.close()
                del wscraper
                
                resume_scrape(PARTNER_IDS.index(partner_id), TIME_IDS.index(time_id))
                return
            else:
                NUM_PART += 1
                wscraper.close()
                del wscraper
        # end of inner for-loop
    # end of outer for-loop


def scrape(db_params):
    global PARTNER_IDS
    global TIME_IDS
    
    print 'Start scraping at %s...' % datetime.now()
    
    # get the latest data date from DB
    dbm = DBManager(db_params[0], db_params[1], db_params[2], db_params[3])
    sql = ('select max(yearmonth) as max_date from eurostat_pig_meat_trade_hs2 '
           'group by product_code, flow order by max_date asc limit 1;')
    date_from = dbm.get_latest_date_record(sql)
    year_from = int(date_from[0][:4])
    month_from = int(date_from[0][4:])
    del dbm
    
    file_name = 'pig_meat_trade_hs2'
    
    #get period ids
    get_titles('period') # should run this on a monthly basis
    all_time_ids = read_from_file('%s%s\\title_options\\periods.csv' % (WEB_EUROSTAT_PATH, file_name))
    all_time_ids = all_time_ids[2:]
    all_time_ids = [t[0] for t in all_time_ids]
    
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
    
    if not TIME_IDS:
        print 'No new data found'
        print 'Finish scraping at %s...' % datetime.now()
        return
    
    n = get_valid_chunck_length(len(TIME_IDS), 30)
    TIME_IDS = chunck_list(TIME_IDS, n)
    
    # get partners
    PARTNER_IDS = read_from_file('%s%s\\title_options\\partners_needed.csv' % (WEB_EUROSTAT_PATH, file_name))
    PARTNER_IDS = PARTNER_IDS[2:]
    PARTNER_IDS = [p[0] for p in PARTNER_IDS]
    n = get_valid_chunck_length(len(PARTNER_IDS), 2)
    n = 1
    PARTNER_IDS = chunck_list(PARTNER_IDS, n)
    
    #print len(TIME_IDS), TIME_IDS
    #print year_from, month_from
    #print len(PARTNER_IDS), PARTNER_IDS
    #return
    
    # do not use this
    # this bookmark_url selects all flows, indicators, HS2 products, reporters and partners, period 198801 selected
    #bookmark_url = 'http://appsso.eurostat.ec.europa.eu/nui/show.do?query=BOOKMARK_DS-016894_QID_441F7225_UID_-3F171EB0&layout=PERIOD,L,X,0;REPORTER,L,Y,0;PARTNER,L,Z,0;PRODUCT,L,Z,1;FLOW,L,Z,2;INDICATORS,C,Z,3;&zSelection=DS-016894FLOW,2;DS-016894INDICATORS,QUANTITY_IN_100KG;DS-016894PARTNER,AD;DS-016894PRODUCT,0203;&rankName1=PARTNER_1_2_-1_2&rankName2=INDICATORS_1_2_-1_2&rankName3=FLOW_1_2_-1_2&rankName4=PRODUCT_1_2_-1_2&rankName5=PERIOD_1_0_0_0&rankName6=REPORTER_1_2_0_1&sortC=ASC_-1_FIRST&rStp=&cStp=&rDCh=&cDCh=&rDM=true&cDM=true&footnes=false&empty=false&wai=false&time_mode=NONE&time_most_recent=false&lang=EN&cfo=%23%23%23%2C%23%23%23.%23%23%23'
    
    resume_scrape(0, 0)
    
    print 'Finish scraping at %s...' % datetime.now()


if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
