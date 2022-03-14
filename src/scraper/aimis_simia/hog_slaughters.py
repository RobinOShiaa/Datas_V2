'''
Created on 24 Apr 2015

@author: Suzanne
'''
from datas.web.scraper import WebScraper, create_directory
from datas.db.manager import DBManager, RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.web.path import WEB_AIMIS_SIMIA_PATH
from datetime import datetime
from datas.function.function import chunck_list
import time
import sys
#import os
from datas.function.function import save_error_to_log

def resume_scrape(url, date_from, k, date_k, date_v):
    headers = []
    data = []
    # use this to skip process when dropdown menu option is blank
    try:
        curr_date = datetime.strptime(date_v, '%Y-%m-%d')
    except:
        return True
    #print (curr_date >= date_from)
    if curr_date >= date_from:
        try:
            scraper = WebScraper('Chrome')
            scraper.open(url)
            scraper.load_field('select', 'id', 'p_71', k)
            scraper.click_button('name', 'btnNext')
            time.sleep(5)
            
            scraper.load_field('select', 'id', 'p_72', date_k)
            #print 'date_k', date_k
            scraper.load_field('select', 'id', 'report_format_type_code', '21') # download as xls
            scraper.click_button('name', 'btnNext')
            scraper.wait(30, 'name', 'btnDownload')
            scraper.click_button('name', 'btnDownload')
            time.sleep(5)
            
            domain_tags = scraper.find_elements('xpath', '//table[@class="xt"][1]//tr[1]/th[contains(@id, "hdr")]')[:3]

            date_tags = scraper.find_elements('xpath', '//table[@class="xt"][1]//tr[2]/th[not(contains(text(), "%"))]')[:6]
          
            i=0
            while i < len(domain_tags):
                headers.append(str(domain_tags[i].text.replace(',','')+' - '+date_tags[i].text.replace(',','')))
                headers.append(str(domain_tags[i].text.replace(',','')+' - '+date_tags[i+1].text.replace(',','')))
                i=i+1
                        
            headers.insert(0, ' ')
            #print headers
#             //*[@id="wb-main-in"]/div[2]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[7]/td[7]
#             //*[@id="wb-main-in"]/div[2]/div/div[2]/div[2]/div/div/div[3]/table/tbody/tr[3]/td[1]
            data_tags = scraper.find_elements('xpath', '//*[@id="wb-main-in"]//div[1]/table[@class="xt"]//tr/*[not(contains(@style, "center"))]')
            
            for d in data_tags:
                if 'West' not in d.text and 'East' not in d.text and '%' not in d.text and d.text !=' ':
                    data.append(d.text.replace(',',''))
            
            data = chunck_list(data, len(headers))
            #print data
            f = date_v.replace('-','_')
        except:
            scraper.close()
            return False
        else:
            #print data
            #print 'writing %s.csv' % f
            today = datetime.strftime(datetime.now(), '%Y_%m_%d')
            dir_path = create_directory(WEB_AIMIS_SIMIA_PATH+'hog_slaughters\\', today)
            with open('%s%s.csv' % (dir_path, f), 'w') as out:
                out.write('url,%s\n' % url)
                out.write(','.join(headers))
                out.write('\n')
                for d in data:
                    out.write(','.join(d))
                    out.write('\n')
            scraper.close()
            return True
    else:
        return True

def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()
        
        # get the latest data date from DB
        dbm = DBManager(db_params[0], db_params[1], db_params[2], db_params[3])
        date_from = dbm.get_latest_date_record('select max(date) from aimis_simia_hog_slaughters;')
        
        try:
            date_from = datetime.strptime(str(date_from[0]), '%Y-%m-%d')
        except:
            date_from = '1998-01-01'
            date_from = datetime.strptime(date_from, '%Y-%m-%d')
    
        year_from = date_from.year
    
        del dbm
        
        url = 'http://aimis-simia.agr.gc.ca/rp/index-eng.cfm?menupos=1.02.06&LANG=EN&r=53&pdctc=&action=pR'
        scraper = WebScraper('Chrome')
        scraper.open(url)
        
        keys = scraper.get_dropdown_list('name', 'p_71', 'value')[1:]
        values = scraper.get_dropdown_list('name', 'p_71', 'text')[1:]
    
        year_options = dict(zip(keys, values))
        scraper.close()
        
        #print values
        
        for k, v in year_options.items():
            if v >= year_from :
                scraper = WebScraper('Chrome')
                scraper.open(url)
                scraper.load_field('select', 'id', 'p_71', k)
                scraper.click_button('name', 'btnNext')
                time.sleep(5)
                
                date_keys = scraper.get_dropdown_list('name', 'p_72', 'value')
                date_values = scraper.get_dropdown_list('name', 'p_72', 'text')
                
                dates = dict(zip(date_keys, date_values))
                #print weeks
                scraper.close()
                
                # check that week option in dropdown menu is later than latest date in database
                for date_k, date_v in dates.items():
                    counter = 0
                 
                    while not resume_scrape(url, date_from, k, date_k, date_v):
                        if counter >= 4:
                            return#raise Exception('web communication error, exceeds max number of attempts, stop scraping')
                        else:
                            #print 'Trying scrape %s at counter %s...' % (date_v, counter)
                            counter += 1
        print 'Finish scraping at %s.' % datetime.now() 
    except Exception as err:

        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['aimis_simia.hog_slaughters.py'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('weekly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['aimis_simia.hog_slaughters.py'],[success_msg]]
        save_error_to_log('weekly', msg_list)

if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)

