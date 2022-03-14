'''
Created on 31 Aug 2015

@author: Suzanne
'''

import time
from datetime import datetime
from datas.web.path import WEB_EUROSTAT_PATH
from datas.db.manager import DBManager, RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.web.scraper import WebScraper
#from bs4 import BeautifulSoup

def scrape(db_params):
    print 'Start scraping at %s...' % datetime.now()
    
    '''Create dairy query'''
    
    dbm = DBManager(db_params[0], db_params[1], db_params[2], db_params[3])
    sql = ('select max(yearmonth) as max_date from eurostat_dairy_trade '
           'group by type order by max_date asc limit 1;')
    date_from = dbm.get_latest_date_record(sql)
 
    try:
        date_from = date_from[0]
    except:
        date_from = '199801'
 
    del dbm
    
    date_from = datetime.strptime(date_from, '%Y%m')
    date_to = datetime.now()
    #testing purposes only
#     date_to = '201306'
#     date_to = datetime.strptime(date_to, '%Y%m')
#     date_from = '201301'
#     date_from = datetime.strptime(date_from, '%Y%m')

    wscraper = WebScraper('Chrome')
    url = "http://epp.eurostat.ec.europa.eu/newxtweb/"
    wscraper.open(url)
    
    email = "cosullivan@computing.dcu.ie"
    password = "DATASdcu1234#"
    
    wscraper.login_eurostat_query(email, password)

    wscraper.click_button('xpath', ".//*[@id='treeViewImage0*0']") # available

    wscraper.click_button('xpath', ".//*[@id='treeViewImage0*0*0']") # international

    #wscraper.click_button('xpath', ".//*[@id='treeView0*0*0']/table/tbody/tr[2]/td[2]/table/tbody/tr/td[2]/a") # hs
    wscraper.click_button('xpath', ".//*[@id='treeView0*0*0']/table/tbody/tr[6]/td[2]/table/tbody/tr/td[2]/a") # hs

    existing_query = ".//*[@id='menuItemHilite4']"
    wscraper.wait(10, 'xpath', existing_query)

    i = 0
    while i < 3:
        try:
            wscraper.hover('xpath', existing_query)
            wscraper.click_button('xpath',existing_query)
        except:
            i += 1
            
        else:
            time.sleep(3)
            break

    wscraper.click_button('xpath', ".//*[@id='content']/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr/td[8]/div/a") # existing
    time.sleep(3)
    
    wscraper.click_button('xpath',".//*[@id='treeList']/tbody/tr[5]/td[2]/img[contains (@id,'open')]") # modify query
    time.sleep(3)

    wscraper.click_button('xpath', ".//*[@id='CONTENT_DS-057380PERIOD']/a") # time period
    time.sleep(3)

    #remove_xpath = ".//*[@id='removeAll']"

    wscraper.switch_browser_window(1)
    frame_elements = wscraper.find_elements('tag', 'frame')
    wscraper.switch_frame(frame_elements[0])
    #print wscraper.html_source()
    #wscraper.switch_frame()

    wscraper.hover('xpath',".//*[@id='content']/form[9]/table/tbody/tr[4]/td/table/tbody/tr[3]/td[2]/table/tbody/tr[4]/td/img")
    wscraper.click_button('xpath',".//*[@id='content']/form[9]/table/tbody/tr[4]/td/table/tbody/tr[3]/td[2]/table/tbody/tr[4]/td/img")
        
    date_elements = wscraper.find_elements('xpath',".//*[@id='availableElements']/option")
    
    #year_month_str = "C1_" + year_month
    
    ele_value_lst = []
    for ele_num in xrange(0,len(date_elements)):
        ele_value = date_elements[ele_num].get_attribute('value').split('_')[1]
        ele_value = datetime.strptime(ele_value, '%Y%m')
        if ele_value >= date_from and ele_value <= date_to:
            ele_value_lst.append(date_elements[ele_num])
            #cur_year_month = date_elements[ele_num]
            #ele_value_lst = [ele_num -2,ele_num - 1,ele_num,ele_num + 1,ele_num + 2,ele_num + 3]
            
    for click_ele_num in ele_value_lst:
        #date_elements[click_ele_num].click()
        click_ele_num.click()
        time.sleep(1)
        wscraper.click_button('xpath',".//*[@id='DS-057380PERIOD']")
        #try:
        wscraper.hover('xpath',".//*[@id='content']/form[9]/table/tbody/tr[4]/td/table/tbody/tr[3]/td[2]/table/tbody/tr[1]/td/img")
        time.sleep(4)
        wscraper.click_button('xpath',".//*[@id='content']/form[9]/table/tbody/tr[4]/td/table/tbody/tr[3]/td[2]/table/tbody/tr[1]/td/img")
