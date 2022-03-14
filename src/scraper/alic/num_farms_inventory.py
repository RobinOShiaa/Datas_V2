'''
Created on 20 Jan 2015

@author: Conor


13/03/2015(Wenchong): Moved two functions to datas.function. Put the scraper
in the scrape() function.
14/04/2015(Wenchong): Scrape data to sub-directories.
15/07/2015(Sue): Find most recently downloaded file
'''
import time
from datetime import datetime
#from datas.db.manager import DBManager
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import create_directory, save_download_file, transform_excel_to_csv
from datas.web.path import WEB_ALIC_PATH, DOWNLOAD_PATH
from datas.web.scraper import WebScraper    


def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()
        
        dir_title = datetime.now().strftime('%Y_%m_%d')
        file_path = create_directory('%snum_farms_inventory' % WEB_ALIC_PATH, dir_title)
        
        browser = WebScraper('Chrome')
        url = 'http://lin.alic.go.jp/alic/statis/dome/data2/e_nstatis.htm'
        browser.open(url)
        
        #browser.click_button('xpath','html/body/table/tbody/tr[1]/td[3]/table/tbody/tr[4]/td/div/table[5]/tbody/tr[13]/td[3]/font/a')
        browser.click_button('xpath','/html/body/table/tbody/tr[1]/td[3]/table/tbody/tr[4]/td/div/table[5]/tbody/tr[15]/td[5]/font/a')
        time.sleep(5)
        save_download_file(DOWNLOAD_PATH, file_path+'num_farms_inventory.xls')
        
        browser.close()
    
        new_path = file_path + 'num_farms_inventory.xls'
        csv_path = file_path + 'num_farms_inventory'
        transform_excel_to_csv(new_path,csv_path)
        
        print 'Finish scraping at %s...' % datetime.now()
    except Exception as err:
        import sys
        from datas.function.function import save_error_to_log
        exc_info = sys.exc_info()
        error_msg = '\n\nauto_run() scrape error:'
        msg_list = [[sys.argv[0]],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n\n']]
        save_error_to_log('monthly', msg_list)

if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
    
