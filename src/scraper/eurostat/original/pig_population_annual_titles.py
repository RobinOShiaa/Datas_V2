'''
Created on 18 Nov 2014

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
    dir_path = create_directory(EUROSTAT_PATH, 'pig_population_annual/title_options')
    bookmark_url = 'http://appsso.eurostat.ec.europa.eu/nui/show.do?query=BOOKMARK_DS-056126_QID_-23899AE9_UID_-3F171EB0&layout=TIME,C,X,0;GEO,L,Y,0;ANIMALS,L,Z,0;MONTH,L,Z,1;UNIT,L,Z,2;INDICATORS,C,Z,3;&zSelection=DS-056126UNIT,THS_HD;DS-056126INDICATORS,OBS_FLAG;DS-056126MONTH,M12;DS-056126ANIMALS,A3100;&rankName1=UNIT_1_2_-1_2&rankName2=INDICATORS_1_2_-1_2&rankName3=ANIMALS_1_2_-1_2&rankName4=MONTH_1_2_-1_2&rankName5=TIME_1_0_0_0&rankName6=GEO_1_2_0_1&sortC=ASC_-1_FIRST&rStp=&cStp=&rDCh=&cDCh=&rDM=true&cDM=true&footnes=false&empty=false&wai=false&time_mode=NONE&time_most_recent=false&lang=EN&cfo=%23%23%23%2C%23%23%23.%23%23%23'
    
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
    
    # get checkbox ids, codes and labels for animals
    wscraper.click_button('xpath', '//div/a/span[contains(text(),"ANIMALS")]')
    time.sleep(1)
    wscraper.get_title_attributes(bookmark_url, dir_path, 'animals')
    
    # get checkbox ids, codes and labels for geo
    wscraper.click_button('xpath', '//div/a/span[contains(text(),"GEO")]')
    time.sleep(1)
    wscraper.get_title_attributes(bookmark_url, dir_path, 'geo')
    
    # get checkbox ids, codes and labels for month
    wscraper.click_button('xpath', '//div/a/span[contains(text(),"MONTH")]')
    time.sleep(1)
    wscraper.get_title_attributes(bookmark_url, dir_path, 'month')
    
    # get checkbox ids, codes and labels for time
    wscraper.click_button('xpath', '//div/a/span[contains(text(),"TIME")]')
    time.sleep(1)
    wscraper.get_title_attributes(bookmark_url, dir_path, 'time')
    
    # get checkbox ids, codes and labels for unit
    wscraper.click_button('xpath', '//div/a/span[contains(text(),"UNIT")]')
    time.sleep(1)
    wscraper.get_title_attributes(bookmark_url, dir_path, 'unit')
    
    
    
    browser.quit()
    
    
    print "finished..."



