'''
Created on 6 Oct 2014

@author: Wenchong

25/11/2014(Wenchong): Fixed the problems found during QA on 24/11/2014.
07/01/2015(Wenchong): Automation completed.
12/02/2015(Wenchong): Fixed sql query to get the correct date as a new scraping point.
'''
import sys
from datas.function.function import save_error_to_log
import time
from datetime import datetime
from datas.db.manager import DBManager
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import chunck_list
from datas.function.function import create_directory
from datas.web.path import WEB_BORDBIA_PATH
from datas.web.scraper import WebScraper


def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()
        # get the latest data date from DB
        dbm = DBManager(db_params[0], db_params[1], db_params[2], db_params[3])
        sql = ('select max(date) as max_date from bordbia_pig_price '
               'group by area, type order by max_date asc limit 1;')
        date_from = dbm.get_latest_date_record(sql)
        date_from = datetime.strftime(date_from[0], '%d/%m/%Y')
        del dbm
        #print date_from
        
        url = 'http://www.bordbia.ie/industry/farmers/pricetracking/pig/pages/prices.aspx'
        time_scale = 'weekly'
        display_type = 'table'
        date_to = datetime.now().strftime('%d/%m/%Y')  # the most recent date
        num_col = 6  # number of columns of countries that can be scraped at a time
        is_time_stored = False  # is the first column of time scraped
        
        data_list = []
        
        wscraper = WebScraper('Chrome')
        wscraper.open(url)
        
        # get all countries
        headers = wscraper.get_dropdown_list('id', 'ctl00_PlaceHolderMain_ctl01_ctl00_ddlS1Country', 'value')
        countries = chunck_list(headers, num_col)
        
        # scrape 6 countries at a time
        for country in countries:
            wscraper.open(url)
            
            num_country = len(country)
            
            # select the 6 countries
            for i in range(num_country):
                wscraper.load_field('select', 'name', 'ctl00$PlaceHolderMain$ctl01$ctl00$ddlS%sCountry' % (i + 1), country[i])
            
            wscraper.load_field('select', 'name', 'ctl00$PlaceHolderMain$ctl01$ctl00$ddlTimeScale', time_scale)
            wscraper.load_field('select', 'name', 'ctl00$PlaceHolderMain$ctl01$ctl00$ddlDDA', display_type)
            wscraper.load_field('input', 'name', 'ctl00$PlaceHolderMain$ctl01$ctl00$txtDateFrom',date_from)
            wscraper.load_field('input', 'name', 'ctl00$PlaceHolderMain$ctl01$ctl00$txtDateTo', date_to)
            
            # display
            wscraper.click_button('name', 'ctl00$PlaceHolderMain$ctl01$ctl00$btnDisplay')
            
            time.sleep(3)
            
            # start retrieving data
            row_list = []
            data_objs = wscraper.web_driver.find_elements_by_xpath('//table[@class="GenericListTable"]/tbody/tr/td')
            for obj in data_objs:
                data_str = str(obj.text)
                row_list.append(data_str if data_str else 'NA')
            
            row_list = chunck_list(row_list, num_country + 1)
            
            # combine datasets from different iterations into one dataset
            if is_time_stored:
                for i in range(len(row_list)):
                    data_list[i] += row_list[i][1:]
            else:
                for i in range(len(row_list)):
                    data_list.append(row_list[i])
            
            is_time_stored = True
        # end of outer for-loop
        
        wscraper.close()
        
        # check if there's new data
        if not data_list:
            print 'No new data found, terminated at %s...' % datetime.now()
            return
        
        # store the dataset into the file
        dir_title = datetime.now().strftime('%Y_%m_%d')
        dir_path = '%spig_price\\' % WEB_BORDBIA_PATH
        dir_path = create_directory(dir_path, dir_title)
        file_path = '%spig_price.csv' % dir_path
        
        headers = ['%s' % h for h in headers]
        headers.insert(0, 'time')
        wscraper.save_to_file(file_path, url, headers, data_list)
        
        print 'Finish scraping at %s.' % datetime.now()
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['bordbia.pig_price'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('weekly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['bordbia.pig_price'],[success_msg]]
        save_error_to_log('weekly', msg_list)

if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
    
