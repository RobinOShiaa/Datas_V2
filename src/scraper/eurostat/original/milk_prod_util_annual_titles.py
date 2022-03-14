'''
Created on 14 Nov 2014

@author: Wenchong

26/11/2014: Fixed excluding some areas problem found during
the QA on 25/11/2014. The symbol ',' in the title labels are
replaced with symbol '/'.
'''


import time
from selenium import webdriver
from datas.web.scraper import *
from datas.functions.functions import *


if __name__ == '__main__':
    dir_path = create_directory(EUROSTAT_PATH, 'milk_prod_util_annual/title_options')
    bookmark_url = 'http://appsso.eurostat.ec.europa.eu/nui/show.do?query=BOOKMARK_DS-052668_QID_-5B77CB67_UID_-3F171EB0&layout=TIME,C,X,0;GEO,L,Y,0;PRODMILK,L,Z,0;MILKITEM,L,Z,1;INDICATORS,C,Z,2;&zSelection=DS-052668PRODMILK,MF000;DS-052668MILKITEM,PRO;DS-052668INDICATORS,OBS_FLAG;&rankName1=INDICATORS_1_2_-1_2&rankName2=MILKITEM_1_2_-1_2&rankName3=PRODMILK_1_2_-1_2&rankName4=TIME_1_0_0_0&rankName5=GEO_1_2_0_1&sortC=ASC_-1_FIRST&rStp=&cStp=&rDCh=&cDCh=&rDM=true&cDM=true&footnes=false&empty=false&wai=false&time_mode=NONE&time_most_recent=false&lang=EN&cfo=%23%23%23%2C%23%23%23.%23%23%23'
    
    # open parent window by bookmark url
    browser = webdriver.Firefox()
    browser.get(bookmark_url)
    time.sleep(5)
    
    wscraper = WebScraper(browser)
    
    # open option window
    wscraper.click_button('class', 'selectDataButton')
    time.sleep(1)
    
    # get control of the popup option window
    parent_handle = browser.current_window_handle
    handles = browser.window_handles
    handles.remove(parent_handle)
    popup_window_handle = handles.pop()
    browser.switch_to_window(popup_window_handle)
    
    # get checkbox ids, codes and labels for geo
    wscraper.click_button('xpath', '//div/a/span[contains(text(),"GEO")]')
    time.sleep(1)
    wscraper.get_title_attributes(bookmark_url, dir_path, 'geo')
    
    # get checkbox ids, codes and labels for milkitem
    wscraper.click_button('xpath', '//div/a/span[contains(text(),"MILKITEM")]')
    time.sleep(1)
    wscraper.get_title_attributes(bookmark_url, dir_path, 'milkitem')
    
    # get checkbox ids, codes and labels for prodmilk
    wscraper.click_button('xpath', '//div/a/span[contains(text(),"PRODMILK")]')
    time.sleep(1)
    wscraper.get_title_attributes(bookmark_url, dir_path, 'prodmilk')
    
    # get checkbox ids, codes and labels for time
    wscraper.click_button('xpath', '//div/a/span[contains(text(),"TIME")]')
    time.sleep(1)
    wscraper.get_title_attributes(bookmark_url, dir_path, 'time')
    
    
    browser.quit()
    
    
    print "finished..."



