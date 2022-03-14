'''
Created on 12 Nov 2014

@author: Wenchong

25/11/2014: Fixed excluding some areas problem found during
the QA on 25/11/2014. The symbol ',' in the title labels are
replaced with symbol '/'.
'''


import time
from datas.function.function import create_directory
from datas.web.path import WEB_EUROSTAT_PATH
from datas.web.scraper import WebScraper


def get_titles(option='all'):
    dir_path = create_directory(WEB_EUROSTAT_PATH, 'milk_prod_util_annual/title_options')
    bookmark_url = 'http://appsso.eurostat.ec.europa.eu/nui/show.do?query=BOOKMARK_DS-052400_QID_7343C90B_UID_-3F171EB0&layout=TIME,C,X,0;GEO,L,Y,0;PRODMILK,L,Z,0;MILKITEM,L,Z,1;INDICATORS,C,Z,2;&zSelection=DS-052400PRODMILK,MC000;DS-052400MILKITEM,PRO;DS-052400INDICATORS,OBS_FLAG;&rankName1=PRODMILK_1_2_-1_2&rankName2=MILKITEM_1_2_-1_2&rankName3=INDICATORS_1_2_-1_2&rankName4=TIME_1_0_0_0&rankName5=GEO_1_2_0_1&sortC=ASC_-1_FIRST&rStp=&cStp=&rDCh=&cDCh=&rDM=true&cDM=true&footnes=false&empty=false&wai=false&time_mode=NONE&time_most_recent=false&lang=EN&cfo=%23%23%23%2C%23%23%23.%23%23%23'
    
    # open parent window by bookmark url
    wscraper = WebScraper('Chrome')
    wscraper.open(bookmark_url)
    time.sleep(5)
    
    # open option window
    wscraper.click_button('class', 'selectDataButton')
    time.sleep(1)
    
    # get control of the popup option window
    wscraper.switch_to_popup_window()
    
    if option in ['all', 'geo']:
        # get checkbox ids, codes and labels for geo
        wscraper.click_button('xpath', '//div/a/span[contains(text(),"GEO")]')
        time.sleep(1)
        wscraper.get_title_attributes(bookmark_url, dir_path, 'geo')
    
    if option in ['all', 'milkitem']:
        # get checkbox ids, codes and labels for milkitem
        wscraper.click_button('xpath', '//div/a/span[contains(text(),"MILKITEM")]')
        time.sleep(1)
        wscraper.get_title_attributes(bookmark_url, dir_path, 'milkitem')
        
    if option in ['all', 'prodmilk']:
        # get checkbox ids, codes and labels for prodmilk
        wscraper.click_button('xpath', '//div/a/span[contains(text(),"PRODMILK")]')
        time.sleep(1)
        wscraper.get_title_attributes(bookmark_url, dir_path, 'prodmilk')
        
    if option in ['all', 'time']:
        # get checkbox ids, codes and labels for time
        wscraper.click_button('xpath', '//div/a/span[contains(text(),"TIME")]')
        time.sleep(1)
        wscraper.get_title_attributes(bookmark_url, dir_path, 'time')
        
    wscraper.close()
    
    print "finished..."

if __name__ == '__main__':
    get_titles('all')

