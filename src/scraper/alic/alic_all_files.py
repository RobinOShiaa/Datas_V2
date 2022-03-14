'''
Created on 20 Nov 2015

@author: Sue
'''
import time
import sys
from datetime import datetime
from datas.db.manager import DBManager
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import create_directory, save_download_file, transform_excel_to_csv, save_error_to_log
from datas.web.path import WEB_ALIC_PATH, DOWNLOAD_PATH
from datas.web.scraper import WebScraper


def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()
        
        dir_title = datetime.now().strftime('%Y_%m_%d')
            
        browser = WebScraper('Chrome')
        url = 'http://lin.alic.go.jp/alic/statis/dome/data2/e_nstatis.htm'
        browser.open(url)
        
        # hog slaughtering
        browser.click_button('xpath','html/body/table/tbody/tr[1]/td[3]/table/tbody/tr[4]/td/div/table[5]/tbody/tr[4]/td[3]/font/a') # updates
        #browser.click_button('xpath','html/body/table/tbody/tr[1]/td[3]/table/tbody/tr[4]/td/div/table[5]/tbody/tr[4]/td[4]/font/a') # previous data
        time.sleep(5)
        file_path = create_directory('%shog_slaughtering' % WEB_ALIC_PATH, dir_title)
        save_download_file(DOWNLOAD_PATH, file_path+'hog_slaughtering.xls')
        new_path = file_path + 'hog_slaughtering.xls'
        csv_path = file_path + 'hog_slaughtering'
        transform_excel_to_csv(new_path,csv_path)
        
        # import by origin
        xpath_list = ['html/body/table/tbody/tr[1]/td[3]/table/tbody/tr[4]/td/div/table[5]/tbody/tr[8]/td[3]/font/a',
                      'html/body/table/tbody/tr[1]/td[3]/table/tbody/tr[4]/td/div/table[5]/tbody/tr[9]/td[3]/font/a']
    
        for xpath in xpath_list:
            browser.click_button('xpath',xpath)
            time.sleep(5)
            file_path = create_directory('%simport_by_origin' % WEB_ALIC_PATH, dir_title)
            save_download_file(DOWNLOAD_PATH, file_path+'import_by_origin%s.xls' % xpath_list.index(xpath))
            new_path = file_path+'import_by_origin%s.xls' % xpath_list.index(xpath)
            csv_path = file_path+'import_by_origin%s' % xpath_list.index(xpath)
            transform_excel_to_csv(new_path,csv_path)
        
        
        # import price
        browser.click_button('xpath', 'html/body/table/tbody/tr[1]/td[3]/table/tbody/tr[4]/td/div/table[5]/tbody/tr[7]/td[3]/font/a')
        time.sleep(3)
        file_path = create_directory('%simport_price' % WEB_ALIC_PATH, dir_title)
        save_download_file(DOWNLOAD_PATH, file_path+'import_price.xls')
        new_path = file_path + 'import_price.xls'
        csv_path = file_path + 'import_price'
        transform_excel_to_csv(new_path,csv_path)
        
        
        # import quantity
        browser.click_button('xpath', 'html/body/table/tbody/tr[1]/td[3]/table/tbody/tr[4]/td/div/table[5]/tbody/tr[6]/td[3]/font/a')
        time.sleep(3)
        file_path = create_directory('%simport_quantity' % WEB_ALIC_PATH, dir_title)
        save_download_file(DOWNLOAD_PATH, file_path+'import_quantity.xls')
        new_path = file_path + 'import_quantity.xls'
        csv_path = file_path + 'import_quantity'
        transform_excel_to_csv(new_path,csv_path)
        
        
        # num farms inventory
    #     browser.click_button('xpath','/html/body/table/tbody/tr[1]/td[3]/table/tbody/tr[4]/td/div/table[5]/tbody/tr[15]/td[5]/font/a')
    #     time.sleep(3)
    #     file_path = create_directory('%snum_farms_inventory' % WEB_ALIC_PATH, dir_title)
    #     save_download_file(DOWNLOAD_PATH, file_path+'num_farms_inventory.xls')
    #     new_path = file_path + 'num_farms_inventory.xls'
    #     csv_path = file_path + 'num_farms_inventory'
    #     transform_excel_to_csv(new_path,csv_path)
        
        
        # pork retail price
        browser.click_button('xpath','/html/body/table/tbody/tr[1]/td[3]/table/tbody/tr[4]/td/div/table[5]/tbody/tr[13]/td[3]/font/a')
        time.sleep(3)
        file_path = create_directory('%spork_retail_price' % WEB_ALIC_PATH, dir_title)
        save_download_file(DOWNLOAD_PATH, file_path+'pork_retail_price.xls')
        new_path = file_path + 'pork_retail_price.xls'
        csv_path = file_path + 'pork_retail_price'
        transform_excel_to_csv(new_path,csv_path)
        
        
        # pork supply demand
        browser.click_button('xpath','/html/body/table/tbody/tr[1]/td[3]/table/tbody/tr[4]/td/div/table[5]/tbody/tr[3]/td[3]/font/a')
        time.sleep(3)
        file_path = create_directory('%spork_supply_demand' % WEB_ALIC_PATH, dir_title)
        save_download_file(DOWNLOAD_PATH, file_path+'pork_supply_demand.xls')
        new_path = file_path + 'pork_supply_demand.xls'
        csv_path = file_path + 'pork_supply_demand'
        transform_excel_to_csv(new_path,csv_path)
        
        
        # wholesale carcass price
        browser.click_button('xpath','/html/body/table/tbody/tr[1]/td[3]/table/tbody/tr[4]/td/div/table[5]/tbody/tr[12]/td[3]/font/a')
        time.sleep(3)
        file_path = create_directory('%swholesale_carcass_price' % WEB_ALIC_PATH, dir_title)
        save_download_file(DOWNLOAD_PATH, file_path+'wholesale_carcass_price.xls')
        new_path = file_path + 'wholesale_carcass_price.xls'
        csv_path = file_path + 'wholesale_carcass_price'
        transform_excel_to_csv(new_path,csv_path)
        
        
        browser.close()
        print 'Finish scraping at %s.' % datetime.now()
    except Exception as err:
        
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['alic_all_files'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n\n']]
        save_error_to_log('monthly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['alic_all_files'],[success_msg]]
        save_error_to_log('monthly', msg_list)


if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
