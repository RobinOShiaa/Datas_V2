'''
Created on 11 Nov 2014

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
MILKITEM_LABELS = []  # INDICATOR
GEO_LABELS = []  # REPORTER
GEO_LIST = []

LOG_PATH = EUROSTAT_PATH + 'milk_dairy_annual.log'
PROGRAM_PATH = './src/scraper/eurostat/milk_dairy_annual.py'
LABEL_PATH = EUROSTAT_PATH + 'milk_dairy_annual/title_options/'


def init_labels():
    global PRODMILK_LABELS
    global TIME_LABELS
    global MILKITEM_LABELS
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
    
    MILKITEM_LABELS = read_from_file('%smilkitem.csv' % LABEL_PATH)
    MILKITEM_LABELS = MILKITEM_LABELS[2:]


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
    global MILKITEM_LABELS
    global GEO_LABELS
    global GEO_LIST
    global LOG_PATH
    global PROGRAM_PATH
    
    web_driver.get(bookmark_url)
    time.sleep(5)
    
    web_scraper = WebScraper(web_driver)
    
    prodmilk_point_labels = PRODMILK_LABELS[prodmilk_point:]
    time_point_labels = TIME_LABELS[time_point:]
    milkitem_point_labels = MILKITEM_LABELS[milkitem_point:]
    
    # scrape data by every 12 months
    for prodmilk in prodmilk_point_labels:
        # use list of list for prodmilk_list and parter in case of scraping
        # for multiple prodmilks at a time in the future
        prodmilk_list = [prodmilk[1]]
        prodmilk_id = [prodmilk[0]]
        is_prodmilk_selected = False
        
        if prodmilk_point_labels.index(prodmilk) != 0:
            time_point_labels = TIME_LABELS[0:]
        
        for ptime in time_point_labels:
            try:
                time_list = [[p[1]] for p in ptime]
                time_id = [p[0] for p in ptime]
                
                # open option window
                web_scraper.click_button('selectDataButton', 'class')
                
                # get control of the popup option window
                parent_handle = web_driver.current_window_handle
                handles = web_driver.window_handles
                handles.remove(parent_handle)
                popup_window_handle = handles.pop()
                web_driver.switch_to_window(popup_window_handle)
                
                web_scraper.click_button('//div/a/span[contains(text(),"PRODMILK")]', 'xpath')
                
                # TODO(Wenchong): fill in options to the popup window
                # select the given 12 months under Period label
                web_scraper.click_checkbox('//div/a/span[contains(text(),"TIME")]',
                                           'checkUncheckAllCheckboxTable',
                                           '//input[@id="%s"]',
                                           time_id)
                
                # select the current prodmilk
                if not is_prodmilk_selected:
                    is_prodmilk_selected = True
                    web_scraper.click_checkbox('//div/a/span[contains(text(),"PRODMILK")]',
                                               'checkUncheckAllCheckboxTable',
                                               '//input[@id="%s"]',
                                               prodmilk_id)
                
                # update the statistics
                web_scraper.click_button('updateExtractionButton', 'id')
                
                # TODO(Wenchong): wait until statistics is updated
                #time.sleep(1)
                
                # get control of the updated parent window
                handles = web_driver.window_handles
                parent_handle = handles.pop()
                web_driver.switch_to_window(parent_handle)
            except Exception as e:
                info = [datetime.now().strftime('UTC: %Y-%m-%d %H:%M:%S')]
                info.append(PROGRAM_PATH)
                info.append('Error %s' % e)
                info.append('Resumed from crash point at prodmilk %s, time %s' % (prodmilk[1], ptime[0][1]))
                write_to_log(LOG_PATH, info)
                
                prodmilk_point = PRODMILK_LABELS.index(prodmilk)
                time_point = TIME_LABELS.index(ptime)
                milkitem_point = 0
                
                #web_driver.close()
                
                scraping(web_driver, prodmilk_point, time_point, milkitem_point,
                         dir_path, bookmark_url)
            
            if time_point_labels.index(ptime) != 0:
                milkitem_point_labels = MILKITEM_LABELS[0:]
            
            # get production in weigh and value
            for milkitem in milkitem_point_labels:
                try:
                    data_list  = []
                    
                    #web_scraper.load_field('projDimsValuesAvailable(DS-052400MILKITEM)', milkitem[1], 'list')
                    web_scraper.load_field("model.projDimsValuesAvailable['DS-052400MILKITEM']", milkitem[1], 'list')
                    time.sleep(5)
                    
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
                except Exception as e:
                    info = [datetime.now().strftime('UTC: %Y-%m-%d %H:%M:%S')]
                    info.append(PROGRAM_PATH)
                    info.append('Error %s' % e)
                    info.append('Resumed from crash point at prodmilk %s, time %s, milkitem %s' % (prodmilk[1], ptime[0][1], milkitem[1]))
                    write_to_log(LOG_PATH, info)
                    
                    prodmilk_point = PRODMILK_LABELS.index(prodmilk)
                    time_point = TIME_LABELS.index(ptime)
                    milkitem_point = MILKITEM_LABELS.index(milkitem)
                    
                    #web_driver.close()
                    
                    scraping(web_driver, prodmilk_point, time_point, milkitem_point,
                             dir_path, bookmark_url)
                else:
                    # write all data to file
                    file_path = '%s%s_%s.csv' % (dir_path, prodmilk_list[0], milkitem[1])
                    web_scraper.save_to_file(file_path, bookmark_url, GEO_LIST, row_list)
                    
                    '''
                    Don't ask me why I put the following code to release the memory while I don't
                    put it in its sibling code, pig_meat_trade.py for example, because I have no
                    idea why I should do this. Otherwise, the same data will be accumulated again
                    and again and again. If anyone figures it out, please please let me know!!!
                    '''
                    for r in row_list:
                        r[1:] = []
            # end of inner for: indicators
        # end of middle for loop: times
    # end of outer for loop: prodmilks


if __name__ == '__main__':
    
    dir_title = datetime.now().strftime('%Y_%m_%d')
    dir_path = EUROSTAT_PATH + 'milk_dairy_annual/'
    dir_path = create_directory(dir_path, dir_title)
    
    date_from = '01/01/2007'
    date_to = datetime.now().strftime('%d/%m/%Y')
    
    bookmark_url = 'http://appsso.eurostat.ec.europa.eu/nui/show.do?query=BOOKMARK_DS-052400_QID_19C1E60F_UID_-3F171EB0&layout=TIME,C,X,0;GEO,L,Y,0;PRODMILK,L,Z,0;MILKITEM,L,Z,1;INDICATORS,C,Z,2;&zSelection=DS-052400MILKITEM,PRO;DS-052400PRODMILK,MC000;DS-052400INDICATORS,OBS_FLAG;&rankName1=INDICATORS_1_2_-1_2&rankName2=MILKITEM_1_2_-1_2&rankName3=PRODMILK_1_2_-1_2&rankName4=TIME_1_0_0_0&rankName5=GEO_1_2_0_1&sortC=ASC_-1_FIRST&rStp=&cStp=&rDCh=&cDCh=&rDM=true&cDM=true&footnes=false&empty=false&wai=false&time_mode=NONE&time_most_recent=false&lang=EN&cfo=%23%23%23%2C%23%23%23.%23%23%23'

    # initialise option field labels
    init_labels()

    # open parent window by bookmark url
    wdriver = webdriver.Firefox()
    
    # start scraping
    print 'start scraping'
    scraping(wdriver, 0, 0, 0, dir_path, bookmark_url)
    
    wdriver.quit()
    
    print 'finished...'
    


