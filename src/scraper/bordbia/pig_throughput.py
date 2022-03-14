'''
Created on 9 Jan 2015

@author: Suzanne

09/01/2015(Suzanne): File output not working properly.
27/01/2015(Wenchong): Fixed data output bugs.
27/01/2015(Wenchong): Automation completed.
12/02/2015(Wenchong): Fixed sql query to get the correct date as a new scraping point.
'''
import sys
import os
from datas.function.function import save_error_to_log
import time
from datetime import datetime
from datetime import timedelta
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
        sql = ('select max(week_end_date) as max_date from bordbia_pig_throughput '
               'group by member_state, type order by max_date asc limit 1;')
        date_from = dbm.get_latest_date_record(sql)
        date_from = date_from[0] + timedelta(days=1)
        date_from = datetime.strftime(date_from, '%d/%m/%Y')
        del dbm
        date_from = '01/01/2010'
        url= 'http://www.bordbia.ie/industry/farmers/pricetracking/pig/pages/throughput.aspx'
        types = ['Fattening Pigs', 'Total Pigs', 'Sows & Boars']
        titles = ['weekly_slaughterings_Fattening Pigs_1 head',
                  'weekly_slaughterings_Total Pigs_1 head',
                  'weekly_slaughterings_Sows Boars_1 head']
        time_scale = 'weekly'
        display_type = 'table'
        date_to = datetime.now().strftime('%d/%m/%Y')  # for web scrape
        dir_path = '%sthroughput\\' % WEB_BORDBIA_PATH
        
        """Start scrape"""
        for type in types:
            scraper = WebScraper('Chrome')
            scraper.open(url)
            scraper.load_field('select', 'id', 'ctl00_PlaceHolderMain_ctl01_ctl00_ddlS1Country', 'Germany')
            scraper.load_field('select', 'id', 'ctl00_PlaceHolderMain_ctl01_ctl00_ddlS2Country', 'Ireland')
            scraper.load_field('select', 'id', 'ctl00_PlaceHolderMain_ctl01_ctl00_ddlS3Country', 'Denmark')
            scraper.load_field('select', 'id', 'ctl00_PlaceHolderMain_ctl01_ctl00_ddlS4Country', 'Great Britain')
            scraper.load_field('select', 'id', 'ctl00_PlaceHolderMain_ctl01_ctl00_ddlS5Country', 'Northern Ireland')
            scraper.load_field('select', 'id', 'ctl00_PlaceHolderMain_ctl01_ctl00_ddlS6Country', 'Netherlands')
                     
            scraper.load_field('select', 'id', 'ctl00_PlaceHolderMain_ctl01_ctl00_ddlS1Type', type)
            scraper.load_field('select', 'id', 'ctl00_PlaceHolderMain_ctl01_ctl00_ddlS2Type', type)
            scraper.load_field('select', 'id', 'ctl00_PlaceHolderMain_ctl01_ctl00_ddlS3Type', type)
            scraper.load_field('select', 'id', 'ctl00_PlaceHolderMain_ctl01_ctl00_ddlS4Type', type)
            scraper.load_field('select', 'id', 'ctl00_PlaceHolderMain_ctl01_ctl00_ddlS5Type', type)
            scraper.load_field('select', 'id', 'ctl00_PlaceHolderMain_ctl01_ctl00_ddlS6Type', type)
         
            scraper.load_field('select', 'id', 'ctl00_PlaceHolderMain_ctl01_ctl00_ddlTimeScale', time_scale)
            scraper.load_field('select', 'id', 'ctl00_PlaceHolderMain_ctl01_ctl00_ddlDDA', display_type)
            scraper.load_field('input', 'id', 'ctl00_PlaceHolderMain_ctl01_ctl00_txtDateFrom', date_from)
            scraper.load_field('input', 'id', 'ctl00_PlaceHolderMain_ctl01_ctl00_txtDateTo', date_to)
            
            scraper.click_button('id', 'ctl00_PlaceHolderMain_ctl01_ctl00_btnDisplay')
            time.sleep(2)
            
            tags = scraper.find_elements('xpath', '//table[@class="GenericListTable"]/thead/tr/th')
            
            headers = []
            for tag in tags:
                headers.append(tag.text)
            
            row_list = []
            data_objs = scraper.web_driver.find_elements_by_xpath('//table[@class="GenericListTable"]/tbody/tr/td')
            for obj in data_objs:
                data_str = str(obj.text.replace(',',''))
                row_list.append(data_str if data_str else 'NA')
            
            row_list = chunck_list(row_list, len(headers))
            
            # check if there's new data
            if not row_list:
                scraper.close()
                print 'No new data found, terminated at %s...' % datetime.now()
                continue
            
            # store the dataset into the file
            dir_title = datetime.now().strftime('%Y_%m_%d')
            dir_path = '%sthroughput\\' % WEB_BORDBIA_PATH
            dir_path = create_directory(dir_path, dir_title)
            file_path = '%s%s.csv' % (dir_path, titles[types.index(type)])
            scraper.save_to_file(file_path, url, headers, row_list)
            
            scraper.close()
            
        print 'Finish scraping at %s...' % datetime.now()
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['bordbia.pig_throughput'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n\n']]
        save_error_to_log('weekly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['bordbia.pig_throughput'],[success_msg]]
        save_error_to_log('weekly', msg_list)

if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)

