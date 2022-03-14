'''
Created on 18 Nov 2014

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


ANIMALS_LABELS = []
GEO_LABELS = []
GEO_LIST = []
UNIT_LABELS = []
TIME_LABELS = []
MONTH_LABELS = []

LOG_PATH = EUROSTAT_PATH + 'pig_population_annual.log'
PROGRAM_PATH = './src/scraper/eurostat/pig_population_annual.py'
LABEL_PATH = EUROSTAT_PATH + 'pig_population_annual/title_options/'


def init_labels():
    global UNIT_LABELS
    global TIME_LABELS
    global ANIMALS_LABELS
    global GEO_LABELS
    global GEO_LIST
    global LABEL_PATH
    global MONTH_LABELS
    
    TIME_LABELS = read_from_file('%stime.csv' % LABEL_PATH)
    TIME_LABELS = TIME_LABELS[2:14]
    TIME_LABELS.reverse()
    TIME_LABELS = chunck_list(TIME_LABELS, 12)
    #TIME_LABELS = TIME_LABELS[len(TIME_LABELS) - 8:]
    
    UNIT_LABELS = read_from_file('%sunit.csv' % LABEL_PATH)
    UNIT_LABELS = UNIT_LABELS[2:]
    
    GEO_LABELS = read_from_file('%sgeo.csv' % LABEL_PATH)
    GEO_LIST = [r[1] for r in GEO_LABELS[2:]]
    GEO_LIST.insert(0, 'time')
    
    ANIMALS_LABELS = read_from_file('%sanimals.csv' % LABEL_PATH)
    ANIMALS_LABELS = ANIMALS_LABELS[2:]
    
    MONTH_LABELS = read_from_file('%smonth.csv' % LABEL_PATH)
    MONTH_LABELS = MONTH_LABELS[2:]
    

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
    global UNIT_LABELS
    global TIME_LABELS
    global ANIMALS_LABELS
    global GEO_LABELS
    global GEO_LIST
    global LOG_PATH
    global PROGRAM_PATH
    global MONTH_LABELS
    
    web_driver.get(bookmark_url)
    time.sleep(5)
    
    web_scraper = WebScraper(web_driver)
    
    # open option window
    web_scraper.click_button('selectDataButton', 'class')
    
    # get control of the popup option window
    parent_handle = web_driver.current_window_handle
    handles = web_driver.window_handles
    handles.remove(parent_handle)
    popup_window_handle = handles.pop()
    web_driver.switch_to_window(popup_window_handle)
    
    #web_scraper.click_button('//div/a/span[contains(text(),"PRODMILK")]', 'xpath')
    
    time_list = [[p[1]] for p in TIME_LABELS[0]]
    time_id = [p[0] for p in TIME_LABELS[0]]
    
    # select time by year
    web_scraper.click_checkbox('//div/a/span[contains(text(),"TIME")]',
                               'checkUncheckAllCheckboxTable',
                               '//input[@id="%s"]',
                               time_id)
    
    # update the statistics
    web_scraper.click_button('updateExtractionButton', 'id')
    
    # get control of the updated parent window
    handles = web_driver.window_handles
    parent_handle = handles.pop()
    web_driver.switch_to_window(parent_handle)
    time.sleep(10)
    
    for animal in ANIMALS_LABELS:
        web_scraper.load_field("model.projDimsValuesAvailable['DS-056126ANIMALS']", animal[1], 'list')
        time.sleep(5)
            
        data_list  = []
        
        # get production data sets
        rows = web_driver.find_elements_by_xpath('//td[starts-with(@class, "table_cell column")]')
        for row in rows:
            data_str = str(row.find_element_by_tag_name('div').text).replace(',', '')
            data_list.append(data_str)
        
        # chunck data sets by table row
        num_col = len(time_list)
        data_list = chunck_list(data_list, num_col)
        
        # join times and data sets into rows
        row_list = []
        index = 0
        
        for t in time_list:
            row_list.append(t)
            for dt in data_list:
                row_list[index].append(dt[index])
            index += 1
        
        file_path = '%s%s_%s_%s.csv' % (dir_path, animal[1], MONTH_LABELS[-1][1], UNIT_LABELS[0][1])
        web_scraper.save_to_file(file_path, bookmark_url, GEO_LIST, row_list)
        
        '''
        Don't ask me why I put the following code to release the memory while I don't
        put it in its sibling code, pig_meat_trade.py for example, because I have no
        idea why I should do this. Otherwise, the same data will be accumulated again
        and again and again. If anyone figures it out, please please let me know!!!
        '''
        for r in row_list:
            r[1:] = []



if __name__ == '__main__':
    
    dir_title = datetime.now().strftime('%Y_%m_%d')
    dir_path = EUROSTAT_PATH + 'pig_population_annual/'
    dir_path = create_directory(dir_path, dir_title)
    
    date_from = '01/01/2007'
    date_to = datetime.now().strftime('%d/%m/%Y')
    
    bookmark_url = 'http://appsso.eurostat.ec.europa.eu/nui/show.do?query=BOOKMARK_DS-056126_QID_-23899AE9_UID_-3F171EB0&layout=TIME,C,X,0;GEO,L,Y,0;ANIMALS,L,Z,0;MONTH,L,Z,1;UNIT,L,Z,2;INDICATORS,C,Z,3;&zSelection=DS-056126UNIT,THS_HD;DS-056126INDICATORS,OBS_FLAG;DS-056126MONTH,M12;DS-056126ANIMALS,A3100;&rankName1=UNIT_1_2_-1_2&rankName2=INDICATORS_1_2_-1_2&rankName3=ANIMALS_1_2_-1_2&rankName4=MONTH_1_2_-1_2&rankName5=TIME_1_0_0_0&rankName6=GEO_1_2_0_1&sortC=ASC_-1_FIRST&rStp=&cStp=&rDCh=&cDCh=&rDM=true&cDM=true&footnes=false&empty=false&wai=false&time_mode=NONE&time_most_recent=false&lang=EN&cfo=%23%23%23%2C%23%23%23.%23%23%23'

    # initialise option field labels
    init_labels()

    # open parent window by bookmark url
    wdriver = webdriver.Firefox()
    
    # start scraping
    print 'start scraping'
    scraping(wdriver, 0, 0, 0, dir_path, bookmark_url)
    
    wdriver.quit()
    
    print 'finished...'
    


