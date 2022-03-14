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


PARTNER_LABELS = []
PERIOD_LABELS = []
INDICATOR_LABELS = []
REPORTER_LABELS = []
REPORTER_LIST = []
FLOW_LABELS = [] # not used
PRODUCT_LABELS = [] # not used

LOG_PATH = EUROSTAT_PATH + 'pig_meat_trade.log'
PROGRAM_PATH = './src/scraper/eurostat/pig_meat_trade.py'
LABEL_PATH = EUROSTAT_PATH + 'pig_meat_trade/title_options/'


def init_labels():
    global PARTNER_LABELS
    global PERIOD_LABELS
    global INDICATOR_LABELS
    global REPORTER_LABELS
    global REPORTER_LIST
    global LABEL_PATH
    
    PERIOD_LABELS = read_from_file('%speriods.csv' % LABEL_PATH)
    PERIOD_LABELS = PERIOD_LABELS[2:]
    PERIOD_LABELS.reverse()
    PERIOD_LABELS = chunck_list(PERIOD_LABELS, 12)
    PERIOD_LABELS = PERIOD_LABELS[len(PERIOD_LABELS) - 8:]
    
    PARTNER_LABELS = read_from_file('%spartners.csv' % LABEL_PATH)
    PARTNER_LABELS = PARTNER_LABELS[2:]
    
    REPORTER_LABELS = read_from_file('%sreporters.csv' % LABEL_PATH)
    REPORTER_LIST = [r[1] for r in REPORTER_LABELS[2:]]
    REPORTER_LIST.insert(0, 'period')
    
    INDICATOR_LABELS = read_from_file('%sindicators.csv' % LABEL_PATH)
    INDICATOR_LABELS = INDICATOR_LABELS[2:]


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


def scraping(web_driver, partner_point, period_point, indicator_point,
             dir_path, bookmark_url):
    global PARTNER_LABELS
    global PERIOD_LABELS
    global INDICATOR_LABELS
    global REPORTER_LABELS
    global REPORTER_LIST
    global LOG_PATH
    global PROGRAM_PATH
    
    web_driver.get(bookmark_url)
    time.sleep(5)
    
    web_scraper = WebScraper(web_driver)
    
    partner_point_labels = PARTNER_LABELS[partner_point:]
    period_point_labels = PERIOD_LABELS[period_point:]
    indicator_point_labels = INDICATOR_LABELS[indicator_point:]
    
    # scrape data by every 12 months
    for partner in partner_point_labels:
        # use list of list for partner_list and parter in case of scraping
        # for multiple partners at a time in the future
        partner_list = [partner[1]]
        partner_id = [partner[0]]
        is_partner_selected = False
        
        if partner_point_labels.index(partner) != 0:
            period_point_labels = PERIOD_LABELS[0:]
        
        for period in period_point_labels:
            try:
                period_list = [[p[1]] for p in period]
                period_id = [p[0] for p in period]
                
                # open option window
                web_scraper.click_button('selectDataButton', 'class')
                #time.sleep(1)
                
                # get control of the popup option window
                parent_handle = web_driver.current_window_handle
                handles = web_driver.window_handles
                handles.remove(parent_handle)
                popup_window_handle = handles.pop()
                web_driver.switch_to_window(popup_window_handle)
                
                # TODO(Wenchong): fill in options to the popup window
                # select the given 12 months under Period label
                web_scraper.click_checkbox('//div/a/span[contains(text(),"PERIOD")]',
                                           'checkUncheckAllCheckboxTable',
                                           '//input[@id="%s"]',
                                           period_id)
                
                # select the current partner
                if not is_partner_selected:
                    is_partner_selected = True
                    web_scraper.click_checkbox('//div/a/span[contains(text(),"PARTNER")]',
                                               'checkUncheckAllCheckboxTable',
                                               '//input[@id="%s"]',
                                               partner_id)
                
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
                info.append('Resumed from crash point at partner %s, period %s' % (partner[1], period[0][1]))
                write_to_log(LOG_PATH, info)
                
                partner_point = PARTNER_LABELS.index(partner)
                period_point = PERIOD_LABELS.index(period)
                indicator_point = 0
                
                scraping(web_driver, partner_point, period_point, indicator_point,
                         dir_path, bookmark_url)
            
            if period_point_labels.index(period) != 0:
                indicator_point_labels = INDICATOR_LABELS[0:]
            
            # get production in weigh and value
            for indicator in indicator_point_labels:
                try:
                    data_list  = []
                    
                    #web_scraper.load_field('projDimsValuesAvailableValue(DS-016894INDICATORS)', indicator[2], 'list')
                    web_scraper.load_field("model.projDimsValuesAvailable['DS-016894INDICATORS']", indicator[2], 'list')
                    time.sleep(5)
                    
                    # get production data sets
                    rows = web_driver.find_elements_by_xpath('//td[starts-with(@class, "table_cell column")]')
                    for row in rows:
                        data_str = str(row.find_element_by_tag_name('div').text).replace(',', '')
                        data_list.append(data_str)
                        
                    # chunck data sets by table row
                    num_col = len(period_list)
                    data_list = chunck_list(data_list, num_col)
                    
                    # join periods and data sets into rows
                    row_list = []
                    index = 0
                    for p in period_list:
                        row_list.append(p)
                        for d in data_list:
                            row_list[index].append(d[index])
                        index += 1
                except Exception as e:
                    info = [datetime.now().strftime('UTC: %Y-%m-%d %H:%M:%S')]
                    info.append(PROGRAM_PATH)
                    info.append('Error %s' % e)
                    info.append('Resumed from crash point at partner %s, period %s, indicator %s' % (partner[1], period[0][1], indicator[1]))
                    write_to_log(LOG_PATH, info)
                    
                    partner_point = PARTNER_LABELS.index(partner)
                    period_point = PERIOD_LABELS.index(period)
                    indicator_point = INDICATOR_LABELS.index(indicator)
                    
                    web_driver.close()
                    
                    scraping(web_driver, partner_point, period_point, indicator_point,
                             dir_path, bookmark_url)
                else:
                    # write all data to file
                    file_path = '%s%s_%s.csv' % (dir_path, partner_list[0], indicator[1])
                    web_scraper.save_to_file(file_path, bookmark_url, REPORTER_LIST, row_list)
            # end of inner for: indicators
        # end of middle for loop: periods
    # end of outer for loop: partners


