'''
Created on 18 Nov 2014

@author: Wenchong

28/01/2015(Wenchong): Automation completed.
'''
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime#, date
from datas.db.manager import DBManager
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import create_directory, chunck_list
from datas.function.function import save_download_file
from datas.web.scraper import WebScraper
from datas.web.path import DOWNLOAD_PATH
from datas.web.path import WEB_USDA_PATH
import sys
import os
from datas.function.function import save_error_to_log


def resume_scrape(flow, flow_id, year, month, prod_list, dir_path, dir_title, url, counter):
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
        
        # search for products with code containing 0203
        wscraper.load_field('select', 'name', 'ctl00$ContentPlaceHolder1$ddlProductSearch', 'Code') 
        wscraper.load_field('input', 'name', 'ctl00$ContentPlaceHolder1$txtProductSearch', '02')
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
        except:
            wscraper.close()
            print 'year on website not presented yet'
            return
        
        # select January as month, otherwise months are skipped
        wscraper.load_field('select', 'name', 'ctl00$ContentPlaceHolder1$ddlMYStartMonth', '01')
        time.sleep(4)
        # select start month
    #         try:
    #             wscraper.load_field('select', 'name', 'ctl00$ContentPlaceHolder1$ddlMYStartMonth', month)
    #             time.sleep(2)
    #         except:
    #             wscraper.close()
    #             print 'month on website not presented yet'
    #             return
        
        # select all countries
        wscraper.load_field_multiple('//*[@id="ctl00_ContentPlaceHolder1_lb_Partners"]/option', 33, '-')

        # select products
        action = ActionChains(wscraper.web_driver)
        action.key_down(Keys.CONTROL)
        for prod in prod_list:
            #print prod
            element = wscraper.find_element('xpath','//*[@id="ctl00_ContentPlaceHolder1_lb_Products"]/option[@value=%s]' % prod)
            action.click(element)
        action.key_up(Keys.CONTROL).perform()
        #wscraper.load_field('select', 'id','ctl00_ContentPlaceHolder1_lb_Products', prod)
        
        # click retrieve data button
        wscraper.click_button('id', 'ctl00_ContentPlaceHolder1_btnRetrieveData')
        time.sleep(15)
        
        try:
            wscraper.click_button('id', 'ctl00_ContentPlaceHolder1_UltraWebTab1__ctl1_grdExpressQuery_btn_ExportToExcel')
            time.sleep(10)
            dest_path = create_directory(dir_path, dir_title)
            dest_file = '%sworldtotal_%s_%s.csv' % (dest_path, flow, prod_list[0])
            print dest_file
            save_download_file(DOWNLOAD_PATH, dest_file)
        except:
            pass
        
#         try:
#             wscraper.wait(10, 'id', "ctl00_ContentPlaceHolder1_UltraWebTab1__ctl1_grdExpressQuery_lblNoDataMessage")        
#             
#         except:
#             # click save as csv button
#             wscraper.wait(20, 'id', 'ctl00_ContentPlaceHolder1_UltraWebTab1__ctl1_grdExpressQuery_btn_ExportToExcel')
#     
#             wscraper.click_button('id', 'ctl00_ContentPlaceHolder1_UltraWebTab1__ctl1_grdExpressQuery_btn_ExportToExcel')
#     
#             time.sleep(8)
#             
#             # find the downloaded file and save it as dest_file and remove the original file
#             dest_path = create_directory(dir_path, dir_title)
#             dest_file = '%sworldtotal_%s_%s.csv' % (dest_path, flow, prod_list[0])
#             save_download_file(DOWNLOAD_PATH, dest_file)
#         else:
#             print 'no data available'    
    except Exception, e:
        wscraper.close()
        print 'resume_scrape() error: %s' % e
        return False
    else:
        wscraper.close()
        return True


def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()
        
        # get the latest data date from DB
        dbm = DBManager(db_params[0], db_params[1], db_params[2], db_params[3])
        sql = ('select max(yearmonth) as max_date from usda_trade_flow_pig;')
        date_from = dbm.get_latest_date_record(sql)
        #date_from = '200001'
        try:
            date_from = datetime.strptime(date_from[0], '%Y%m')
        except:
            date_from = '200001'
            date_from = datetime.strptime(date_from, '%Y%m')
        
        #date_from += timedelta(days=(date_from.max.day - date_from.day) + 1) # increment month by 1
        year = datetime.strftime(date_from, '%Y')
        month = datetime.strftime(date_from, '%m')
        del dbm
       
        url = 'http://apps.fas.usda.gov/gats/ExpressQuery1.aspx'
        dir_path = WEB_USDA_PATH + 'trade_flow_meat\\'
        dir_title = datetime.now().strftime('%Y_%m_%d')
        
        flows = {'X':'exports', 'G':'imports'}
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
            time.sleep(7)
            
            # search for products with code containing 0203
            wscraper.load_field('select', 'name', 'ctl00$ContentPlaceHolder1$ddlProductSearch', 'Code')
            wscraper.load_field('input', 'name', 'ctl00$ContentPlaceHolder1$txtProductSearch', '02')
            wscraper.click_button('id', 'ctl00_ContentPlaceHolder1_btnProductSearch')
            time.sleep(5)
    
            prods = wscraper.get_dropdown_list('id', "ctl00_ContentPlaceHolder1_lb_Products", 'value')
            prods = [p for p in prods if p[:2] == '02']
            prods = chunck_list(prods, 10)
    
            wscraper.close()
                
            for prod_list in prods:
                #print prod, flows.get(flow_id)
                
                counter = 0
                flow = flows[flow_id]
                is_success = resume_scrape(flow, flow_id, year, month, prod_list, dir_path, dir_title, url, counter)
                    
                while is_success == False:
                    if counter >= 5:
                        raise Exception('web communication error, exceeds max number of attempts, stop scraping')
                    else:
                        print 'at counter %s scraping %s...' % (counter, prod_list[0])
                        counter += 1
                        time.sleep(20)
                    
                    is_success = resume_scrape(flow, flow_id, year, month, prod_list, dir_path, dir_title, url, counter)
                    
                    # this means year/month not presented on the website yet, stop scraping for this flow
                    if is_success == None:
                        break
        
        print 'Finished scraping at %s.' % datetime.now()
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['usda.trade_flow_pig.py'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('monthly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['usda.trade_flow_pig.py'],[success_msg]]
        save_error_to_log('monthly', msg_list)


if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)

    
