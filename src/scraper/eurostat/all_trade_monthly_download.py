'''
Created on 31 Aug 2015

@author: Suzanne
'''
import sys
from datas.function.function import save_error_to_log
import time
from datetime import datetime
from datas.web.path import WEB_EUROSTAT_PATH
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.web.scraper import WebScraper
from datas.web.path import DOWNLOAD_PATH
from datas.function.function import create_directory, unzip,delete_file,\
    get_download_file_name

def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()
        #//*[@id="unique_id"]/tbody/tr[2]
        #'''pig download'''
        dir_title = datetime.now().strftime('%Y_%m_%d')
        wscraper = WebScraper('Chrome')
        url = "http://epp.eurostat.ec.europa.eu/newxtweb/"
        wscraper.open(url)
        
        dir_path_dairy = '%sdairy_trade\\' % WEB_EUROSTAT_PATH
        dir_path_meat = '%spig_meat_trade\\' % WEB_EUROSTAT_PATH
        dir_path_casein = '%scasein_trade\\' % WEB_EUROSTAT_PATH
        dir_path_dairy = create_directory(dir_path_dairy, dir_title)
        dir_path_meat = create_directory(dir_path_meat, dir_title)
        dir_path_casein = create_directory(dir_path_casein, dir_title)

        
        #email = "cosullivan@computing.dcu.ie"
        #password = "DATASdcu1234#"
        email = "smccarthy@computing.dcu.ie"
        password = "DATAS$123piggy"
        
        
        wscraper.click_button('xpath','//*[@id="content"]/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr/td[4]/div/a')
        time.sleep(3)
        wscraper.load_field('input','id','username',email)
        wscraper.click_button('xpath', '//*[@id="whoamiForm"]/input[2]')
        time.sleep(3)
        wscraper.load_field('input','id','password',password)
        wscraper.click_button('xpath', '//*[@id="loginForm"]/div/input')
        time.sleep(5)
        
        
        
         
        #wscraper.login_eurostat_query(email, password)
     
        completed_xpath = ".//*[@id='content']/table[1]/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr/td[12]/div/a"
        wscraper.click_button('xpath',completed_xpath)
        time.sleep(4)
    
        rows = wscraper.find_elements('xpath',".//table[@class='sortable']//tr[@class='text2']")
        
        for row in rows:
            if 'Output' in row.text:
                print row.text
                download_button = row.find_element_by_xpath(".//tr/td/img[@alt = 'Download completed work']")#[contains(@id,'download')]")
                download_button.click()

                time.sleep(4)

                download_dir = get_download_file_name(DOWNLOAD_PATH)

                if 'dairy' in row.text:
                    dir_path = dir_path_dairy
                if 'meat' in row.text:
                    dir_path = dir_path_meat
                if 'casein' in row.text:
                    dir_path = dir_path_casein

        
                unzip(download_dir,dir_path)
                delete_file(download_dir)
                   
        wscraper.close()
        print 'Finished scraping at %s.' % datetime.now()
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['eurostat.all_trade_monthly_download.py'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('monthly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['eurostat.all_trade_monthly_download.py'],[success_msg]]
        save_error_to_log('monthly', msg_list)


if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
    
