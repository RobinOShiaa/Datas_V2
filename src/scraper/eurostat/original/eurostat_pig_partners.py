'''
Created on 5 Nov 2014

@author: Wenchong
'''


import time
from selenium import webdriver
from datas.web.scraper import *
from datas.functions.functions import *


"""
-------------------------------------------------------------
start scraping
-------------------------------------------------------------
"""
# variables for options to be filled in to the web form
partners = []
bookmark_url = 'http://appsso.eurostat.ec.europa.eu/nui/show.do?query=BOOKMARK_DS-016894_QID_2F63A93A_UID_-3F171EB0&layout=PERIOD,L,X,0;REPORTER,L,Y,0;PARTNER,L,Z,0;PRODUCT,L,Z,1;FLOW,L,Z,2;INDICATORS,C,Z,3;&zSelection=DS-016894FLOW,2;DS-016894PARTNER,CN;DS-016894PRODUCT,0203;DS-016894INDICATORS,QUANTITY_IN_100KG;&rankName1=PARTNER_1_2_-1_2&rankName2=PRODUCT_1_2_-1_2&rankName3=FLOW_1_2_-1_2&rankName4=INDICATORS_1_2_-1_2&rankName5=PERIOD_1_0_0_0&rankName6=REPORTER_1_2_0_1&sortC=ASC_-1_FIRST&rStp=&cStp=&rDCh=&cDCh=&rDM=true&cDM=true&footnes=false&empty=false&wai=false&time_mode=NONE&time_most_recent=false&lang=EN&cfo=%23%23%23%2C%23%23%23.%23%23%23'

# open parent window by bookmark url
browser = webdriver.Firefox()
browser.get(bookmark_url)
wscraper = WebScraper(browser)

# open option window
wscraper.click_button('selectDataButton', 'class')

# get control of the popup option window
parent_handle = browser.current_window_handle
handles = browser.window_handles
handles.remove(parent_handle)
popup_window_handle = handles.pop()
browser.switch_to_window(popup_window_handle)

wscraper.click_button('//div/a/span[contains(text(),"PARTNER")]', 'xpath')
time.sleep(1)


# get checkbox id, region_code2 and region abbr_name
region_tags = browser.find_elements_by_xpath('//td/input[starts-with(@id, "ck_")]')
region_checkbox = [[str(r.get_attribute('id'))] for r in region_tags]

region_tags = browser.find_elements_by_xpath('//td/label[starts-with(@for, "ck_")]')
region_code2 = [[str(r.text)] for r in region_tags]

region_tags = browser.find_elements_by_tag_name('td')
region_name = [[str(r.text)] for r in region_tags if r.get_attribute('title')]

browser.quit()

regions = join_list(region_checkbox, region_code2)
regions = join_list(regions, region_name)


removes = [r for r in regions if len(r[1]) != 2]
for r in removes:
    regions.remove(r)

regions.insert(0, ['url', bookmark_url])
regions.insert(1, ['checkbox_id', 'region_code2', 'abbr_name'])

file_path = './../../output/eurostat/partners.csv'
delete_file(file_path)
save_to_file(regions, file_path)



print "finished..."



