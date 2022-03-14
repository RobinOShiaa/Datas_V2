'''
Created on 3 Nov 2014

@author: Suzanne

07/01/2015(Wenchong): Automation completed.
12/02/2015(Wenchong): Fixed sql query to get the correct date as a new scraping point.
20/03/2015 (Sue): changed to include database params after merging databases
'''
import pandas as pd
import re
import sys
from datas.function.function import save_error_to_log
import os
import time
from datetime import datetime
from datas.db.manager import DBManager
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import create_directory
from datas.function.function import join_list
from datas.web.path import WEB_BORDBIA_PATH
from datas.web.scraper import WebScraper


def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()
        
        # get the latest data date from DB
        dbm = DBManager(db_params[0], db_params[1], db_params[2], db_params[3])
        sql = ('select max(date) as max_date from bordbia_cereal_price '
               'group by area, type order by max_date asc limit 1;')
        date_from = dbm.get_latest_date_record(sql)
        date_from = datetime.strftime(date_from[0], '%d/%m/%Y')
        del dbm
    
        scraper = WebScraper('Chrome')
        url= 'http://www.bordbia.ie/industry/farmers/pricetracking/cereals/pages/cerealpricesgraphs.aspx'
        scraper.open(url)
        
        countries = scraper.get_dropdown_list('id','ctl00_PlaceHolderMain_ctl01_ctl00_ddlS1Country')
        time_scale = 'weekly'
        display_type = 'table'
        date_to = datetime.now().strftime('%d/%m/%Y')  # the most recent date
        regex = '<td>(\d\d/[0-1]\d/[1-2]\d\d\d)</td><td>(\d+.\d+)</td>'
        pattern = re.compile(str.encode(regex))
        
        dir_title = datetime.now().strftime('%Y_%m_%d')
        dir_path = '%scereal_price\\' % WEB_BORDBIA_PATH
        dir_path = create_directory(dir_path, dir_title)
    
        
    
        """Start scrape"""
        for country in countries[1:]: #First element in list is empty string
            scraper.open(url)
            scraper.load_field('select', 'id', 'ctl00_PlaceHolderMain_ctl01_ctl00_ddlS1Country', country)
            time.sleep(2)
            types = scraper.get_dropdown_list('id','ctl00_PlaceHolderMain_ctl01_ctl00_ddlS1Type')
            flag = 0
            time_list = []
            data_list = []
            for type in types:
                scraper.open(url)
                scraper.load_field('select', 'id', 'ctl00_PlaceHolderMain_ctl01_ctl00_ddlTimeScale', time_scale)
                scraper.load_field('select', 'id', 'ctl00_PlaceHolderMain_ctl01_ctl00_ddlDDA', display_type)
                scraper.load_field('select', 'id', 'ctl00_PlaceHolderMain_ctl01_ctl00_ddlTimeScale', time_scale)
                scraper.load_field('input', 'id', 'ctl00_PlaceHolderMain_ctl01_ctl00_txtDateFrom', date_from)
                scraper.load_field('input', 'id', 'ctl00_PlaceHolderMain_ctl01_ctl00_txtDateTo', date_to)
                scraper.load_field('select', 'id', 'ctl00_PlaceHolderMain_ctl01_ctl00_ddlS1Country', country)
                time.sleep(2)
                scraper.load_field('select', 'id', 'ctl00_PlaceHolderMain_ctl01_ctl00_ddlS1Type', type)
                scraper.click_button('id', 'ctl00_PlaceHolderMain_ctl01_ctl00_btnDisplay')
                time.sleep(2)
                
                resultsstr = '<table>' + scraper.web_driver.find_element_by_id('ctl00_PlaceHolderMain_ctl01_ctl00_plResults').get_attribute("innerHTML") + '<table>'
                htmltext = unicode.encode(resultsstr)
                titles = pattern.findall(htmltext)
        
                     
                if flag == 0:
                    flag = 1
                         
                    for point in titles:
                        line = [str(point[0].decode('utf-8')), str(point[1].decode('utf-8'))]
                            
                        time_list.append([line[0]])
                        data_list.append([line[1]])
                else:
                    count = 0
                    for point in titles:
                        line = [str(point[0].decode('utf-8')), str(point[1].decode('utf-8'))]
                                                  
                        date1 = datetime.strptime(time_list[count][0], '%d/%m/%Y')
                        date2 = datetime.strptime(line[0], '%d/%m/%Y')
                                 
                        while date1 < date2:
                            data_list[count].append('NA')
                            count += 1
                            date1 = datetime.strptime(time_list[count][0], '%d/%m/%Y')
                                 
                        if date1 > date2: # be careful, may need more insertions for other columns
                            time_list[count].insert(count, [line[0]])
                            data_list.insert(count, ['NA'])
                                 
                        data_list[count].append(line[1])
                        count += 1
                    #end of inner for-loop
                #print data_list
                # check if there's new data
                if not data_list:
                    scraper.close()
                    print 'No new data found, terminated at %s...' % datetime.now()
                    return
    
                line_list = join_list(time_list, data_list)
                out = pd.DataFrame(line_list)
                
                temp_filepath = '%scereal_price_cent_%s.csv' % (dir_path, country)
                temp_file = open(temp_filepath, 'w')
                temp_file.write('url,%s\ndate,' % (url))
                temp_file.write(','.join(types))
                temp_file.write('\n')
                out.to_csv(temp_file, header=False, index=False) # prevent automatically numbering rows and columns
                '''
                out_filepath = BORDBIA_PATH+'grain/bordbia_cereal_price(cent)_%s.csv' % (country)
                out_file = open(out_filepath,"w")
                data = open(temp_filepath).read()
                out_file.write(re.sub(",0.00",",NA",data))
                out_file.close()'''
                # end of outer if-else
            # end of type for-loop
        # end of countries for-loop
        scraper.close()
        
        print 'Finish scraping at %s.' % datetime.now()
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['bordbia.cereal_price.py'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('weekly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['bordbia.cereal_price.py'],[success_msg]]
        save_error_to_log('weekly', msg_list)

if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)

