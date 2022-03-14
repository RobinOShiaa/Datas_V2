'''
Created on 11 Nov 2016

@author: Suzanne
'''
import time
from datetime import datetime
from datas.function.function import chunck_list
from datas.web.path import WEB_CLAL_PATH
from datas.web.scraper import WebScraper, create_directory
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD, DBManager
from bs4 import BeautifulSoup
import sys
from datas.function.function import save_error_to_log

def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()
        
        url='http://www.clal.it/en/?section=smp_olanda'
        
        types=['food','feed']
        
                
        browser = WebScraper('Chrome')
        browser.open(url)
        browser.web_driver.maximize_window()
      
        html = browser.html_source()

        soup = BeautifulSoup(html, 'html.parser')
        #
        tables = soup.find_all('table',{'width':'98%'})
        for table in tables:
            data = []
            trs = table.findAll('tr')
            for tr in trs[4:]:
                date_td = tr.findAll('td')[0]
                data.append(date_td.text.replace('\n','').replace('\t','').encode('utf-8').replace('\xc2\xa0',''))
                #data.append(tr.text.lstrip().strip().replace('\n','').encode('utf-8').replace('\t','').replace('\xc2\xa0',''))
             
            chunked_list = chunck_list(data,2)
             
            today = datetime.now().strftime('%Y_%m_%d')
            dir_path = create_directory('%sdutch_smp_price_weekly' % WEB_CLAL_PATH, today)
     
            with open(dir_path+types[tables.index(table)]+'_euro_per_ton.csv', 'wb') as out_file:
                out_file.write('url,%s\n' % (url))
                for d in chunked_list:
                    # NB (Sue): multiply values by 1000 to account for CLAL's way of displaying values
                    out_file.write(d[0]+','+str(float(d[1])*1000)+'\n')
            
        browser.close()
        print 'Finish scraping at %s.' % datetime.now()
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['clal_dairy_price.py'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('monthly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['clal_dairy_price.py'],[success_msg]]
        save_error_to_log('monthly', msg_list)

if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)

    