'''
Created on 18 May 2015

@author: Conor O'Sullivan
05/08/2015 (Sue): Combined dairy and pig query inputs.  Encapsulated login in new function.
'''
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datas.db.manager import DBManager, RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.web.scraper import WebScraper
import sys
from datas.function.function import save_error_to_log

def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()
        
        dbm = DBManager(db_params[0], db_params[1], db_params[2], db_params[3])
    #     sql = ('select max(yearmonth) as max_date from eurostat_dairy_trade_test '
    #            'group by type order by max_date asc limit 1;')

        url = "http://epp.eurostat.ec.europa.eu/newxtweb/"
        email = "smccarthy@computing.dcu.ie"
        password = "DATAS$123piggy"
        
        dbm = DBManager(db_params[0], db_params[1], db_params[2], db_params[3])
        sql = ('select max(yearmonth) as max_date from eurostat_dairy_trade;')
        sql_date_from = dbm.get_latest_date_record(sql)
        try:
            sql_date_from = sql_date_from[0]
        except:
            sql_date_from = '199801'
       
        del dbm
        
        date_to = datetime.now()
        queries = ['dairy_imports_normal','dairy_imports_inward','dairy_imports_other', 'dairy_exports_normal', 'dairy_exports_inward','dairy_exports_other','meat_imports', 'meat_exports','casein_trade']
        #queries = ['dairy_exports_other']
        for query in queries[1:]:
            print query
            
            date_from = datetime.strptime(sql_date_from, '%Y%m')
            date_from = date_from - relativedelta(months=6)
            while date_from <= date_to:
                
                yearmonth = datetime.strftime(date_from, '%Y%m')
                print yearmonth
                wscraper = WebScraper('Chrome')

                wscraper.open(url)
         
                #email = "cosullivan@computing.dcu.ie"
                #password = "DATASdcu1234#"

                #wscraper.login_eurostat_query(email, password)
                wscraper.click_button('xpath','//*[@id="content"]/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr/td[4]/div/a')
                time.sleep(3)
                wscraper.load_field('input','id','username',email)
                wscraper.click_button('xpath', '//*[@id="whoamiForm"]/input[2]')
                time.sleep(3)
                wscraper.load_field('input','id','password',password)
                wscraper.click_button('xpath', '//*[@id="loginForm"]/div/input')
                time.sleep(5)

                wscraper.click_button('xpath', ".//*[@id='treeViewImage0*0']") # available
                time.sleep(3)
                wscraper.click_button('xpath', ".//*[@id='treeViewImage0*0*0']") # international
                time.sleep(3)
                #wscraper.click_button('xpath', ".//*[@id='treeView0*0*0']/table/tbody/tr[2]/td[2]/table/tbody/tr/td[2]/a") # hs
                wscraper.click_button('xpath', ".//*[@id='treeView0*0*0']/table/tbody/tr[6]/td[2]/table/tbody/tr/td[2]/a") # hs
    
                wscraper.click_button('xpath', ".//*[@id='content']/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr/td[8]/div/a") # existing
                time.sleep(3)
                 
                #wscraper.click_button('xpath',".//*[@id='treeList']/tbody/tr[6]/td[2]/img[contains (@id,'open')]") # modify query
                 
                wscraper.click_button('xpath','//*[@id="treeList"]/tbody/tr[@data-tt-id="%s"]//img[@title = "Modify query"]' % query) #dairy imports
                time.sleep(3)
             
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
        
        #wscraper.close()
        print 'Finished scraping at %s.' % datetime.now()
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['eurostat.all_trade_monthly_query.py'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('monthly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['eurostat.all_trade_monthly_query.py'],[success_msg]]
        save_error_to_log('monthly', msg_list)
   
if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)

    
