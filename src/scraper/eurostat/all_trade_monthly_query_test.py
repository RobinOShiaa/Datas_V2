'''
Created on 20 Jan 2017

@author: Suzanne
'''
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datas.db.manager import DBManager, RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.web.scraper import WebScraper
import sys
from datas.function.function import save_error_to_log

#date_from = 
date_to = datetime.now()

urls=['http://epp.eurostat.ec.europa.eu/newxtweb/getquery.do?queryID=100771354&queryName=/dairy_imports_normal&datasetID=DS-057380&keepsessionkey=true',
      'http://epp.eurostat.ec.europa.eu/newxtweb/getquery.do?queryID=100771355&queryName=/dairy_imports_inward&datasetID=DS-057380&keepsessionkey=true',
      'http://epp.eurostat.ec.europa.eu/newxtweb/getquery.do?queryID=100771356&queryName=/dairy_imports_other&datasetID=DS-057380&keepsessionkey=true',
      'http://epp.eurostat.ec.europa.eu/newxtweb/getquery.do?queryID=100771372&queryName=/dairy_exports_normal&datasetID=DS-057380&keepsessionkey=true',
      'http://epp.eurostat.ec.europa.eu/newxtweb/getquery.do?queryID=100771373&queryName=/dairy_exports_inward&datasetID=DS-057380&keepsessionkey=true',
      'http://epp.eurostat.ec.europa.eu/newxtweb/getquery.do?queryID=100771374&queryName=/dairy_exports_other&datasetID=DS-057380&keepsessionkey=true']

for url in urls[1:]:
    query = url.split('/')[-1].split('&')[0]
    date_from = datetime.strptime('201001', '%Y%m')
    #date_from = date_from - relativedelta(months=6)
        
    while date_from <= date_to:
        
        yearmonth = datetime.strftime(date_from, '%Y%m')
        print query, yearmonth
        wscraper = WebScraper('Chrome')
        wscraper.open(url)
        
        
        wscraper.click_button('xpath', '//*[@id="content"]/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr/td[4]/div/a')
        
        
        wscraper.click_button('xpath', ".//*[@id='CONTENT_DS-057380PERIOD']/a") # time period
        time.sleep(3)
     
        #remove_xpath = ".//*[@id='removeAll']"
     
        wscraper.switch_browser_window(1)
        frame_elements = wscraper.find_elements('tag', 'frame')
        wscraper.switch_frame(frame_elements[0])
        wscraper.web_driver.maximize_window()
        #print wscraper.html_source()
        #wscraper.switch_frame()
     
        wscraper.hover('xpath',".//*[@id='content']/form[9]/table/tbody/tr[4]/td/table/tbody/tr[3]/td[2]/table/tbody/tr[4]/td/img")
        wscraper.click_button('xpath',".//*[@id='content']/form[9]/table/tbody/tr[4]/td/table/tbody/tr[3]/td[2]/table/tbody/tr[4]/td/img") # remove all
        
        #print query, yearmonth
        try:
            time_tag = wscraper.find_element('xpath', '//*[contains(text(),"%s")]' % yearmonth)
        except:
            wscraper.close()
            break
        if time_tag:
            time_tag.click()
        else:
            wscraper.close()
            break

        time.sleep(2)
        wscraper.click_button('xpath',".//*[@id='DS-057380PERIOD']")
        #try:
        wscraper.hover('xpath','.//*[@id="content"]/form[9]/table/tbody/tr[4]/td/table/tbody/tr[3]/td[2]/table/tbody/tr[1]/td/img[@id="toRight"]')
        time.sleep(4)
        wscraper.click_button('xpath','.//*[@id="content"]/form[9]/table/tbody/tr[4]/td/table/tbody/tr[3]/td[2]/table/tbody/tr[1]/td/img[@id="toRight"]')
        time.sleep(2)
 
        wscraper.hover('xpath',".//*[@id='Select']")
        wscraper.click_button('xpath',".//*[@id='Select']")
     
        wscraper.switch_browser_window(0)
     
        wscraper.click_button('xpath', ".//*[@id='finish']")
        time.sleep(4)
     
        wscraper.select_eurostat_output_options()

        wscraper.load_field('input','name','extractionname', query + yearmonth)
     
        wscraper.click_button('xpath', ".//*[@id='Finish']")
        time.sleep(3)
         
        wscraper.close()
        
        #increment date_yearmonth
        date_from = date_from + relativedelta(months=1)