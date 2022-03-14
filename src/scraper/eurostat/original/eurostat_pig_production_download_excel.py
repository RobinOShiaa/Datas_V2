'''
Created on 7 Oct 2014

@author: Wenchong
'''


import re
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from datetime import datetime
import urllib


def load_field(field_name, value, choice):
    if choice == 'list':
        element = browser.find_element_by_name(field_name)
        select= Select(element)
        select.select_by_value(value)
    if choice == 'date':
        element = browser.find_element_by_name(field_name)
        element.send_keys(value)
        
def button_click(attr, choice):
    if choice == 'name':
        browser.find_element_by_name(attr).click()
    elif choice == 'class':
        browser.find_element_by_class_name(attr).click()
    elif choice == 'id':
        browser.find_element_by_id(attr).click()
    elif choice == 'xpath':
        browser.find_element_by_xpath(attr).click()
    elif choice == 'link_text':
        browser.find_element_by_link_text(attr).click()


'''
start scraping
'''
countries = []
options = ['', '', '', '']
dateFrom = '01/01/2007'
dateTo = datetime.now().strftime('%d/%m/%Y')
bookmark_url = 'http://appsso.eurostat.ec.europa.eu/nui/show.do?query=BOOKMARK_DS-016894_QID_-789BAC11_UID_-3F171EB0&layout=PERIOD,L,X,0;REPORTER,L,Y,0;PARTNER,L,Z,0;PRODUCT,L,Z,1;FLOW,L,Z,2;INDICATORS,C,Z,3;&zSelection=DS-016894FLOW,2;DS-016894PARTNER,RU;DS-016894PRODUCT,0203;DS-016894INDICATORS,QUANTITY_IN_100KG;&rankName1=PARTNER_1_2_-1_2&rankName2=PRODUCT_1_2_-1_2&rankName3=FLOW_1_2_-1_2&rankName4=INDICATORS_1_2_-1_2&rankName5=PERIOD_1_0_0_0&rankName6=REPORTER_1_2_0_1&sortC=ASC_-1_FIRST&rStp=&cStp=&rDCh=&cDCh=&rDM=true&cDM=true&footnes=false&empty=false&wai=false&time_mode=NONE&time_most_recent=false&lang=EN&cfo=%23%23%23%2C%23%23%23.%23%23%23'

# disable file download dialog window
profile = webdriver.FirefoxProfile()

#profile.native_events_enabled = True
profile.set_preference('browser.download.folderList', 2) # custom location
profile.set_preference('browser.download.manager.showWhenStarting', False)
profile.set_preference('browser.download.dir', './../../output/bordbia/')
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/plain, application/vnd.ms-excel, text/csv, text/comma-separated-values, application/octet-stream, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/msexcel')
profile.set_preference("browser.helperApps.alwaysAsk.force", False);
profile.set_preference('browser.download.panel.shown', False)
profile.update_preferences()


# open parent window by bookmark url
browser = webdriver.Firefox(profile)
browser.get(bookmark_url)

# open option window
button_click('selectDataButton', 'class')

# get control of the popup option window
parent_handle = browser.current_window_handle
handles = browser.window_handles
handles.remove(parent_handle)
popup_window_handle = handles.pop()
browser.switch_to_window(popup_window_handle)

'''
TODO: fill in your options to the popup window here
'''
##### enter your code here

# update the statistics
button_click('updateExtractionButton', 'id')

'''
TODO: wait until statistics is updated
'''
##### enter your code here
time.sleep(10)

# get control of the updated parent window
handles = browser.window_handles
parent_handle = handles.pop()
browser.switch_to_window(parent_handle)

# open the download window
#button_click('download', 'class')
#browser.find_element_by_class_name('download').click()
button_click('//a[@href="/nui/setupDownloads.do"]', 'xpath')
time.sleep(5)
'''
download_page_url = browser.current_url
browser.implicitly_wait(5)
browser.get(download_page_url)
print download_page_url'''


'''
# disable file download dialog window
profile = webdriver.FirefoxProfile()

#profile.native_events_enabled = True
profile.set_preference('browser.download.folderList', 2) # custom location
profile.set_preference('browser.download.manager.showWhenStarting', False)
profile.set_preference('browser.download.dir', './../../output/bordbia/')
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/plain, application/vnd.ms-excel, text/csv, text/comma-separated-values, application/octet-stream, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/msexcel')
profile.set_preference("browser.helperApps.alwaysAsk.force", False);
profile.set_preference('browser.download.panel.shown', False)
profile.update_preferences()


browser2 = webdriver.Firefox(profile)
browser2.get(download_page_url)
'''


# select options for file format
button_click('//input[@id="excelFULL_EXTRACTION"]', 'xpath')
#browser2.find_element_by_xpath('//input[@id="excelFULL_EXTRACTION"]').click()


'''
downloading file here
'''
button_click('//input[@value="Download in Excel Format"]', 'xpath')
#browser2.find_element_by_xpath('//input[@value="Download in Excel Format"]').click()


#browser.quit()


print "finished..."



