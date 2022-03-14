'''
Created on 3 Feb 2015

@author: Suzanne

08/04/2015(Wenchong): Added error handling, if error occurs, try up to 5 scraping attempts.
'''


import time
from datetime import datetime
from selenium.webdriver.common.keys import Keys
from datas.db.manager import DBManager
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import create_directory
from datas.function.function import read_from_file
from datas.function.function import save_download_file
from datas.web.path import DOWNLOAD_PATH
from datas.web.path import WEB_COMTRADE_PATH
from datas.web.scraper import WebScraper


def resume_scrape(url, username, password, reporter, partner, commodity, date_from, dest_file):
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
        time.sleep(5)
        element1.send_keys(Keys.RETURN)
        time.sleep(4)
        
        # fill in partner
        element2 = scraper.web_driver.find_element_by_id('token-input-ctl00_MainContent_PartnerBox')
        element2.send_keys(partner)
        time.sleep(5)
        element2.send_keys(Keys.RETURN)
        time.sleep(4)
        
        # fill in commodity
        element3 = scraper.web_driver.find_element_by_id('token-input-ctl00_MainContent_CommodityBox')
        element3.send_keys('0'+commodity)
        time.sleep(5)
        element3.send_keys(Keys.RETURN)
        time.sleep(4)
        
        # fill in period. Comment this section out for initial scrape
        element4 = scraper.web_driver.find_element_by_id('token-input-ctl00_MainContent_YearPeriodBox')
        element4.send_keys(date_from)
        time.sleep(3)
        element4.send_keys(Keys.RETURN)
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
    
    #reporters = ['Canada', 'Brazil', 'Mexico', 'Chile', 'Australia', 'India', 'Paraguay', 'Uruguay', 'New Zealand', 'Belarus']
    # don't need Canada
    reporters = ['Brazil', 'Mexico', 'Chile', 'Australia', 'India', 'Paraguay', 'Uruguay', 'New Zealand', 'Belarus']
    
    all_partners = 'all'
    product_labels = read_from_file('%smeat_trade\\products.csv' % (WEB_COMTRADE_PATH))
    commodities = [p[0] for p in product_labels]
    
    
    today = datetime.now().strftime("%Y_%m_%d")
    username = 'smccarthy13@gmail.com'
    password = '123dairy123'
    
    # get the latest data date from DB
    dbm = DBManager(db_params[0], db_params[1], db_params[2], db_params[3])
    sql = ('select max(yearmonth) as max_date from comtrade_all_meat_trade '
           'group by hs_code order by max_date asc limit 1;')
    date_from = dbm.get_latest_date_record(sql)
    date_from = datetime.strptime(date_from[0], '%Y%m')
    date_from = datetime.strftime(date_from, '%B %Y')
    del dbm
    
    dest_path = create_directory('%smeat_trade\\' % WEB_COMTRADE_PATH, today)
    
    for reporter in reporters:
        for commodity in commodities:
            dest_file = '%s%s%s.csv' % (dest_path, reporter, commodity)
            
            # fill in the fields in the page
            counter = 0
            while not resume_scrape(url, username, password, reporter, all_partners, commodity, date_from, dest_file):
                if counter >= 5:
                    raise Exception('web communication error, exceeds max number of attempts, stop scraping')
                else:
                    print 'scrape %s, %s at counter %s...' % (reporter, commodity, counter)
                    counter += 1
    
    print 'Finish scraping at %s...' % datetime.now()


if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)