if __name__ == '__main__':
    
    dir_title = datetime.now().strftime('%Y_%m_%d')
    dir_path = EUROSTAT_PATH + 'pig_meat_trade/'
    dir_path = create_directory(dir_path, dir_title)
    
    date_from = '01/01/2007'
    date_to = datetime.now().strftime('%d/%m/%Y')
    
    # this bookmark_url selects all flow, indicators, partner, product and reporter, period 198801 selected
    bookmark_url = 'http://appsso.eurostat.ec.europa.eu/nui/show.do?query=BOOKMARK_DS-016894_QID_441F7225_UID_-3F171EB0&layout=PERIOD,L,X,0;REPORTER,L,Y,0;PARTNER,L,Z,0;PRODUCT,L,Z,1;FLOW,L,Z,2;INDICATORS,C,Z,3;&zSelection=DS-016894FLOW,2;DS-016894INDICATORS,QUANTITY_IN_100KG;DS-016894PARTNER,AD;DS-016894PRODUCT,0203;&rankName1=PARTNER_1_2_-1_2&rankName2=INDICATORS_1_2_-1_2&rankName3=FLOW_1_2_-1_2&rankName4=PRODUCT_1_2_-1_2&rankName5=PERIOD_1_0_0_0&rankName6=REPORTER_1_2_0_1&sortC=ASC_-1_FIRST&rStp=&cStp=&rDCh=&cDCh=&rDM=true&cDM=true&footnes=false&empty=false&wai=false&time_mode=NONE&time_most_recent=false&lang=EN&cfo=%23%23%23%2C%23%23%23.%23%23%23'

    # initialise option field labels
    init_labels()

    # open parent window by bookmark url
    wdriver = webdriver.Firefox()
    
    # start scraping
    print 'start scraping'
    scraping(wdriver, 0, 0, 0, dir_path, bookmark_url)
    
    wdriver.quit()
    
    print 'finished...'
    


