'''
Created on 17 Jun 2016

@author: Suzanne
'''
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import sys
import time
from datetime import datetime
import os
from function.function import save_error_to_log
from db.manager import DBManager, RAW_DB_NAME, HOST, USERNAME, PASSWORD
from function.function import create_directory, chunck_list, save_download_file
from web.scraper import WebScraper
from web.path import DOWNLOAD_PATH
from web.path import WEB_USDA_PATH


def resume_scrape(flow, flow_id, year, month, prods, dir_path, dir_title, url, counter):
    try:
        wscraper = WebScraper('Chrome')
#         if counter %2 == 0:
#             wscraper = WebScraper('Chrome')
#         else:
#             wscraper = WebScraper('Firefox')
        wscraper.open(url)
        wscraper.web_driver.maximize_window()
        
        # browse standard query page
        wscraper.click_button('id', 'ctl00_ContentPlaceHolder1_lbExpressQuery')
        time.sleep(2)  
        
        # select flow type
        wscraper.load_field('select', 'name', 'ctl00$ContentPlaceHolder1$ddlProductType', flow_id) 
        time.sleep(4)
        
        # search for products with code containing 040
        wscraper.load_field('select', 'name', 'ctl00$ContentPlaceHolder1$ddlProductSearch', 'Code')
        wscraper.load_field('input', 'name', 'ctl00$ContentPlaceHolder1$txtProductSearch', '3501')
        wscraper.click_button('id', 'ctl00_ContentPlaceHolder1_btnProductSearch')
        time.sleep(2)
             
        # select value to display
        wscraper.load_field('select', 'name', 'ctl00$ContentPlaceHolder1$ddlValueType', 'GVAL')
        time.sleep(2)
                     
        # select dollars as value unit
        wscraper.load_field('select', 'name', 'ctl00$ContentPlaceHolder1$ddlValueUnit', 'D')
        time.sleep(2)
         
        # select quantity to display
        wscraper.load_field('select', 'name', 'ctl00$ContentPlaceHolder1$ddlQuantityType', 'Q1')
        time.sleep(2)
         
        # select FAS Non Converted as quantity unit
        wscraper.load_field('select', 'name', 'ctl00$ContentPlaceHolder1$ddlQuantityUnit', 'FASN')
        time.sleep(2)
         
        # select Monthly to display
        wscraper.load_field('select', 'name', 'ctl00$ContentPlaceHolder1$ddlDateSeries', 'Monthly')
        time.sleep(2)
         
        # select start year
        try:
            wscraper.load_field('select', 'name', 'ctl00$ContentPlaceHolder1$ddlStartYear', year)
            time.sleep(2)
#         except:
#             wscraper.close()
#             print 'year on website not presented yet'
#             return
        except Exception as err:
            exc_info = sys.exc_info()
            raise Exception('datas.function.function.save_download_file() error:', exc_info[0], exc_info[1], exc_info[2])
        
        
        # select January as month always, otherwise months are skipped
        wscraper.load_field('select', 'name', 'ctl00$ContentPlaceHolder1$ddlMYStartMonth', '01')

        # select start month
#         try:
#             wscraper.load_field('select', 'name', 'ctl00$ContentPlaceHolder1$ddlMYStartMonth', month)
#             time.sleep(2)
#         except:
#             wscraper.close()
#             print 'month on website not presented yet'
#             return
        
        
        # select all countries
        #countries = wscraper.get_dropdown_list('id', , 'value')
        wscraper.load_field_multiple('//*[@id="ctl00_ContentPlaceHolder1_lb_Partners"]/option', 66, '-')
        time.sleep(2)
        
        # select all products
        action = ActionChains(wscraper.web_driver)
        action.key_down(Keys.CONTROL)
        for prod in prods:
            element = wscraper.find_element('xpath','//*[@id="ctl00_ContentPlaceHolder1_lb_Products"]/option[@value=%s]' % prod)
            action.click(element)
        action.key_up(Keys.CONTROL).perform()
        #wscraper.load_field('select', 'id','ctl00_ContentPlaceHolder1_lb_Products', prod)
        
        # click retrieve data button
        wscraper.click_button('id', 'ctl00_ContentPlaceHolder1_btnRetrieveData')
        
        try:
            wscraper.wait(10, 'id', "ctl00_ContentPlaceHolder1_UltraWebTab1__ctl1_grdExpressQuery_lblNoDataMessage")        
        except:
            # click save as csv button
            wscraper.wait(180, 'id', 'ctl00_ContentPlaceHolder1_UltraWebTab1__ctl1_grdExpressQuery_btn_ExportToExcel')
    
            wscraper.click_button('id', 'ctl00_ContentPlaceHolder1_UltraWebTab1__ctl1_grdExpressQuery_btn_ExportToExcel')
    
            time.sleep(8)
            
            # find the downloaded file and save it as dest_file and remove the original file
            dest_path = create_directory(dir_path, dir_title)
            dest_file = '%sworldtotal_%s_%s.csv' % (dest_path, flow, prod)
            save_download_file(DOWNLOAD_PATH, dest_file)
        else:
            print 'no data available'
    # use this version, otherwise, it won't resume the scraping
    # if web error shows up again
    except Exception, e:
        wscraper.close()
        print 'resume_scrape() error: %s' % e
        return False
