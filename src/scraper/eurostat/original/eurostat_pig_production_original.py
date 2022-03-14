'''
Created on 7 Oct 2014

@author: Wenchong
'''


import re
import os
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from datetime import datetime
from datas.functions.functions import *
from datas.web.scraper import *


"""
-------------------------------------------------------------
start scraping
-------------------------------------------------------------
"""
'''
variables for options to be filled in to the web form
'''
dir_path = './../../output/eurostat/'
dir_title = datetime.now().strftime('%Y_%m_%d')

delete_directory('%s%s/' % (dir_path, dir_title))
dir_path = create_directory(dir_path, dir_title)

date_from = '01/01/2007'
date_to = datetime.now().strftime('%d/%m/%Y')

# partners part 1
bookmark_url = 'http://appsso.eurostat.ec.europa.eu/nui/show.do?query=BOOKMARK_DS-016894_QID_-D77E409_UID_-3F171EB0&layout=PERIOD,L,X,0;REPORTER,L,Y,0;PARTNER,L,Z,0;PRODUCT,L,Z,1;FLOW,L,Z,2;INDICATORS,C,Z,3;&zSelection=DS-016894FLOW,2;DS-016894PARTNER,CN;DS-016894PRODUCT,0203;DS-016894INDICATORS,QUANTITY_IN_100KG;&rankName1=PARTNER_1_2_-1_2&rankName2=PRODUCT_1_2_-1_2&rankName3=FLOW_1_2_-1_2&rankName4=INDICATORS_1_2_-1_2&rankName5=PERIOD_1_0_0_0&rankName6=REPORTER_1_2_0_1&sortC=ASC_-1_FIRST&rStp=&cStp=&rDCh=&cDCh=&rDM=true&cDM=true&footnes=false&empty=false&wai=false&time_mode=NONE&time_most_recent=false&lang=EN&cfo=%23%23%23%2C%23%23%23.%23%23%23'

# partners part 2
#bookmark_url = 'http://appsso.eurostat.ec.europa.eu/nui/show.do?query=BOOKMARK_DS-016894_QID_33ADC01D_UID_-3F171EB0&layout=PERIOD,L,X,0;REPORTER,L,Y,0;PARTNER,L,Z,0;PRODUCT,L,Z,1;FLOW,L,Z,2;INDICATORS,C,Z,3;&zSelection=DS-016894FLOW,2;DS-016894PARTNER,US;DS-016894PRODUCT,0203;DS-016894INDICATORS,QUANTITY_IN_100KG;&rankName1=PARTNER_1_2_-1_2&rankName2=PRODUCT_1_2_-1_2&rankName3=FLOW_1_2_-1_2&rankName4=INDICATORS_1_2_-1_2&rankName5=PERIOD_1_0_0_0&rankName6=REPORTER_1_2_0_1&sortC=ASC_-1_FIRST&rStp=&cStp=&rDCh=&cDCh=&rDM=true&cDM=true&footnes=false&empty=false&wai=false&time_mode=NONE&time_most_recent=false&lang=EN&cfo=%23%23%23%2C%23%23%23.%23%23%23'

years = ['2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014']
months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

reporter_labels = []
partner_labels = []
flow_labels = []
product_labels = []
indicator_labels = []
period_labels = union_list(years, months, 'ck_')


# scrape data by every 12 months
for label in period_labels:
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
    
    # select the given 12 months under Period label
    wscraper.click_button('//div/a/span[contains(text(),"PERIOD")]', 'xpath')
    time.sleep(1)
    
    wscraper.click_button('checkUncheckAllCheckboxTable', 'id')
    time.sleep(1)
    wscraper.click_button('checkUncheckAllCheckboxTable', 'id')
    time.sleep(1)
    
    for la in label:
        wscraper.click_button('//input[@id="%s"]' % (la), 'xpath')
    
    '''
    TODO(Wenchong): fill in options to the popup window
    '''
    
    # update the statistics
    wscraper.click_button('updateExtractionButton', 'id')
    
    '''
    TODO(Wenchong): wait until statistics is updated
    '''
    time.sleep(10)
    
    # get control of the updated parent window
    handles = browser.window_handles
    parent_handle = handles.pop()
    browser.switch_to_window(parent_handle)
    
    # variables for storing data from web
    indicator_list = wscraper.get_dropdown_list('selectid_3')
    partner_list = wscraper.get_dropdown_list('selectid_0')
    
    
    for indicator in indicator_list:
        wscraper.load_field('projDimsValuesAvailableValue(DS-016894INDICATORS)', indicator, 'list')
        time.sleep(5)
        
        for partner in partner_list:
            wscraper.load_field('projDimsValuesAvailableValue(DS-016894PARTNER)', partner, 'list')
            time.sleep(5)
            
            period_list  = []
            data_list  = []
            country_list = []
            
            # get periods and reporter countries
            # TODO(Wenchong): move this block out of the for loops
            headers = browser.find_elements_by_xpath('//span[starts-with(@id, "LABEL_")]')
            for header in headers:
                res = str(header.get_attribute('title'))
                mat = re.match('^\d+ - [A-Z][a-z]+. \d+$', res)
                if mat:
                    period_list.append([res])
                else:
                    country_list.append(res)
            
            time.sleep(10)
            
            # get production data sets
            rows = browser.find_elements_by_xpath('//td[starts-with(@class, "table_cell column")]')
            for row in rows:
                data_str = str(row.find_element_by_tag_name('div').text).replace(',', '')
                data_list.append(data_str)
            
            # chunck data sets by table row
            num_col = len(period_list)
            data_list = chunck_list(data_list, num_col)
            
            # join periods and data sets into rows
            #row_list = join_list(period_list, data_list)
            row_list = []
            index = 0
            for p in period_list:
                row_list.append(p)
                for d in data_list:
                    row_list[index].append(d[index])
                index += 1
            
            # write all data to file
            file_path = '%sPIG_%s_%s.csv' % (dir_path, partner, indicator)
            out_file = None
            
            if os.path.isfile(file_path):
                out_file = open(file_path, 'a')
            else:
                out_file = open(file_path, 'w')
                out_file.write(', '.join(country_list))
                out_file.write('\n')
            
            for row in row_list:
                out_file.write(', '.join(row))
                out_file.write('\n')
            out_file.close()
        # end of inner for loop
    # end of middle for loop
    browser.quit()
# end of outer for loop





print "finished..."