#         except:
#             pass
        time.sleep(2)
    
    wscraper.hover('xpath',".//*[@id='Select']")
    wscraper.click_button('xpath',".//*[@id='Select']")

    wscraper.switch_browser_window(0)

    wscraper.click_button('xpath', ".//*[@id='finish']")
    time.sleep(4)

    wscraper.select_eurostat_output_options()
    
    extraction_name = 'dairy_trade'
    wscraper.load_field('input','name','extractionname',extraction_name)

    wscraper.click_button('xpath', ".//*[@id='Finish']")
    time.sleep(3)
    
    wscraper.close()
    
    '''Create pig query'''
    
    dbm = DBManager(db_params[0], db_params[1], db_params[2], db_params[3])
    sql = ('select max(yearmonth) as max_date from eurostat_dairy_trade '
           'group by type order by max_date asc limit 1;')
    date_from = dbm.get_latest_date_record(sql)
 
    try:
        date_from = date_from[0]
    except:
        date_from = '199801'
        date_from = datetime.strptime(date_from, '%Y%m')
     
    del dbm
     
    date_to = datetime.now()
    #testing purposes only
#     date_to = '201504'
#     date_to = datetime.strptime(date_to, '%Y%m')
#     date_from = '201501'
#     date_from = datetime.strptime(date_from, '%Y%m')
    
    wscraper = WebScraper('Chrome')
    wscraper.open(url)
    
    wscraper.login_eurostat_query(email, password)

    wscraper.click_button('xpath', ".//*[@id='treeViewImage0*0']") # available

    wscraper.click_button('xpath', ".//*[@id='treeViewImage0*0*0']") # international
    
    wscraper.click_button('xpath', ".//*[@id='treeView0*0*0']/table/tbody/tr[6]/td[2]/table/tbody/tr/td[2]/a") # hs
    
    wscraper.wait(10,'xpath',".//*[@id='menuItemHilite4']")

    i = 0
    while i < 3:
        try:
            wscraper.hover('xpath', existing_query) # previously declared during earlier scrape
            wscraper.click_button('xpath',existing_query)
        except:
            i += 1
            
        else:
            break
    
    wscraper.wait(5, 'xpath', ".//*[@id='content']/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr/td[8]/div/a")

    wscraper.click_button('xpath', ".//*[@id='content']/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr/td[8]/div/a") # existing
    
    wscraper.wait(10,'xpath',".//*[@id='treeList']/tbody/tr[4]/td[2]/img[contains (@id,'open')]")
    
    wscraper.click_button('xpath', ".//*[@id='treeList']/tbody/tr[4]/td[2]/img[contains (@id,'open')]") # modify query

    wscraper.wait(10,'xpath',".//*[@id='CONTENT_DS-057380PERIOD']/a")
    wscraper.click_button('xpath', ".//*[@id='CONTENT_DS-057380PERIOD']/a")
    time.sleep(3)

    wscraper.switch_browser_window(1)
    frame_elements = wscraper.find_elements('tag', 'frame')
    wscraper.switch_frame(frame_elements[0])
    #print wscraper.html_source()
    #wscraper.switch_frame()

    wscraper.hover('xpath', ".//*[@id='content']/form[9]/table/tbody/tr[4]/td/table/tbody/tr[3]/td[2]/table/tbody/tr[4]/td/img")
    wscraper.click_button('xpath',".//*[@id='content']/form[9]/table/tbody/tr[4]/td/table/tbody/tr[3]/td[2]/table/tbody/tr[4]/td/img")
    #year_month = datetime.date.today().strftime("%Y%m")
    
    date_elements = wscraper.find_elements('xpath',".//*[@id='availableElements']/option")
    
    #year_month_str = "C1_" + year_month
    
    ele_value_lst = []
    for ele_num in xrange(0,len(date_elements)):
        ele_value = date_elements[ele_num].get_attribute('value').split('_')[1]
        ele_value = datetime.strptime(ele_value, '%Y%m')
        if ele_value >= date_from and ele_value <= date_to:
            ele_value_lst.append(date_elements[ele_num])
            
    for click_ele_num in ele_value_lst:
        click_ele_num.click()
        time.sleep(1)
        wscraper.click_button('xpath',".//*[@id='DS-057380PERIOD']")
        wscraper.hover('xpath',".//*[@id='content']/form[9]/table/tbody/tr[4]/td/table/tbody/tr[3]/td[2]/table/tbody/tr[1]/td/img")
        time.sleep(3)
        wscraper.click_button('xpath',".//*[@id='content']/form[9]/table/tbody/tr[4]/td/table/tbody/tr[3]/td[2]/table/tbody/tr[1]/td/img")
        time.sleep(2)
    
    wscraper.hover('xpath',".//*[@id='Select']")
    wscraper.click_button('xpath',".//*[@id='Select']")
    
    #wscraper.close()
    wscraper.switch_browser_window(0)

    wscraper.click_button('xpath', ".//*[@id='finish']")
    
    wscraper.select_eurostat_output_options()
    
    extraction_name = 'pig_trade'
    wscraper.load_field('input','name','extractionname',extraction_name)

    wscraper.click_button('xpath', ".//*[@id='Finish']")
    time.sleep(3)
    wscraper.close()
    
    print 'finished scraping at %s...' % datetime.now()
   
if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)