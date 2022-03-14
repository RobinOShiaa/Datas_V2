'''
Created on 28 Jan 2015

@author: Suzanne
'''


import time
from datas.function.function import create_directory
from datas.web.path import WEB_EUROSTAT_PATH
from datas.web.scraper import WebScraper


def get_titles(option='all'):
    dir_path = create_directory(WEB_EUROSTAT_PATH, 'dairy_trade/title_options')
    #bookmark_url = 'http://appsso.eurostat.ec.europa.eu/nui/show.do?query=BOOKMARK_DS-052400_QID_-DAECD00_UID_-3F171EB0&layout=TIME,C,X,0;GEO,L,Y,0;PRODMILK,L,Z,0;MILKITEM,L,Z,1;INDICATORS,C,Z,2;&zSelection=DS-052400MILKITEM,PRO;DS-052400PRODMILK,MC000;DS-052400INDICATORS,OBS_FLAG;&rankName1=INDICATORS_1_2_-1_2&rankName2=MILKITEM_1_2_-1_2&rankName3=PRODMILK_1_2_-1_2&rankName4=TIME_1_0_0_0&rankName5=GEO_1_2_0_1&sortC=ASC_-1_FIRST&rStp=&cStp=&rDCh=&cDCh=&rDM=true&cDM=true&footnes=false&empty=false&wai=false&time_mode=NONE&time_most_recent=false&lang=EN&cfo=%23%23%23%2C%23%23%23.%23%23%23'
    #bookmark_url = 'PORTER,L,Y,0;PARTNER,L,Z,0;PRODUCT,L,Z,1;FLOW,L,Z,2;INDICATORS,C,Z,3;&zSelection=DS-016894FLOW,2;DS-016894INDICATORS,QUANTITY_IN_100KG;DS-016894PARTNER,AD;DS-016894PRODUCT,0203;&rankName1=PARTNER_1_2_-1_2&rankName2=INDICATORS_1_2_-1_2&rankName3=FLOW_1_2_-1_2&rankName4=PRODUCT_1_2_-1_2&rankName5=PERIOD_1_0_0_0&rankName6=REPORTER_1_2_0_1&sortC=ASC_-1_FIRST&rStp=&cStp=&rDCh=&cDCh=&rDM=true&cDM=true&footnes=false&empty=false&wai=false&time_mode=NONE&time_most_recent=false&lang=EN&cfo=%23%23%23%2C%23%23%23.%23%23%23'
    bookmark_url='http://appsso.eurostat.ec.europa.eu/nui/show.do?query=BOOKMARK_DS-016893_QID_7E3AD81F_UID_-3F171EB0&layout=PERIOD,L,X,0;REPORTER,L,Y,0;PARTNER,L,Z,0;PRODUCT,L,Z,1;FLOW,L,Z,2;INDICATORS,C,Z,3;&zSelection=DS-016893PARTNER,EU28_EXTRA;DS-016893INDICATORS,VALUE_IN_EUROS;DS-016893FLOW,1;DS-016893PRODUCT,040110;&rankName1=PARTNER_1_2_-1_2&rankName2=INDICATORS_1_2_-1_2&rankName3=FLOW_1_2_-1_2&rankName4=PRODUCT_1_2_-1_2&rankName5=PERIOD_1_0_0_0&rankName6=REPORTER_1_2_0_1&sortC=ASC_-1_FIRST&rStp=&cStp=&rDCh=&cDCh=&rDM=true&cDM=true&footnes=false&empty=false&wai=false&time_mode=NONE&time_most_recent=false&lang=EN&cfo=%23%23%23%2C%23%23%23.%23%23%23'
    
    wscraper = WebScraper('Firefox')
    wscraper.open(bookmark_url)
    time.sleep(5)
    
    # open option window
    wscraper.click_button('class', 'selectDataButton')
    time.sleep(1)
    
    # get control of the popup option window
    wscraper.switch_to_popup_window()
    
    if option in ['all', 'partner']:
        # get checkbox ids, codes and labels for partner
        wscraper.click_button('xpath', '//div/a/span[contains(text(),"PARTNER")]')
        time.sleep(1)
        wscraper.get_title_attributes(bookmark_url, dir_path, 'partners')
    
    if option in ['all', 'reporter']:
        # get checkbox ids, codes and labels for reporter
        wscraper.click_button('xpath', '//div/a/span[contains(text(),"REPORTER")]')
        time.sleep(1)
        wscraper.get_title_attributes(bookmark_url, dir_path, 'reporters')
    
    if option in ['all', 'indicator']:
        # get checkbox ids, codes and labels for indicator
        wscraper.click_button('xpath', '//div/a/span[contains(text(),"INDICATORS")]')
        time.sleep(1)
        wscraper.get_title_attributes(bookmark_url, dir_path, 'indicators')
    
    if option in ['all', 'flow']:
        # get checkbox ids, codes and labels for flow
        wscraper.click_button('xpath', '//div/a/span[contains(text(),"FLOW")]')
        time.sleep(1)
        wscraper.get_title_attributes(bookmark_url, dir_path, 'flows')
    
    if option in ['all', 'period']:
        # get checkbox ids, codes and labels for period
        wscraper.click_button('xpath', '//div/a/span[contains(text(),"PERIOD")]')
        time.sleep(1)
        wscraper.get_title_attributes(bookmark_url, dir_path, 'periods')
    
    if option in ['all', 'product']:
        # get checkbox ids, codes and labels for product
        wscraper.click_button('xpath', '//div/a/span[contains(text(),"PRODUCT")]')
        time.sleep(1)
        #wscraper.get_title_attributes(bookmark_url, dir_path, 'products')
        # TODO(Wenchong): scrape products
    
    wscraper.close()
    
    print "finished..."