'''
Created on 24 Nov 2014

@author: Suzanne
'''

#from selenium.webdriver.common.action_chains import ActionChains
import time
from datetime import datetime
#import os
#from datas.db.manager import DBManager
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.web.scraper import WebScraper
from datas.web.path import DOWNLOAD_PATH, WEB_OECD_PATH
from datas.function.function import create_directory, delete_file, save_download_file


def try_scrape(url):

    try:
        scraper = WebScraper('Chrome')
        scraper.web_driver.implicitly_wait(100)
        
        scraper.open(url)
        scraper.web_driver.maximize_window()
         
        #Select from directories
        scraper.click_button('xpath', '//*[@id="browsethemes"]/ul/li[14]') # Monthly Economic Indicators
        scraper.click_button('xpath', '//*[@id="browsethemes"]/ul/li[14]/ul/li[1]') # Composite Leading Indicators
        scraper.click_button('xpath', '//*[@id="browsethemes"]/ul/li[14]/ul/li[1]/ul/li') # Composite Leading Indicators (MEI)
        scraper.click_button('xpath', '//*[@id="browsethemes"]/ul/li[14]/ul/li[1]/ul/li/ul/li[1]/a[2]') # Composite Leading Indicators (MEI)

        time.sleep(5)
         
        #Results
        scraper.load_field('select', 'id', 'PDim_SUBJECT', '7~LORSGPNO')
        time.sleep(5)

        #scraper.hover('xpath','//*[@id="menubar-export"]/a/span[1]/span[2]')
        #print 'hovering'
        scraper.click_button('xpath', '//*[@id="menubar-export"]/a/span[1]/span[2]')
        time.sleep(3)
        scraper.click_button('xpath', '//*[@id="menubar-export"]/a/span[1]/span[2]')
        time.sleep(3)
        #scraper.wait(15, 'xpath', '//*[@id="ui-menu-1-1"]')
        #scraper.hover('xpath','//*[@id="ui-menu-1-1"]')
        
        scraper.wait(15, 'xpath', '//*[@id="ui-menu-1-1"]')
        scraper.click_button('xpath', '//*[@id="ui-menu-1-1"]')
        #print 'results' 
        #Get control of pop-up window
        scraper.web_driver.switch_to_frame("DialogFrame")
        time.sleep(5)
        scraper.click_button('xpath', '//*[@id="_ctl12_btnExportCSV"]')
        time.sleep(45)
        #print 'got control of popup'

    except:
        scraper.close()
        return False
    else:
        scraper.close()
        
        #Move and rename file
        today = datetime.now().strftime("%Y_%m_%d")
        #src_file = '%sMEI_CLI.csv' % (DOWNLOAD_PATH)
        dest_path = '%snormalised_gdp' % WEB_OECD_PATH
        dest_path = create_directory(dest_path, today)
        save_download_file(DOWNLOAD_PATH, '%snormalised_gdp.csv' % dest_path)
        #os.rename(src_file, '%snormalised_gdp.csv' % dest_path)
        #Extract only Normalised GDP data
        with open('%snormalised_gdp.csv' % dest_path) as r, open('%snormalised_gdp_data.csv' % dest_path, "w") as out_file:
            headers=r.next()
            out_file.write('url,%s,\n' % url)
            out_file.write(headers)
             
            rows = [row for row in r if 'LORSGPNO' in row]
            for row in rows:
                out_file.write(row)
         
        delete_file('%snormalised_gdp.csv' % dest_path)
        #scraper.close()
        return True

        #Export button
        scraper.click_button('xpath', '//*[@id="menubar-export"]/a/span[1]/span[2]')
        time.sleep(3)
        
        #scraper.wait(15, 'xpath', '//*[@id="ui-menu-1-1"]')
        #scraper.hover('xpath','//*[@id="ui-menu-1-1"]')
        
        scraper.wait(15, 'xpath', '//*[@id="ui-menu-2-0"]')#//*[@id="menubar-export"]/a/span[1]/span[2]
        scraper.click_button('xpath', '//*[@id="ui-menu-2-0"]')
        #print 'results' 
        #Get control of pop-up window
        scraper.web_driver.switch_to_frame("DialogFrame")
        time.sleep(5)
        scraper.click_button('xpath', '//*[@id="_ctl12_btnExportCSV"]')
        time.sleep(45)
        #print 'got control of popup'

#     except:
#         scraper.close()
#         return False
#     else:
#         scraper.close()
#         
#         #Move and rename file
#         today = datetime.now().strftime("%Y_%m_%d")
#         #src_file = '%sMEI_CLI.csv' % (DOWNLOAD_PATH)
#         dest_path = '%snormalised_gdp' % WEB_OECD_PATH
#         dest_path = create_directory(dest_path, today)
#         save_download_file(DOWNLOAD_PATH, '%snormalised_gdp.csv' % dest_path)
#         #os.rename(src_file, '%snormalised_gdp.csv' % dest_path)
#         #Extract only Normalised GDP data
#         with open('%snormalised_gdp.csv' % dest_path) as r, open('%snormalised_gdp_data.csv' % dest_path, "w") as out_file:
#             headers=r.next()
#             out_file.write('url,%s,\n' % url)
#             out_file.write(headers)
#              
#             rows = [row for row in r if 'LORSGPNO' in row]
#             for row in rows:
#                 out_file.write(row)
#          
#         delete_file('%snormalised_gdp.csv' % dest_path)
#         #scraper.close()
#         return True
        

def scrape(db_params):
    print 'Start scraping at %s...' % datetime.now()
    
    url = 'http://stats.oecd.org/'
    counter = 0
    while not try_scrape(url):
        if counter >= 5:
            raise Exception('web communication error, exceeds max number of attempts, stop scraping')
        else:
            print 'Trying scrape at counter %s...' % (counter)
            counter +=1 
        
    print 'Finished scraping at %s' % datetime.now()


if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
