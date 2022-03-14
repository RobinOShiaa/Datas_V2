'''
Created on 7 Oct 2014

@author: Wenchong

28/11/2014: Fixed excluding some areas problem found during
the QA on 25/11/2014 by downloading all contents from website
instead of scraping. All symbols in the data remain the same.
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


def scrape(db_params):
    print 'Start scraping at %s...' % datetime.now()
    
    file_name = 'pig_meat_trade'
    
    time_ids = read_from_file('%s%s/title_options/periods.csv' % (WEB_EUROSTAT_PATH, file_name))
    time_ids = time_ids[2:]
    time_ids = [t[0] for t in time_ids]
    n = get_valid_chunck_length(len(time_ids), 30)
    time_ids = chunck_list(time_ids, n)
    
    partner_ids = read_from_file('%s%s/title_options/partners.csv' % (WEB_EUROSTAT_PATH, file_name))
    partner_ids = partner_ids[2:]
    partner_ids = [p[0] for p in partner_ids]
    n = get_valid_chunck_length(len(partner_ids), 150)
    partner_ids = chunck_list(partner_ids, n)
    
    # this bookmark_url selects all flow, indicators, partner, product and reporter, period 198801 selected
    #bookmark_url = 'http://appsso.eurostat.ec.europa.eu/nui/show.do?query=BOOKMARK_DS-016894_QID_441F7225_UID_-3F171EB0&layout=PERIOD,L,X,0;REPORTER,L,Y,0;PARTNER,L,Z,0;PRODUCT,L,Z,1;FLOW,L,Z,2;INDICATORS,C,Z,3;&zSelection=DS-016894FLOW,2;DS-016894INDICATORS,QUANTITY_IN_100KG;DS-016894PARTNER,AD;DS-016894PRODUCT,0203;&rankName1=PARTNER_1_2_-1_2&rankName2=INDICATORS_1_2_-1_2&rankName3=FLOW_1_2_-1_2&rankName4=PRODUCT_1_2_-1_2&rankName5=PERIOD_1_0_0_0&rankName6=REPORTER_1_2_0_1&sortC=ASC_-1_FIRST&rStp=&cStp=&rDCh=&cDCh=&rDM=true&cDM=true&footnes=false&empty=false&wai=false&time_mode=NONE&time_most_recent=false&lang=EN&cfo=%23%23%23%2C%23%23%23.%23%23%23'
    
    # this bookmark_url selects all flow, indicators, product and reporter, partner ZZ and period 198801 selected
    bookmark_url = 'http://appsso.eurostat.ec.europa.eu/nui/show.do?query=BOOKMARK_DS-016894_QID_1B958ED1_UID_-3F171EB0&layout=PERIOD,L,X,0;REPORTER,L,Y,0;PARTNER,L,Z,0;PRODUCT,L,Z,1;FLOW,L,Z,2;INDICATORS,C,Z,3;&zSelection=DS-016894FLOW,2;DS-016894INDICATORS,QUANTITY_IN_100KG;DS-016894PARTNER,AD;DS-016894PRODUCT,0203;&rankName1=PARTNER_1_2_-1_2&rankName2=INDICATORS_1_2_-1_2&rankName3=FLOW_1_2_-1_2&rankName4=PRODUCT_1_2_-1_2&rankName5=PERIOD_1_0_0_0&rankName6=REPORTER_1_2_0_1&sortC=ASC_-1_FIRST&rStp=&cStp=&rDCh=&cDCh=&rDM=true&cDM=true&footnes=false&empty=false&wai=false&time_mode=NONE&time_most_recent=false&lang=EN&cfo=%23%23%23%2C%23%23%23.%23%23%23'
    
    count = 0
    for partner_id in partner_ids:
        for time_id in time_ids:
            wscraper = WebScraper('Chrome')
            
            # open parent window by bookmark url
            wscraper.open(bookmark_url)
            time.sleep(10)
            
            # open option window
            wscraper.click_button('class', 'selectDataButton')
            
            # get control of the popup option window
            wscraper.switch_to_popup_window()
            time.sleep(2)
            
            # select all given time and unselect default time
            wscraper.click_eurostat_checkbox('//div/a/span[contains(text(),"PERIOD")]',
                                             '//input[@id="%s"]', time_id, time_ids[-1][-1])
            
            # select all given partners and unselect default partner
            wscraper.click_eurostat_checkbox('//div/a/span[contains(text(),"PARTNER")]',
                                             '//input[@id="%s"]', partner_id, partner_ids[-1][-1])
            
            # update the statistics
            wscraper.click_button('id', 'updateExtractionButton')
            time.sleep(25)
            
            # get control of the updated parent window
            wscraper.switch_to_parent_window()
            time.sleep(2)
            
            # download file to the given folder
            count += 1
            part = '/part%s' % (count)
            print 'start downloading %s...' % part
            wscraper.download_eurostat_file(file_name, bookmark_url, 120, part)
            
            wscraper.web_driver.quit()
            
            del wscraper
        # end of inner for-loop
    # end of outter for-loop
    
    print 'Finish scraping at %s...' % datetime.now()


if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)