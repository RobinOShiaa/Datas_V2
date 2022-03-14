'''
Created on 31 Aug 2015

@author: Suzanne
'''
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import chunck_list, create_directory, save_error_to_log
from datas.web.path import WEB_CLAL_PATH
from datas.web.scraper import WebScraper
from datetime import datetime
import time
import sys

def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()
        
        # get the latest data date from DB
        #dbm = DBManager(db_params[0], db_params[1], db_params[2], db_params[3])
        dir_path = '%scheese_production' % WEB_CLAL_PATH
        today = datetime.strftime(datetime.now(), '%Y_%m_%d')
        
        url = 'http://www.clal.it/en/index.php?section=produzioni_cheese'
    
        browser = WebScraper('Chrome')
        browser.open(url)
        browser.web_driver.maximize_window()
       
        years = browser.find_elements('xpath', '//*[@id="pagina"]/table/tbody/tr[6]/td/table/tbody/tr/td/table/tbody/tr[2]/td/a')
        for year in years[-1:]:
            
            data = []
            #print year.text
            time.sleep(2)
            year.click()
            time.sleep(5)
            test = browser.find_element('tag', 'iframe')
            browser.web_driver.switch_to_frame(test)
            #months = browser.find_elements('xpath', '//td/table/tbody/tr[2]//*[@class="intestazione"]')
            #months = browser.find_elements('xpath', '//*[@id="main"]/div/table/tbody/tr/td/table/tbody/tr[2]/td')
    #         for month in months:
    #             time_periods.append(month.text)
            #print time_periods
            
            data_points = browser.find_elements('xpath', '//td/table/tbody/tr/td')
            for data_point in data_points:
                if 'TOTALE' in data_point.text:
                    break
                data.append(data_point.text)
            #print data
            browser.switch_to_parent_window()
            browser.click_button('xpath', '//*[@id="cboxClose"]')
            time.sleep(3)
            newdir_path = create_directory(dir_path, today)
            file_name = data[0].replace(' ','_').replace(':','')
            #print file_name
            data = data[1:]
            chunked_data = chunck_list(data, 15)
            with open('%s%s.csv' % (newdir_path, file_name),'wb') as out_file:
                for d in chunked_data:
                        out_file.write(','.join(d).encode('ascii', 'ignore'))
                        out_file.write('\n')
        
        browser.close()
        print 'Finished scraping at %s.' % datetime.now()
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['clal_cheese_production.py'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('monthly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['clal_cheese_production.py'],[success_msg]]
        save_error_to_log('monthly', msg_list)
    
if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
    
