'''
Created on 23 May 2016

@author: Suzanne
'''
import time
import sys
import os
from datas.function.function import save_error_to_log
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datas.db.manager import DBManager, RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import create_directory
from datas.function.function import move_download_file
from datas.web.scraper import WebScraper
from datas.web.path import DOWNLOAD_PATH, WEB_STATSNZ_PATH


def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()
        
        # get the latest data date from DB
        dbm = DBManager(db_params[0], db_params[1], db_params[2], db_params[3])


        sql = ('select max(yearmonth) from statsnz_casein_trade;')

        date_from = dbm.get_latest_date_record(sql)
        #date_from=('200912',)
        date_from = datetime.strptime(date_from[0], '%Y%m') - relativedelta(months=2)
        date_from = datetime.strftime(date_from, '%Y%m')
        #print date_from
#         return
        del dbm
         
        # get new yearmonths
        url = 'http://www.stats.govt.nz/infoshare/TradeVariables.aspx?DataType=TEX'
        wscraper = WebScraper('Chrome')
        wscraper.open(url)
        wscraper.web_driver.maximize_window()
        wscraper.click_button('xpath', '/html/body/div[3]/div/a') #get rid of cookie warning
        time.sleep(2)
        wscraper.click_button('id', 'ctl00_MainContent_btnGo')
        time.sleep(4)
        yearmonths = wscraper.get_dropdown_list('name', 'ctl00$MainContent$TimeVariableSelector$lbVariableOptions', 'text')
        wscraper.close()
        yearmonths = [y for y in yearmonths if y.replace('M', '') > date_from]
        #yearmonths=['2010M01','2010M02','2010M03','2010M04']
        # terminate if there are no new data on the website
        if not yearmonths:
            print 'no new data on the website, scraper terminated...'
            return
        
        dir_title = datetime.now().strftime('%Y_%m_%d')
        dir_path = WEB_STATSNZ_PATH + 'statsnz_casein_trade\\'
        folder_path = create_directory(dir_path, dir_title)
        
        # all geo are seperated in two groups
        # get the two geo groups, and construct xpath list
        in_file = open(dir_path + 'geo_groups.csv', 'r')
        rows = in_file.readlines()
        in_file.close()
        
        geo_groups = []
        for row in rows:
            geo_groups.append(['//tr/td/select/option[@value="%s"]' % r for r in row.strip().split(',')])
        
        # start to scrape new data from the website
        for yearmonth in yearmonths:
            for geo_group in geo_groups:
                wscraper = WebScraper('Chrome')
                wscraper.open(url)
                wscraper.web_driver.maximize_window()
                wscraper.click_button('xpath', '/html/body/div[3]/div/a') #get rid of cookie warning
                # select Data type: Total Exports
                #wscraper.click_button('id', 'ctl00_MainContent_rbTER')
                  
                # select Country: select a group of countries together
                wscraper.click_multiple(geo_group)
                  
                # add the countries to the Selected countries box
                wscraper.click_button('id', 'ctl00_MainContent_btnAddCountries')
                
                # select HS code: select products start with 040 for dairy
                # open search box and search '040'
                wscraper.click_button('xpath', '//div/ul/li/a[contains(text(), "Search")]')
                wscraper.load_field('input', 'name', 'hsCodeSearchText', '3501')
                wscraper.click_button('xpath', '//td/div/a[@href="javascript:OnHSCodeSearch();"]')
                time.sleep(4)
                
                # click checkboxes starting with '040'
                wscraper.click_checkbox_by_xpath('//tr/td/div/div/input[starts-with(@value, "350")]')
                
                # add all dairy products to the Selectd HS code box
                wscraper.click_button('id', 'ctl00_MainContent_btnAddSearchCode')
                
                # click 'Go' button to go to next page
                wscraper.click_button('id', 'ctl00_MainContent_btnGo')
                time.sleep(5)
                
                # select time periods: select only one yearmonth to avoid excess data
                wscraper.click_button('xpath', '//tr/td/select/option[contains(text(), "%s")]' % yearmonth)
                time.sleep(2)
                
                # click 'Go'button to go to next page
                wscraper.click_button('id', 'ctl00_MainContent_btnGo')
                time.sleep(10)
                
                # select Edit table: pivot anticlockwise
                wscraper.click_button('xpath', '//tr/td/select/option[@value="pivot_anticlockwise"]')
                time.sleep(2)
                
                # select Edit table: change text code representation
                wscraper.click_button('xpath', '//tr/td/select/option[@value="change_text_code_representation"]')
                time.sleep(2)
                
                # select Code and text
                wscraper.click_button('id', 'ctl00_MainContent_ctlChangeTextCode_rptVariables_ctl01_rbCodeText')
                wscraper.click_button('id', 'ctl00_MainContent_ctlChangeTextCode_rptVariables_ctl02_rbCodeText')
                wscraper.click_button('id', 'ctl00_MainContent_ctlChangeTextCode_rptVariables_ctl03_rbCodeText')
                time.sleep(3)
                try:
                    wscraper.click_button('id', 'ctl00_MainContent_ctlChangeTextCode_btnAccept')
                except:
                    pass
                time.sleep(2)
                
                # select Save table: save data as csv file
                wscraper.click_button('xpath', '//tr/td/select/option[@value="csv"]')
                time.sleep(7)
                
                # click OK button to accept alert
                try:
                    wscraper.accept_alert()
                except:
                    print yearmonth
                    pass
                time.sleep(2)
                
                # save download file
                move_download_file(DOWNLOAD_PATH, folder_path)
                
                wscraper.close()
        
        print 'Finished scraping at %s.' % datetime.now()
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['statsnz.casein_trade.py'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('monthly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['statsnz.casein_trade.py'],[success_msg]]
        save_error_to_log('monthly', msg_list)


if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)

    
