'''
Created on 27 Jul 2016

@author: Suzanne
'''
from datetime import datetime
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import create_directory
from datas.web.scraper import WebScraper
from datas.web.path import WEB_GLOBALDAIRYTRADE_PATH
import sys
from datas.function.function import save_error_to_log

def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()
        
        products = []
        prices = []
        
        url = 'https://www.globaldairytrade.info/en/product-results/'
        today = datetime.strftime(datetime.now(), '%Y_%m_%d')
        
        scraper = WebScraper('Chrome')
        scraper.open(url)

        elements = scraper.find_elements('tag', 'h4')[3:]

        for element in elements:
            if element.text != '':
                products.append(element.text)
        
        elements = scraper.find_elements('class', 'productValue')
        for element in elements:
            prices.append(element.text.replace('$','').replace(',',''))
        
        dir_path = create_directory(WEB_GLOBALDAIRYTRADE_PATH, today)

        
        with open(dir_path+'gdt_recent.csv', 'wb') as outfile:
            outfile.write('product,dollars\n')
            for i in range(0,len(products)):
                outfile.write(products[i]+','+prices[i]+'\n')
        scraper.close()

    
        print 'Finish scraping at %s.' % datetime.now()
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['global_dairy_trade_price.py'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('weekly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['global_dairy_trade_price.py'],[success_msg]]
        save_error_to_log('weekly', msg_list)


if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
    