#     except Exception as err:
#         wscraper.close()
#         exc_info = sys.exc_info()
#         raise Exception('resume_scrape() error:', exc_info[0], exc_info[1], exc_info[2])
    else:
        wscraper.close()
        return True


def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()
        
        # get the latest data date from DB
#         dbm = DBManager(db_params[0], db_params[1], db_params[2], db_params[3])
#         sql = ('select max(yearmonth) as max_date from usda_trade_flow_dairy')
#         
#         date_from = dbm.get_latest_date_record(sql)
#         #print prod, flows.get(flow_id), date_from
#         #date_from = ['201512','']
#         # if no record in the db, scrape from the earliest date available 1989 Jan
#         if not date_from[0]:
#             date_from = ('200001',)
#         
#         date_from = datetime.strptime(date_from[0], '%Y%m')
#         #date_from += timedelta(days=(date_from.max.day - date_from.day) + 1) # increment month by 1
#         
#         year = datetime.strftime(date_from, '%Y')
#         month = datetime.strftime(date_from, '%m')
#                     
#         del dbm
        
        year = '2016'
        month = '01'
        dir_title = datetime.now().strftime('%Y_%m_%d')
        dir_path = WEB_USDA_PATH + 'trade_flow_casein\\'
        url = 'https://apps.fas.usda.gov/gats/ExpressQuery1.aspx'
    
        flows = {'X':'export', 'G':'import'}
        for flow_id in flows:
            prods = []
            wscraper = WebScraper('Chrome')
            wscraper.open(url)
            wscraper.web_driver.maximize_window()
            
            # browse standard query page
            wscraper.click_button('id', 'ctl00_ContentPlaceHolder1_lbExpressQuery')
            time.sleep(2)  
            
            # select flow type
            wscraper.load_field('select', 'name', 'ctl00$ContentPlaceHolder1$ddlProductType', flow_id) 
            time.sleep(4)
            
            # search for products with code containing 040
            wscraper.load_field('select', 'name', 'ctl00$ContentPlaceHolder1$ddlProductSearch', 'Code')
            wscraper.load_field('input', 'name', 'ctl00$ContentPlaceHolder1$txtProductSearch', '3501')
            wscraper.click_button('id', 'ctl00_ContentPlaceHolder1_btnProductSearch')
            time.sleep(2)
            
            prods = wscraper.get_dropdown_list('id', "ctl00_ContentPlaceHolder1_lb_Products", 'value')
            prods = [p for p in prods if p[:4] == '3501']

            wscraper.close()
            
            #for prod_list in prods:
            counter = 0
            flow = flows[flow_id]
            is_success = resume_scrape(flow, flow_id, year, month, prods, dir_path, dir_title, url, counter)
            
            while is_success == False:
                if counter >= 5:
                    raise Exception('web communication error, exceeds max number of attempts, stop scraping')
                else:
                    print 'at counter %s scraping' % (counter)
                    counter += 1
                    time.sleep(20)
                
                is_success = resume_scrape(flow, flow_id, year, month, prods, dir_path, dir_title, url, counter)
                
                # this means year/month not presented on the website yet, stop scraping for this flow
                if is_success == None:
                    break
        
        print 'Finished scraping at %s.' % datetime.now()
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['usda.trade_flow_casein.py'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('monthly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['usda.trade_flow_casein.py'],[success_msg]]
        save_error_to_log('monthly', msg_list)


if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
    
