'''
Created on 20 Jan 2015

@author: Conor


13/03/2015(Wenchong): Moved two functions to datas.function. Put the scraper
in the scrape() function.
TODO(Wenchong): 13/03/2015 scrape data to sub-directories.
'''


import os
import time
from datetime import datetime
from os.path import expanduser
from datas.db.manager import DBManager
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import create_directory
from datas.function.function import transform_excel_to_csv
from datas.web.path import WEB_ALIC_PATH
from datas.web.scraper import WebScraper    


def scrape(db_params):
    browser = WebScraper('Chrome')
    
    url = 'http://lin.alic.go.jp/alic/statis/dome/data2/e_nstatis.htm'
    
    browser.open(url)
    
    xpath_list = [# pork_supply_demand
                  'html/body/table/tbody/tr[1]/td[3]/table/tbody/tr[4]/td/div/table[5]/tbody/tr[3]/td[3]/font/a',#recent
                  'html/body/table/tbody/tr[1]/td[3]/table/tbody/tr[4]/td/div/table[5]/tbody/tr[3]/td[4]/font/a',#historical
                  # hog_slaughtering
                  'html/body/table/tbody/tr[1]/td[3]/table/tbody/tr[4]/td/div/table[5]/tbody/tr[4]/td[3]/font/a',#recent
                  'html/body/table/tbody/tr[1]/td[3]/table/tbody/tr[4]/td/div/table[5]/tbody/tr[4]/td[4]/font/a',#historical
                  # import_quantity
                  'html/body/table/tbody/tr[1]/td[3]/table/tbody/tr[4]/td/div/table[5]/tbody/tr[6]/td[3]/font/a',#recent
                  'html/body/table/tbody/tr[1]/td[3]/table/tbody/tr[4]/td/div/table[5]/tbody/tr[6]/td[4]/font/a',#historical
                  # import_price
                  'html/body/table/tbody/tr[1]/td[3]/table/tbody/tr[4]/td/div/table[5]/tbody/tr[7]/td[3]/font/a',#recent
                  'html/body/table/tbody/tr[1]/td[3]/table/tbody/tr[4]/td/div/table[5]/tbody/tr[7]/td[4]/font/a',#historical
                  # import_by_origin
                  'html/body/table/tbody/tr[1]/td[3]/table/tbody/tr[4]/td/div/table[5]/tbody/tr[8]/td[3]/font/a',#recent
                  'html/body/table/tbody/tr[1]/td[3]/table/tbody/tr[4]/td/div/table[5]/tbody/tr[8]/td[4]/font/a',#historical
                  'html/body/table/tbody/tr[1]/td[3]/table/tbody/tr[4]/td/div/table[5]/tbody/tr[9]/td[3]/font/a',#recent
                  'html/body/table/tbody/tr[1]/td[3]/table/tbody/tr[4]/td/div/table[5]/tbody/tr[9]/td[4]/font/a',#historical
                  # wholesale_carcass_price
                  'html/body/table/tbody/tr[1]/td[3]/table/tbody/tr[4]/td/div/table[5]/tbody/tr[11]/td[3]/font/a',#recent
                  'html/body/table/tbody/tr[1]/td[3]/table/tbody/tr[4]/td/div/table[5]/tbody/tr[11]/td[4]/font/a',#historical
                  # pork_retail_price
                  'html/body/table/tbody/tr[1]/td[3]/table/tbody/tr[4]/td/div/table[5]/tbody/tr[12]/td[3]/font/a',#recent
                  'html/body/table/tbody/tr[1]/td[3]/table/tbody/tr[4]/td/div/table[5]/tbody/tr[12]/td[4]/font/a',#historical
                  # num_farms_inventory
                  'html/body/table/tbody/tr[1]/td[3]/table/tbody/tr[4]/td/div/table[5]/tbody/tr[13]/td[3]/font/a',#recent
                  'html/body/table/tbody/tr[1]/td[3]/table/tbody/tr[4]/td/div/table[5]/tbody/tr[13]/td[4]/font/a']#historical
    
    file_name_list = ['4(1)A.xls','4(1)AF.xls','4(2)A.xls','4(2)AF.xls','4(6)AA.xls','4(6)AAF.xls','4(6)BA.xls','4(6)BAF.xls',
                      '4(6)C1A.xls','4(6)C1AF.xls','4(6)C2A.xls','4(6)C2AF.xls','4(4)aA.xls','4(4)aAF.xls','4(4)bA.xls','4(4)bAF.xls',
                      '4(5)A.xls','4(5)AF.xls']
    
    #xpath_category = 'html/body/table/tbody/tr[1]/td[3]/table/tbody/tr[4]/td/div/table[5]/tbody/tr[3]/td[2]/font'
    row_nums = [3,4,6,7,8,9,11,12,13]
    
    category_list = []
    
    for row_num in row_nums:
        xpath_category = 'html/body/table/tbody/tr[1]/td[3]/table/tbody/tr[4]/td/div/table[5]/tbody/tr[' + str(row_num) + ']/td[2]/font'
        ending_list = ['_recent','_historical']
        for ending in ending_list:
            category = browser.find_element('xpath', xpath_category).text.strip().replace(" ","_") + ending
            category_list.append(category)
    
    #print browser.find_element('xpath', xpath_category).text.strip().replace(" ","_")
    
    for xpath in xpath_list:
        browser.click_button('xpath',xpath)
        time.sleep(3)
    
    home = expanduser("~")
    downloads_dir = os.chdir(home + '\Downloads')
    
    #recent_file_name = '4(4)aAF.xls'
    #past_file_name = '4(4)aA.xls'
    
    dir_title = datetime.now().strftime('%Y_%m_%d')
    file_path = create_directory(WEB_ALIC_PATH, dir_title)
    
    for file_name in xrange(0,len(file_name_list)):
        old_path = home + '\Downloads' + '\\' + file_name_list[file_name]
        
        new_path = file_path + '\\' + category_list[file_name] + '.xls'
        
        if os.path.isfile(new_path) != True:
            os.rename(old_path,new_path)
        
        if os.path.isfile(old_path) == True:
            os.remove(old_path)    
    
    browser.close()
    
    for xsl in xrange(0,len(category_list)):
        new_path = file_path + "\\" + category_list[xsl] + '.xls'
        csv_path = file_path + "\\" + category_list[xsl]
        transform_excel_to_csv(new_path,csv_path)


if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)