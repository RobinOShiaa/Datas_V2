'''
Created on 18 Jan 2016

@author: Suzanne
'''
import sys
import os
from datas.function.function import save_error_to_log
from datetime import datetime
import time
import pandas as pd
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.web.scraper import WebScraper
from datas.web.path import DOWNLOAD_PATH, WEB_MPI_NZ_PATH
from datas.function.function import move_download_file, create_directory,\
    get_download_file_name, delete_file

def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()
        url='https://www.mpi.govt.nz/news-and-resources/statistics-and-forecasting/agriculture/livestock-slaughter-statistics/'
        today = datetime.now().strftime('%Y_%m_%d')
         
        scraper = WebScraper('Chrome')
        scraper.open(url)
        scraper.click_button('xpath', '//*[@id="main-content"]/p[2]/a')
        time.sleep(5)
        scraper.close()
        
        dir_path = create_directory(WEB_MPI_NZ_PATH, today)
        filename = get_download_file_name(DOWNLOAD_PATH)
        filename = filename.split('\\')[-1]
    
        move_download_file(DOWNLOAD_PATH, dir_path)
        
        xl = pd.ExcelFile(dir_path+filename)
    
        sheet_names = xl.sheet_names  # see all sheet names
        for sheet_name in sheet_names:
            df = xl.parse(sheet_name)
            df.to_csv('%s%s.csv' % (dir_path, sheet_name), index=False)
            
        delete_file(dir_path+filename)
        print 'Finish scraping at %s...' % datetime.now()
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['mpi_nz.animal_slaughters'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n\n']]
        save_error_to_log('monthly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['mpi_nz.animal_slaughters'],[success_msg]]
        save_error_to_log('monthly', msg_list) 

if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
    