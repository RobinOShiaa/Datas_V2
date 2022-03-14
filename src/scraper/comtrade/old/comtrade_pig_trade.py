'''
Created on 11 Nov 2014

@author: Suzanne

28/01/2015(Wenchong): Automation completed.
12/02/2015(Wenchong): Fixed sql query to get the correct date as a new scraping point.
08/04/2015(Wenchong): Added error handling, if error occurs, try up to 5 scraping attempts.
'''


import time
from datetime import datetime
from datetime import timedelta
from selenium.webdriver.common.keys import Keys
from datas.db.manager import DBManager
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import create_directory
from datas.function.function import save_download_file
from datas.web.path import DOWNLOAD_PATH
from datas.web.path import WEB_COMTRADE_PATH
from datas.web.scraper import WebScraper


def resume_scrape(url, username, password, reporter, partner, commodities, date_from, dest_file):
    try:
        scraper = WebScraper('Chrome')
        
        #log in - must have existing account with site
        scraper.open(url)
        #scraper.web_driver.maximize_window()
        scraper.load_field('input', 'id', "ctl00_MainContent_LoginUser_UserName", username)
        scraper.load_field('input', 'id', "ctl00_MainContent_LoginUser_Password", password)
        scraper.click_button('id', "ctl00_MainContent_LoginUser_RememberMe")
        scraper.click_button('id', "ctl00_MainContent_LoginUser_LoginButton")
        time.sleep(5)
        
        # fill in reporter
        element1 = scraper.web_driver.find_element_by_id('token-input-ctl00_MainContent_ReporterBox')
        element1.send_keys(reporter)
        time.sleep(3)
        element1.send_keys(Keys.RETURN)
        time.sleep(3)
        
        # fill in partner
        element2 = scraper.web_driver.find_element_by_id('token-input-ctl00_MainContent_PartnerBox')
        element2.send_keys(partner)
        time.sleep(3)
        element2.send_keys(Keys.RETURN)
        time.sleep(3)
        
        #time period
        while date_from < datetime.now():
            date_from += timedelta(days=(date_from.max.day - date_from.day) + 1) # increment month by 1
            date = datetime.strftime(date_from, '%B %Y')
            element4 = scraper.web_driver.find_element_by_id('token-input-ctl00_MainContent_YearPeriodBox')
            element4.send_keys(date)
            time.sleep(3)
            element4.send_keys(Keys.RETURN)
            time.sleep(3)
    
        #commodity
        for commodity in commodities:
            element3 = scraper.web_driver.find_element_by_id('token-input-ctl00_MainContent_CommodityBox')
            element3.send_keys(commodity)
            time.sleep(5)
            element3.send_keys(Keys.RETURN)
            time.sleep(3)
        
        #downloading & renaming file        
        scraper.click_button('id', 'GetDataButton')
        time.sleep(15)
        
        # download file from the page
        save_download_file(DOWNLOAD_PATH, dest_file)
    except Exception, e:
        scraper.close()
        print 'scrape() --> resume_scrape() error: %s' % e
        return False
    else:
        scraper.close()
        return True


def scrape(db_params):
    print 'Start scraping at %s...' % datetime.now()
    
    url = 'http://comtrade.un.org/monthly/Account/Login.aspx'
    
    #reporters = ['Australia', 'Brazil', 'Canada', 'Chile', 'Mexico']
    # don't need Canada
    reporters = ['Australia', 'Brazil', 'Chile', 'Mexico']
    all_partners = 'all'
    commodities = ['0203', '020311', '020312','020319','020321','020322','020329']
    
    today = datetime.now().strftime("%Y_%m_%d")
    username = 'smccarthy13@gmail.com'
    password = '123dairy123'
    
    dest_path = create_directory('%spig_trade\\' % WEB_COMTRADE_PATH, today)
    
    for reporter in reporters:
        # get the latest data date from DB
        dbm = DBManager(db_params[0], db_params[1], db_params[2], db_params[3])
        
        sql = ('select max(yearmonth) from comtrade_pig_trade where reporter = "%s";' % reporter)
        date_from = dbm.get_latest_date_record(sql)
        # need to scrape initial data for Canada (probably some other countries)
        if date_from[0] != None:
            date_from = datetime.strptime(date_from[0], '%Y%m')
        else:
            date_from = datetime.strptime('201101', '%Y%m')
        
        dest_file = '%s%s.csv' % (dest_path, reporter)
        
        # fill in the fields in the page
        counter = 0
        while not resume_scrape(url, username, password, reporter, all_partners, commodities, date_from, dest_file):
            if counter >= 5:
                raise Exception('web communication error, exceeds max number of attempts, stop scraping')
            else:
                print 'scrape %s at counter %s...' % (reporter, counter)
                counter += 1
    
    print 'Finish scraping at %s...' % datetime.now()


if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)