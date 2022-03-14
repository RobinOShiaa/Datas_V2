'''
Created on 11 Nov 2014

@author: Suzanne

27/01/2015(Wenchong): Website rebuilt, adapted the changes.
27/01/2015(Wenchong): Automation completed.
12/02/2015(Wenchong): Fixed sql query to get the correct date as a new scraping point.
'''
import sys
from datas.function.function import save_error_to_log
import re
from datetime import datetime
from datas.db.manager import DBManager
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import chunck_list
from datas.function.function import create_directory
from datas.web.path import WEB_BPEX_PATH
from datas.web.scraper import WebScraper

def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()
        
        # get the latest data date from DB
        dbm = DBManager(db_params[0], db_params[1], db_params[2], db_params[3])
        sql = 'select max(date) from bpex_weaner_price;'
        date_from = dbm.get_latest_date_record(sql)
        date_from = date_from[0]
        del dbm
        
        url = 'http://www.bpex.org.uk/prices-facts-figures/pricing/Weaner.aspx'
        
        timescale = ["0.5", "1", "3", "5"]
        hregex = '<th class="date ordinance_0">(.*?)</th>|<th class="numeric ordinance_1">(.*?)</th>'
        regex = '<td class="date ordinance_0">(\d+\s\w+\s\d+)</td>|<td class="numeric ordinance_1">(\d+\.\d+)</td>'
        pattern = re.compile(str.encode(regex))
        hpattern = re.compile(str.encode(hregex))
        
        '''Start scraping'''
        scraper = WebScraper('Chrome')
        scraper.open(url)
        
        # Specify how far back to scrape
        scraper.load_field('select', 'id', 'duration', timescale[3])
        
        resultsstr = scraper.web_driver.find_element_by_xpath('//table[@class="report chart"]').get_attribute('innerHTML')
        htmltext = unicode.encode(resultsstr)
        
        heads = hpattern.findall(htmltext)
        headers = [x for t in heads for x in t]
        headers = filter(None, headers)
        
        titles = pattern.findall(htmltext)    #NB - results in tuple
        data = [x for t in titles for x in t] #convert to list
        data = filter(None, data)
        data = chunck_list(data, 2)
        
        scraper.close()
        '''Done scraping'''
        
        # check if there's new data
        if not data:
            print 'No new data found, terminated at %s...' % datetime.now()
            return
        
        dir_title = datetime.now().strftime('%Y_%m_%d')
        dir_path = '%sweaner_price\\' % WEB_BPEX_PATH
        dir_path = create_directory(dir_path, dir_title)
        file_path = '%sweaner_pricing_euro per head.csv' % dir_path
        
        # get all records later than the latest record in db
        data_list = []
        for d in data:
            date_to = datetime.strptime(d[0], '%d %b %Y').date()
            
            if date_from < date_to:
                data_list.append(d)
            else:
                break
        
        with open(file_path, 'w') as out_file:
            out_file.write('url,%s' % (url))
            out_file.write('\n')
            
            out_file.write(','.join(headers))
            out_file.write('\n')
                 
            for d in data_list:
                out_file.write(','.join(d))
                out_file.write('\n')
                     
        
        
        
        '''Alternative to download file'''
         
        # timescale = ["0.5", "1", "3", "5"]       
        # source_file = '/users/suzanne/downloads/Export.xls'
        # dest_file = 'BPEX_PATH/weaner_pricing'+today+'.xls'
        # browser = webdriver.Chrome() 
        # browser.get(url)
        # scraper_original.load_field('select', 'id', 'ddlDuration',timescale[3])
        # # time.sleep(2)       
        # element = browser.find_element_by_link_text('Download as Excel)
        # element.click() 
        # time.sleep(2) 
        # browser.quit()
        # os.rename(source_file, dest_file)
        print 'Finish scraping at %s.' % datetime.now()
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['bpex.weaner_price.py'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('weekly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['bpex.weaner_price.py'],[success_msg]]
        save_error_to_log('weekly', msg_list)

if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
    