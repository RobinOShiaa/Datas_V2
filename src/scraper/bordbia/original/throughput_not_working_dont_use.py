'''
Created on 9 Jan 2015

@author: Suzanne

'''

import pandas as pd
import re
import time
from datetime import datetime
from datas.db.manager import DBManager
from datas.web.path import WEB_BORDBIA_PATH
from datas.web.scraper import WebScraper
from datas.function.function import create_directory
from datas.function.function import join_list


def scrape():
    print 'Start scraping at %s...' % datetime.now()
    
    # create db connection
    #dbm = DBManager(db_name='raw_db_copy', host_name='127.0.0.1', user_name='root', pass_word='123abc')
    
    # get the latest data date from DB
#     date_from = dbm.get_latest_date_record('select max(date) from raw_db_copy.bordbia_price where type != "Pig";')
#     date_from = datetime.strftime(date_from[0], '%d/%m/%Y')
    date_from = '01/01/2007'
    #del dbm
    
    scraper = WebScraper('Firefox')
    url= 'http://www.bordbia.ie/industry/farmers/pricetracking/pig/pages/throughput.aspx'
    scraper.open(url)
    
    countries = scraper.get_dropdown_list('id','ctl00_PlaceHolderMain_ctl01_ctl00_ddlS1Country')
    time_scale = 'weekly'
    display_type = 'table'
    date_to = datetime.now().strftime('%d/%m/%Y')  # the most recent date
    regex = '<td>(\d\d\d\d-\d\d-\d\d)</td><td>((\d+,)?\d+)</td>' #'<td>(\d\d\-[0-1]\d\-[1-2]\d\d\d)</td><td>(\d+,\d+)</td>'
    pattern = re.compile(str.encode(regex))
    
    dir_title = datetime.now().strftime('%Y_%m_%d')
    dir_path = '%sthroughput\\' % WEB_BORDBIA_PATH
    dir_path = create_directory(dir_path, dir_title)
    
    """Start scrape"""
    for country in countries:
        scraper.open(url)
        scraper.load_field('select', 'id', 'ctl00_PlaceHolderMain_ctl01_ctl00_ddlS1Country', country)
        types = scraper.get_dropdown_list('id','ctl00_PlaceHolderMain_ctl01_ctl00_ddlS1Type')
        flag = 0
        timeList = []
        dataList = []
        for type in types:
            print 'scraping '+country+type
            scraper.open(url)
            scraper.load_field('select', 'id', 'ctl00_PlaceHolderMain_ctl01_ctl00_ddlTimeScale', time_scale)
            scraper.load_field('select', 'id', 'ctl00_PlaceHolderMain_ctl01_ctl00_ddlDDA', display_type)
            scraper.load_field('select', 'id', 'ctl00_PlaceHolderMain_ctl01_ctl00_ddlTimeScale', time_scale)
            scraper.load_field('input', 'id', 'ctl00_PlaceHolderMain_ctl01_ctl00_txtDateFrom', date_from)
            scraper.load_field('input', 'id', 'ctl00_PlaceHolderMain_ctl01_ctl00_txtDateTo', date_to)
            scraper.load_field('select', 'id', 'ctl00_PlaceHolderMain_ctl01_ctl00_ddlS1Country', country)
            scraper.load_field('select', 'id', 'ctl00_PlaceHolderMain_ctl01_ctl00_ddlS1Type', type)
            scraper.click_button('id', 'ctl00_PlaceHolderMain_ctl01_ctl00_btnDisplay')
            time.sleep(2)
            
            resultsstr = '<table>' + scraper.web_driver.find_element_by_id('ctl00_PlaceHolderMain_ctl01_ctl00_plResults').get_attribute("innerHTML") + '<table>'
            htmltext = unicode.encode(resultsstr)
            titles = pattern.findall(htmltext)
            print titles     
            if flag == 0:
                flag = 1
                     
                for point in titles:
                    line = [str(point[0].decode('utf-8')), str(point[1].decode('utf-8'))]
                        
                    timeList.append([line[0]])
                    dataList.append([line[1]])
            else:
                count = 0
                for point in titles:
                    line = [str(point[0].decode('utf-8')), str(point[1].decode('utf-8'))]
                                              
                    date1 = datetime.strptime(timeList[count][0], '%Y-%m-%d')
                    date2 = datetime.strptime(line[0], '%Y-%m-%d')
                             
                    while date1 < date2:
                        dataList[count].append('NA')
                        count += 1
                        date1 = datetime.strptime(timeList[count][0], '%d/%m/%Y')
                             
                    if date1 > date2: # be careful, may need more insertions for other columns
                        timeList[count].insert(count, [line[0]])
                        dataList.insert(count, ['NA'])
                             
                    dataList[count].append(line[1])
                    count += 1
                #end of inner for-loop   
            #print dataList
            lineList = join_list(timeList, dataList)
            out = pd.DataFrame(lineList)
            temp_filepath = '%sthroughput_%s.csv' % (dir_path, country)
            temp_file = open(temp_filepath, 'w')
            temp_file.write('url,%s' % (url))
            temp_file.write('\n')
            temp_file.write('date,')
            temp_file.write(','.join(types))
            temp_file.write('\n')
            out.to_csv(temp_file, header=False, index=False) #to stop it automatically numbering the rows and cols
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
    
    print 'Finish scraping at %s...' % datetime.now()

if __name__ == '__main__':
    scrape()
