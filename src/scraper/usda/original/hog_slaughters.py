'''
Created on 6 Jan 2015

@author: Suzanne

06/01/2015(Suzanne): This program only works correctly if your downloads folder
has no .csv files in it at beginning of runtime
29/01/2015(Wenchong): Fixed a few bugs.
30/01/2015(Wenchong): There are problems communicating with websites trying to get as
detailed as to week level. Download whole year data and get latest data by processing files.
03/02/2015(Wenchong): Automation completed.
12/02/2015(Wenchong): Fixed sql query to get the correct date as a new scraping point.
'''


import sys
import time
from datetime import datetime
from selenium.webdriver.support.select import Select
from datas.db.manager import DBManager
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import create_directory
from datas.function.function import save_download_file
from datas.web.path import DOWNLOAD_PATH
from datas.web.path import WEB_USDA_PATH
from datas.web.scraper import WebScraper


def scrape():
    print 'Start scraping at %s...' % datetime.now()
    
    # get the latest data date from DB
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    dbm = DBManager(db_params[0], db_params[1], db_params[2], db_params[3])
    sql = ('select max(year) as max_date from usda_hog_slaughters '
           'group by region, data_item order by max_date asc limit 1;')
    date_from = dbm.get_latest_date_record(sql)
    year_from = int(date_from[0][:4])
    #week_from = int(date_from[0][4:])
    del dbm
    #print year_from, week_from
    
    url = 'http://quickstats.nass.usda.gov/'
    measures = ['HEAD', 'LB / HEAD, DRESSED BASIS']
    this_year = datetime.now().year
    
    dir_title = datetime.now().strftime('%Y_%m_%d')
    dir_path = '%shog_slaughters\\' % WEB_USDA_PATH
    dest_path = create_directory(dir_path, dir_title)
    
    # if year_from = this_year, assign True, else assign False
    is_yearfrom_thisyear = not (this_year - year_from)
    
    # since there are more problems selecting weeks, we simply download
    # all data in this year, then the latest data will be picked up
    # in the db loader
    for measure in measures:
        for i in range(year_from, this_year + 1):
            wscraper = WebScraper('Chrome')
            wscraper.open(url)
            wscraper.web_driver.maximize_window()
            
            # select commodity
            wscraper.wait(30, 'xpath', '//*[text()="HOGS"]')
            time.sleep(2)
            wscraper.click_button('xpath', '//*[text()="HOGS"]')
            
            # select category
            wscraper.wait(30, 'xpath', '//*[text()="SLAUGHTERED"]')
            time.sleep(2)
            wscraper.click_button('xpath', '//*[text()="SLAUGHTERED"]')
            
            # select data item
            wscraper.wait(30, 'xpath', '//*[text()="HOGS, SLAUGHTER, COMMERCIAL, FI - SLAUGHTERED, MEASURED IN %s"]' % measure)
            time.sleep(2)
            wscraper.click_button('xpath', '//*[text()="HOGS, SLAUGHTER, COMMERCIAL, FI - SLAUGHTERED, MEASURED IN %s"]' % measure)
            
            # select year
            wscraper.wait(30, 'xpath', '//*[text()="2014"]')
            time.sleep(2)
            wscraper.click_button('xpath', '//*[text()="%s"]' % str(i))
            
            # select period type
            wscraper.wait(30, 'xpath', '//*[text()="WEEKLY"]')
            time.sleep(2)
            wscraper.click_button('xpath', '//*[text()="WEEKLY"]')
            
            '''
            # select weeks after week_from, otherwise leave it blank and all weeks will be selected
            if i == this_year:
                if is_yearfrom_thisyear:
                    #get_new_week_data(wscraper, week_from)
                    wscraper.wait(30, 'id', 'reference_period_desc')
                    time.sleep(10)
                    #weeks = wscraper.find_elements('xpath', '//select[@id="reference_period_desc"]/option')
                    wscraper.wait(30, 'xpath', '//select[@id="reference_period_desc"]/option[@value="WEEK #01"]')
                    time.sleep(10)
                    select = Select(wscraper.find_element('id', 'reference_period_desc'))
                    for week in range(week_from, 53):
                        print 'select option %02d' % week
                        time.sleep(2)
                        select.select_by_value('WEEK #%02d' % week)
            elif i == this_year - 1:
                if not is_yearfrom_thisyear:
                    #get_new_week_data(wscraper, week_from)
                    wscraper.wait(30, 'id', 'reference_period_desc')
                    time.sleep(10)
                    #weeks = wscraper.find_elements('xpath', '//select[@id="reference_period_desc"]/option')
                    wscraper.wait(30, 'xpath', '//select[@id="reference_period_desc"]/option[@value="WEEK #01"]')
                    time.sleep(10)
                    select = Select(wscraper.find_element('id', 'reference_period_desc'))
                    for week in range(week_from, 53):
                        print 'select option %02d' % week
                        time.sleep(2)
                        select.select_by_value('WEEK #%02d' % week)
            '''
            
            # browser seems to 'forget' this from earlier!
            wscraper.click_button('xpath', '//*[text()="HOGS, SLAUGHTER, COMMERCIAL, FI - SLAUGHTERED, MEASURED IN %s"]' % measure)
                        
            # click submit button
            time.sleep(2)
            wscraper.click_button('id', 'submit001_label')
            
            # download file
            wscraper.wait(30, 'xpath', '//*[text()="Spreadsheet"]')
            time.sleep(2)
            wscraper.click_button('xpath', '//*[text()="Spreadsheet"]')
            time.sleep(5)
            
            wscraper.close()
            
            print 'scraped %s %s' % (measure, str(i))
            
            save_download_file(DOWNLOAD_PATH, '%s%s%s.csv' % (dest_path, measure.replace('/','per'), str(i)))
        # end of inner for-loop
    # end of outter for-loop
    
    print 'Finish scraping at %s...' % datetime.now()
    
if __name__ == '__main__':
    scrape()