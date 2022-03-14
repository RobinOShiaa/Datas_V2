'''
Created on 14 Nov 2014

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


PRODMILK_LABELS = []  # PARTNER
TIME_LABELS = []  # PERIOD
UNIT_LABELS = []  # INDICATOR
GEO_LABELS = []  # REPORTER
GEO_LIST = []

LOG_PATH = EUROSTAT_PATH + 'cows_milk_monthly.log'
PROGRAM_PATH = './src/scraper/eurostat/cows_milk_monthly.py'
LABEL_PATH = EUROSTAT_PATH + 'cows_milk_monthly/title_options/'


def init_labels():
    global PRODMILK_LABELS
    global TIME_LABELS
    global UNIT_LABELS
    global GEO_LABELS
    global GEO_LIST
    global LABEL_PATH
    
    TIME_LABELS = read_from_file('%stime.csv' % LABEL_PATH)
    TIME_LABELS = TIME_LABELS[2:14]
    TIME_LABELS.reverse()
    TIME_LABELS = chunck_list(TIME_LABELS, 12)
    #TIME_LABELS = TIME_LABELS[len(TIME_LABELS) - 8:]
    
    PRODMILK_LABELS = read_from_file('%sprodmilk.csv' % LABEL_PATH)
    PRODMILK_LABELS = PRODMILK_LABELS[2:]
    
    GEO_LABELS = read_from_file('%sgeo.csv' % LABEL_PATH)
    GEO_LIST = [r[1] for r in GEO_LABELS[2:]]
    GEO_LIST.insert(0, 'time')
    
    UNIT_LABELS = read_from_file('%sunit.csv' % LABEL_PATH)
    UNIT_LABELS = UNIT_LABELS[2:]


def write_to_log(file_path, data_list):
    out_file = None
    
    if os.path.isfile(file_path):
        out_file = open(file_path, 'a')
    else:
        out_file = open(file_path, 'w')
    
    for d in data_list:
        out_file.write(d)
        out_file.write('\n')
    
    out_file.write('\n\n')
    
    out_file.close()


def scraping(web_driver, prodmilk_point, time_point, milkitem_point,
             dir_path, bookmark_url):
    global PRODMILK_LABELS
    global TIME_LABELS
    global UNIT_LABELS
    global GEO_LABELS
    global GEO_LIST
    global LOG_PATH
    global PROGRAM_PATH
    
    web_driver.get(bookmark_url)
    time.sleep(5)
    
    web_scraper = WebScraper(web_driver)
    
    time_list = [[[d] for d in label] for label in TIME_LABELS[0]]
    time_list = [t[2:] for t in time_list]
    time_id = [t[1] for t in TIME_LABELS[0]]
    
    previous_tid = '2014'
    for tid in time_id:
        # open option window
        web_scraper.click_button('selectDataButton', 'class')
        
        # get control of the popup option window
        parent_handle = web_driver.current_window_handle
        handles = web_driver.window_handles
        handles.remove(parent_handle)
        popup_window_handle = handles.pop()
        web_driver.switch_to_window(popup_window_handle)
        
        # open TIME tag to select time
        web_scraper.click_button('//div/a/span[contains(text(),"TIME")]', 'xpath')
        time.sleep(1)
        
        # select a given time
        web_scraper.click_button('//li/a[contains(text(), "%s")]' % (tid), 'xpath')
        time.sleep(1)
        
        # unselect the previous time
        web_scraper.click_button('//li/a[contains(text(), "%s")]' % (previous_tid), 'xpath')
        time.sleep(1)
        previous_tid = tid
        
        # update the statistics
        web_scraper.click_button('updateExtractionButton', 'id')
        
        # get control of the updated parent window
        handles = web_driver.window_handles
        parent_handle = handles.pop()
        web_driver.switch_to_window(parent_handle)
        time.sleep(10)
        
        for prodmilk in PRODMILK_LABELS:
            web_scraper.load_field("model.projDimsValuesAvailable['DS-055514PRODMILK']", prodmilk[1], 'list')
            time.sleep(3)
            
            for unit in UNIT_LABELS:
                web_scraper.load_field("model.projDimsValuesAvailable['DS-055514UNIT']", unit[1], 'list')
                time.sleep(5)
                
                data_list  = []
                
                # get production data sets
                rows = web_driver.find_elements_by_xpath('//td[starts-with(@class, "table_cell column")]')
                for row in rows:
                    data_str = str(row.find_element_by_tag_name('div').text).replace(',', '')
                    data_list.append(data_str)
                
                # chunck data sets by table row
                num_col = len(time_list[0])
                data_list = chunck_list(data_list, num_col)
                
                # join times and data sets into rows
                row_list = []
                index = 0
                
                for t in time_list[time_id.index(tid)]:
                    row_list.append(t)
                    for d in data_list:
                        row_list[index].append(d[index])
                    index += 1
                
                file_path = '%s%s_%s_%s.csv' % (dir_path, tid, prodmilk[1], unit[1])
                web_scraper.save_to_file(file_path, bookmark_url, GEO_LIST, row_list)
                
                '''
                Don't ask me why I put the following code to release the memory while I don't
                put it in its sibling code, pig_meat_trade.py for example, because I have no
                idea why I should do this. Otherwise, the same data will be accumulated again
                and again and again. If anyone figures it out, please please let me know!!!
                '''
                for r in row_list:
                    r[1:] = []
            # end of inner for-loop
        # end of middle for-loop
    # end of outer for-loop



if __name__ == '__main__':
    
    dir_title = datetime.now().strftime('%Y_%m_%d') + '_by_year'
    dir_path = EUROSTAT_PATH + 'cows_milk_monthly/'
    dir_path = create_directory(dir_path, dir_title)
    
    date_from = '01/01/2007'
    date_to = datetime.now().strftime('%d/%m/%Y')
    
    # this bookmark_url selects all geo, prodmilk and unit, time 1968 selected
    bookmark_url = 'http://appsso.eurostat.ec.europa.eu/nui/show.do?query=BOOKMARK_DS-055514_QID_-210671E6_UID_-3F171EB0&layout=TIME,C,X,0;GEO,L,Y,0;PRODMILK,L,Z,0;UNIT,L,Z,1;INDICATORS,C,Z,2;&zSelection=DS-055514PRODMILK,MM001;DS-055514UNIT,THS_T;DS-055514INDICATORS,OBS_FLAG;&rankName1=UNIT_1_2_-1_2&rankName2=INDICATORS_1_2_-1_2&rankName3=PRODMILK_1_2_-1_2&rankName4=TIME_1_0_0_0&rankName5=GEO_1_2_0_1&sortC=ASC_-1_FIRST&rStp=&cStp=&rDCh=&cDCh=&rDM=true&cDM=true&footnes=false&empty=false&wai=false&time_mode=NONE&time_most_recent=false&lang=EN&cfo=%23%23%23%2C%23%23%23.%23%23%23'

    # initialise option field labels
    init_labels()

    # open parent window by bookmark url
    wdriver = webdriver.Firefox()
    
    # start scraping
    print 'start scraping'
    scraping(wdriver, 0, 0, 0, dir_path, bookmark_url)
    
    wdriver.quit()
    
    print 'finished...'
    


