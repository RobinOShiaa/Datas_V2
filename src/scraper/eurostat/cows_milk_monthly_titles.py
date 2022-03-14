'''
Created on 14 Nov 2014

@author: Wenchong

26/11/2014: Fixed excluding some areas problem found during
the QA on 25/11/2014. The symbol ',' in the title labels are
replaced with symbol '/'.
'''


import time
from datas.function.function import create_directory
from datas.function.function import delete_file
from datas.function.function import save_to_file
from datas.function.function import union_list
from datas.web.path import WEB_EUROSTAT_PATH
from datas.web.scraper import WebScraper


def get_titles(option='all'):
    dir_path = create_directory(WEB_EUROSTAT_PATH, 'cows_milk_monthly\\title_options')
    bookmark_url = 'http://appsso.eurostat.ec.europa.eu/nui/show.do?query=BOOKMARK_DS-055514_QID_-57BB536C_UID_-3F171EB0&layout=TIME,C,X,0;GEO,L,Y,0;PRODMILK,L,Z,0;UNIT,L,Z,1;INDICATORS,C,Z,2;&zSelection=DS-055514PRODMILK,MM001;DS-055514UNIT,THS_T;DS-055514INDICATORS,OBS_FLAG;&rankName1=UNIT_1_2_-1_2&rankName2=INDICATORS_1_2_-1_2&rankName3=PRODMILK_1_2_-1_2&rankName4=TIME_1_0_0_0&rankName5=GEO_1_2_0_1&sortC=ASC_-1_FIRST&rStp=&cStp=&rDCh=&cDCh=&rDM=true&cDM=true&footnes=false&empty=false&wai=false&time_mode=NONE&time_most_recent=false&lang=EN&cfo=%23%23%23%2C%23%23%23.%23%23%23'
    
    months = ['M{0:02d}'.format(i) for i in range(1, 13)]
    
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
        
    if option in ['all', 'unit']:
        # get checkbox ids, codes and labels for unit
        wscraper.click_button('xpath', '//div/a/span[contains(text(),"UNIT")]')
        time.sleep(1)
        wscraper.get_title_attributes(bookmark_url, dir_path, 'unit')
        
    if option in ['all', 'prodmilk']:
        # get checkbox ids, codes and labels for prodmilk
        wscraper.click_button('xpath', '//div/a/span[contains(text(),"PRODMILK")]')
        time.sleep(1)
        wscraper.get_title_attributes(bookmark_url, dir_path, 'prodmilk')
        
    if option in ['all', 'time']:
        # get checkbox ids, codes and labels for time
        wscraper.click_button('xpath', '//div/a/span[contains(text(),"TIME")]')
        time.sleep(1)
        #wscraper.get_title_attributes(bookmark_url, dir_path, 'time')
        id_objs = wscraper.web_driver.find_elements_by_xpath('//li[starts-with(@id, "TIME")]')
        id_list = []
        for id in id_objs:
            id_str = str(id.get_attribute('id'))
            year = id_str[4:]
            year_month = union_list([year], months, '', pos='prefix')
            tmp = [id_str, year]
            for y in year_month[0]:
                tmp.append(y)
            id_list.append(tmp)
        
        id_list.insert(0, ['url', bookmark_url])
        id_list.insert(1, ['checkbox_id', 'code', 'label'])
        
        file_path = '%s%s.csv' % (dir_path, 'time')
        delete_file(file_path)
        save_to_file(file_path, id_list)
    
    wscraper.close()

