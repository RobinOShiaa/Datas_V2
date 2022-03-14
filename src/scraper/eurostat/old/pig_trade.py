'''
Created on 17 Apr 2015

@author: Conor 
'''
import time

import datetime
from datas.web.path import WEB_EUROSTAT_PATH
from datas.db.manager import DBManager
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.web.scraper import WebScraper
from bs4 import BeautifulSoup

def scrape(db_params):
    
    wscraper = WebScraper('Chrome')
    
    url = "http://epp.eurostat.ec.europa.eu/newxtweb/"
    
    wscraper.open(url)
    
    login_xpath = ".//*[@id='content']/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr/td[4]/div/a"
    
    wscraper.click_button('xpath', login_xpath)
    
    external_xpath = ".//*[@id='responsive-main-nav']/div[6]/a[2]"
    
    wscraper.click_button('xpath',external_xpath)
    
    email = "cosullivan@computing.dcu.ie"
    password = "DATASdcu1234#"
    
    wscraper.load_field('input', 'name', 'username', email)
    wscraper.load_field('input','name','password',password)
    
    submit_xpath = ".//*[@id='loginForm']/input[11]"
    
    wscraper.click_button('xpath',submit_xpath)
    
    time.sleep(3)
    
    available_xpath = ".//*[@id='treeViewImage0*0']"
    wscraper.click_button('xpath',available_xpath)
    
    international_xpath = ".//*[@id='treeViewImage0*0*0']"
    
    wscraper.click_button('xpath',international_xpath)
    
    hs_xpath = ".//*[@id='treeView0*0*0']/table/tbody/tr[2]/td[2]/table/tbody/tr/td[2]/a"
    wscraper.click_button('xpath',hs_xpath)
    time.sleep(5)
    existing_xpath = ".//*[@id='menuItemHilite4']"
    
    wscraper.hover('xpath',existing_xpath)
    wscraper.click_button('xpath',existing_xpath)
    
    existing_two_xpath = ".//*[@id='content']/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr/td[8]/div/a"
    
    wscraper.click_button('xpath',existing_two_xpath)
    
    time.sleep(3)
    modify_query_xpath = wscraper.find_element('xpath', ".//*[@id='treeList']/tbody/tr[4]/td[2]/img[contains (@id,'open')]")
    modify_query_xpath.click()
    
    time.sleep(3)
    
    
    period_xpath = ".//*[@id='CONTENT_DS-057380PERIOD']/a"
    wscraper.click_button('xpath', period_xpath)
    
    
    remove_xpath = ".//*[@id='removeAll']"
    
    time.sleep(4)
    
    
    
    wscraper.switch_browser_window(1)
    
    frame_elements = wscraper.find_elements('tag', 'frame')
    wscraper.switch_frame(frame_elements[0])
    #print wscraper.html_source()
    #wscraper.switch_frame()
    
    
    
    wscraper.hover(".//*[@id='content']/form[9]/table/tbody/tr[4]/td/table/tbody/tr[3]/td[2]/table/tbody/tr[4]/td/img")
    wscraper.click_button('xpath',".//*[@id='content']/form[9]/table/tbody/tr[4]/td/table/tbody/tr[3]/td[2]/table/tbody/tr[4]/td/img")
    year_month = datetime.date.today().strftime("%Y%m")
    
    date_elements = wscraper.find_elements('xpath',".//*[@id='availableElements']/option")
    
    year_month_str = "C1_" + year_month
    
    for ele_num in xrange(0,len(date_elements)):
        ele_value = date_elements[ele_num].get_attribute('value')
        if ele_value == year_month_str:
            cur_year_month = date_elements[ele_num]
            ele_value_lst = [ele_num -2,ele_num - 1,ele_num,ele_num + 1,ele_num + 2,ele_num + 3]
            
    for click_ele_num in ele_value_lst:
        date_elements[click_ele_num].click()
        time.sleep(1)
        wscraper.click_button('xpath',".//*[@id='DS-057380PERIOD']")
        wscraper.hover(".//*[@id='content']/form[9]/table/tbody/tr[4]/td/table/tbody/tr[3]/td[2]/table/tbody/tr[1]/td/img")
        time.sleep(3)
        wscraper.click_button('xpath',".//*[@id='content']/form[9]/table/tbody/tr[4]/td/table/tbody/tr[3]/td[2]/table/tbody/tr[1]/td/img")
        time.sleep(2)
    
    wscraper.hover(".//*[@id='Select']")
    wscraper.click_button('xpath',".//*[@id='Select']")
    
    #wscraper.close()
    wscraper.switch_browser_window(0)
    
    finish_xpath = ".//*[@id='finish']"
    wscraper.click_button('xpath',finish_xpath)
    
    
    output_xpath = ".//*[@id='setBatchOutputFormat']"
    
    wscraper.click_button('xpath',output_xpath)
    
    labels_xpath = ".//*[@id='batchOptions']/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr[2]/td[2]/input[3]"
    
    wscraper.click_button('xpath',labels_xpath)
    
    format_xpath = ".//*[@id='batchFormats']/option[1]"
    
    wscraper.click_button('xpath',format_xpath)
    
    extraction_name = 'pig_trade'
    wscraper.load_field('input','name','extractionname',extraction_name)
    
    finish_two_xpath = ".//*[@id='Finish']"
    
    wscraper.click_button('xpath',finish_two_xpath)
    time.sleep(3)
    wscraper.close()
    

if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
