'''
Created on 11 Nov 2014

@author: Suzanne

TODO 27/01/2015(Wenchong): url changed so the elements changed. Need to adjust it.
Data haven't been updated since 2013, need to automate?
'''

import re
from datetime import datetime
from datas.web.scraper import WebScraper
import sys
import os
from datas.function.function import save_error_to_log
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import chunck_list
from datas.function.function import create_directory
from datas.web.path import WEB_BPEX_PATH


def scrape(db_params):

    try:
        print 'Start scraping at %s...' % datetime.now()
        
        """13/01/2015(Wenchong): Please keep this naming for the convenience of name recognition"""
        today = datetime.now().strftime('%Y_%m_%d')
        
        # url changed
        #url = 'http://www.bpex.org.uk/prices-facts-figures/consumption/Eupercapitapigmeatconsumption2.aspx'
        url = 'http://www.bpex.org.uk/prices-stats/consumption/eu-per-capita-consumption/'
        scraper = WebScraper('Chrome')
        scraper.open(url)

        regex = '<td>(\w[\s\w]*)</td>|<td align="right">(\d+\.\d)</td>'
        yregex = '<td align="right"><strong>(\d{4})'#</strong></td>' #year
        
         
        pattern = re.compile(str.encode(regex))
        ypattern = re.compile(str.encode(yregex))
         
         
        '''Start scraping'''
        scraper.open(url)
         
        # TODO(Wenchong): 27/01/2015 elements changed
        #resultsstr = browser.find_element_by_xpath('//*[@id="rightcol"]/table').get_attribute('innerHTML')
        resultsstr = scraper.find_element('xpath','//*[@id="innerRight"]//table').get_attribute('innerHTML')
         
        htmltext = unicode.encode(resultsstr)
        headers = ypattern.findall(htmltext)
        #print headers
        titles = pattern.findall(htmltext)    #NB - results in tuple
        #print titles
        data = [x for t in titles for x in t] #convert to list
        data = filter(None, data)
        data = chunck_list(data, len(headers)+1)
         
        scraper.close()
            
        dir_path = create_directory(WEB_BPEX_PATH+'consumption', today)
        
        """13/01/2015(Wenchong): Please keep this naming for the convenience of name recognition"""
        file_path = dir_path+'eu_per_capita_consumption_kg per head.csv'
         
        with open(file_path, 'w') as out_file:
            out_file.write('url,%s' % (url))
            out_file.write('\n')
            out_file.write('Year,')
            out_file.write(','.join(headers))
            out_file.write('\n')
                       
            for d in data:
                out_file.write(','.join(d))
                out_file.write('\n')
        
        print 'Finished scraping at %s.' % datetime.now()
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['bpex.consumption.py'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('monthly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['bpex.consumption.py'],[success_msg]]
        save_error_to_log('monthly', msg_list)

if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
    