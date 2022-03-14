'''
Created on 19 August 2016

Modified from dairy_price.py
'''
import sys
import os
from datas.function.function import save_error_to_log
import pandas as pd
import re
import time
from datetime import datetime
from datas.db.manager import DBManager, RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.web.path import WEB_BORDBIA_PATH
from datas.web.scraper import WebScraper
from datas.function.function import create_directory
from datas.function.function import join_list


def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()
        
        # get the latest data date from DB
        dbm = DBManager(db_params[0], db_params[1], db_params[2], db_params[3])
        date_from = dbm.get_latest_date_record('select max(date) from bordbia_dairy_price;')
        date_from = datetime.strftime(date_from[0], '%d/%m/%Y')
        del dbm
        #date_from='01/01/2000'
        scraper = WebScraper('Chrome')
        url= 'http://www.bordbia.ie/industry/farmers/PriceTracking/Archive/cattle/Pages/Prices.aspx'
        scraper.open(url)
        
        countries = scraper.get_dropdown_list('id','ctl00_PlaceHolderMain_ctl01_ctl00_ddlS1Country', 'value')
        time_scale = 'weekly'
        display_type = 'table'
        date_to = datetime.now().strftime('%d/%m/%Y')  # the most recent date
        regex = r'(?:<td>(\d\d/[0-1]\d/[1-2]\d\d\d)</td><td>(\d+.\d+)</td>)'
        pattern = re.compile(str.encode(regex))
        
        dir_title = datetime.now().strftime('%Y_%m_%d')
        dir_path = '%sbeef_price\\' % WEB_BORDBIA_PATH
        dir_path = create_directory(dir_path, dir_title)
        
        """Start scrape"""
        for country in countries: 
            scraper.open(url)
            types = scraper.get_dropdown_list('id', 'ctl00_PlaceHolderMain_ctl01_ctl00_ddlS1Type')
            flag = 0
            timeList = []
            dataList = []
            for type in types:
                scraper.open(url)
                grades = scraper.get_dropdown_list('id', 'ctl00_PlaceHolderMain_ctl01_ctl00_ddlS1Grade')
                timeList = []
                dataList = []
                for grade in grades:
                    titles = []
                    timeList = []
                    dataList = []
                    scraper.open(url)
                    
                    scraper.load_field('select', 'id', 'ctl00_PlaceHolderMain_ctl01_ctl00_ddlTimeScale', time_scale)
                    scraper.load_field('select', 'id', 'ctl00_PlaceHolderMain_ctl01_ctl00_ddlDDA', display_type)
                    scraper.load_field('select', 'id', 'ctl00_PlaceHolderMain_ctl01_ctl00_ddlTimeScale', time_scale)
                    scraper.load_field('input', 'id', 'ctl00_PlaceHolderMain_ctl01_ctl00_txtDateFrom', date_from)
                    scraper.load_field('input', 'id', 'ctl00_PlaceHolderMain_ctl01_ctl00_txtDateTo', date_to)
                    scraper.load_field('select', 'id', 'ctl00_PlaceHolderMain_ctl01_ctl00_ddlS1Country', country)
                    scraper.load_field('select', 'id', 'ctl00_PlaceHolderMain_ctl01_ctl00_ddlS1Type', type)
                    time.sleep(2)
                    scraper.load_field('select', 'id', 'ctl00_PlaceHolderMain_ctl01_ctl00_ddlS1Grade', grade)
                    scraper.click_button('id','ctl00_PlaceHolderMain_ctl01_ctl00_btnDisplay')
                    time.sleep(2)
                            
                    resultsstr = '<table>' + scraper.find_element('id','ctl00_PlaceHolderMain_ctl01_ctl00_plResults').get_attribute("innerHTML") + '<table>'
                    htmltext = unicode.encode(resultsstr)
                    titles = pattern.findall(htmltext)
                    
                    for point in titles:
                        line = [str(point[0].decode('utf-8')), str(point[1].decode('utf-8'))]
                        timeList.append([line[0]])
                        dataList.append([line[1]])
                    
                    currency_web = scraper.find_element('xpath', '//*[@id="ctl00_PlaceHolderMain_ctl01_ctl00_plResults"]/table/tbody/tr[4]/td/table/thead/tr/th[2]')
                    currency_text = currency_web.text
                    currency_headings = currency_text.split('(')
                    currency = currency_headings[1][:-1]
                    
                    lineList = join_list(timeList, dataList)
                    out = pd.DataFrame(lineList)
                    temp_filepath = '%sbeef_price_%s_%s%s%s.csv' % (dir_path, country, currency, grade, type)
                    temp_file = open(temp_filepath, 'w')
                    temp_file.write('url, %s\ndate,' % (url))
                    temp_file.write('\n')
                    out.to_csv(temp_file, header=False, index=False) #prevent automatically numbering the rows and cols
                    '''
                    out_filepath = '%sdairy_price_cent_%s.csv' % (dir_path, country)
                    out_file = open(out_filepath,"w")
                    data = open(temp_filepath).read()
                    out_file.write(re.sub(",0.00",",NA",data))'''
                    temp_file.close()
                    # end of outer if-else
                # end of grade for-loop
            # end of type for-loop
        # end of countries for-loop 
        scraper.close()
        
        print 'Finish scraping at %s.' % datetime.now()
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['bordbia.dairy_price'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('weekly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['bordbia.dairy_price'],[success_msg]]
        save_error_to_log('weekly', msg_list)
    
if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)