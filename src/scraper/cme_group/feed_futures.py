'''
Created on 16 Dec 2015

@author: Suzanne
'''
import time
from datetime import datetime
from datas.function.function import create_directory, chunck_list, save_error_to_log
from datas.web.scraper import WebScraper
from datas.web.path import WEB_CME_PATH
import sys

def scrape():
    try:
        print 'Start scraping at %s...' % datetime.now()
        data = ['Month','Last','Change','Prior Settle','Open','High','Low','Volume','Hi / Low Limit','Updated']
        #data = []
        url = 'http://www.cmegroup.com/trading/agricultural/grain-and-oilseed/corn.html'
        
        scraper = WebScraper('Chrome')
        scraper.open(url)
        #scraper.web_driver.maximize_window()
        
        #table = scraper.find_element('id', 'quotesFuturesProductTable1')
        
        #time.sleep(7)
    #     headers = scraper.find_elements('xpath', '//table[@id="quotesFuturesProductTable1"]/thead/tr/th')
    #     for h in headers:
    #         print h.text
    #         if h.text not in ['Options','Charts']:
    #             data.append(h.text.replace('\n', ' '))
        
        
        data_tags = scraper.find_elements('xpath', '//table[@id="quotesFuturesProductTable1"]/tbody/tr/td')

        for d in data_tags:
            if d.text not in ['Show Price Chart','Options','Charts','']:
                data.append(d.text.replace(',','').replace('\n', ' '))
            
        data = filter(None, data)
        data = chunck_list(data, 10)
        
        dir_path = WEB_CME_PATH + 'feed/'
         
        today = datetime.strftime(datetime.now(), '%Y_%m_%d')
         
    #     with open ('%s%s.csv' % (dir_path, today), 'wb') as file:
    #         for w in data:
    #             file.write(','.join(w))
    #             file.write('\n')
               
        with open ('Y:\\SITES\\node\\public\\current_feed.csv', 'wb') as file:
            file.write('Product,'+','.join(data[0])+'\n')
            
            for w in data[1:3]:
                file.write('Corn futures quotes,' + ','.join(w) + '\n')

     
        scraper.close()
        print 'Finished scraping at %s...' % datetime.now()
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() load error:\n'
        msg_list = [['feed_futures.py'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('daily', msg_list)
    else:
        success_msg = 'auto_run() loaded successfully\n'
        msg_list = [['feed_futures.py'],[success_msg]]
        save_error_to_log('daily', msg_list)

if __name__ == '__main__':
    scrape()
