'''
date created: 02/12/2014
author: Conor 
Scrapes milk price data for New Zealand, Argentina and China
'''
from datetime import datetime
from datas.function.function import chunck_list
from datas.web.path import WEB_CLAL_PATH
from datas.web.scraper import WebScraper, create_directory
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD#, DBManager
import sys
import time
from datas.function.function import save_error_to_log

def fill_nulls(mylist):
    for value in xrange(0,len(mylist)):
        if not mylist[value]:        
            mylist[value] = 'NA'
    return mylist        


def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()
        
        # get the latest data date from DB
        #dbm = DBManager(db_params[0], db_params[1], db_params[2], db_params[3])
        
        '''One scraper for New Zealand and Argentina'''
        url_list = ['http://www.clal.it/en/index.php?section=latte_new_zealand',
                    'http://www.clal.it/en/index.php?section=latte_argentina']
         
        country_names = ['newzealand','argentina']
        country_index = 0
        
         
        for url in url_list:
            browser = WebScraper('Chrome')
            browser.open(url)
            time.sleep(2)
            data = []
            headers = []
            months = []
            
            header_elements = browser.find_elements('class', 'intestazione')[3:]
            #print header_elements
            for header_element in header_elements:
                #print header_element.text
                if 'on' in header_element.text:
                    break
                header = header_element.text.split('\n')[0]
                if header not in headers:
                    headers.append(header)
            headers.insert(0, 'Month')
            #print headers
            
            month_elements = browser.find_elements('xpath', './/*[@id="pagina"]/table//td[contains(@class, "data")]')
         
            for month_element in month_elements:
                months.append(month_element.text)
            
            
            for row_num in xrange(2,14):
                for col_num in xrange(3,len(headers)*2,2):
                    value = browser.find_element('xpath','.//*[@id="pagina"]/table/tbody/tr[1]/td/table[1]/tbody/tr[4]/td/table/tbody/tr/td/table/tbody/tr/td/table[1]/tbody/tr/td/table[2]/tbody/tr[%s]/td[%s]' %(str(row_num), str(col_num)))
                    #value = browser.find_element_by_xpath(".//*[@id='pagina']//tbody/tr[" + str(row_num) +"]/td[contains(@class, \"Data\")][" + str(col_num) +"]")
                    data.append(str(value.text).replace(',','.').strip())
            
            
            browser.close()
            data = fill_nulls(data)
            #latest_year = browser.find_element_by_xpath('//*[@id="pagina"]/table/tbody/tr[1]/td/table[1]/tbody/tr[4]/td/table/tbody/tr/td/table/tbody/tr/td/table[1]/tbody/tr/td/table[2]/tbody/tr[1]/td[7]')
    
            #print headers
            chunked_data = chunck_list(data, len(headers)-1)
            i=0 # combine month and data lists and avoid output problems with join_list function
            while i < len(chunked_data):
                chunked_data[i].insert(0, months[i])
                i+=1
            #print chunked_data
            dir_title = datetime.now().strftime('%Y_%m_%d')
            file_path = create_directory('%sdairy_price' % WEB_CLAL_PATH, dir_title)
            
            with open(file_path + 'milk_%s_euro_per_100kg.csv' % (country_names[country_index]),'w') as out_file:
                out_file.write('url,%s\n' % (url))
                out_file.write(','.join(headers))
                out_file.write('\n')
                for d in chunked_data:
                    out_file.write(','.join(d))
                    out_file.write('\n')
            out_file.close()
            country_index += 1
            
        
        
        
        '''different scraper for China'''
        url = 'http://www.clal.it/en/index.php?section=latte_cina'
         
        browser = WebScraper('Chrome')
         
        browser.open(url)
         
        periods = []
        months = []
        data = []
        # extract years
        headers = browser.find_elements('xpath', './/table[@cellpadding="0"]//td[@colspan="2"]')
        for header in headers:
            if 'on' in header.text:
                break
            periods.append(header.text)
        periods.insert(0, 'Month')
        #print periods
        
        # extract data in table
        for row_num in xrange(3,15):
            for col_num in xrange(2,len(periods)*2-1,2):
                value = browser.find_element('xpath', './/*[@id="table-scroll"]/table/tbody/tr[%s]/td[%s]' %(str(row_num), str(col_num)))
                data.append(str(value.text).replace(',','.').strip())
        
        month_elements = browser.find_elements('xpath', './/*[@id="pagina"]/table//td[contains(@class, "data")]')
     
        for month_element in month_elements:
            months.append(month_element.text)
         
        browser.close()
        data = fill_nulls(data)
        chunked_list = chunck_list(data,len(periods)-1)
        
        i=0 # combine month and data lists and avoid output problems with join_list function
        while i < len(chunked_list):
            chunked_list[i].insert(0, months[i])
            i+=1
        #print chunked_list
        
        dir_title = datetime.now().strftime('%Y_%m_%d')
        file_path = create_directory('%sdairy_price' % WEB_CLAL_PATH, dir_title)
        
        with open('%smilk_china_euro_per_100kg.csv' % (file_path),'w') as out_file:
            out_file.write('url,%s\n' % (url))
            out_file.write(','.join(periods))
            out_file.write('\n')
            for cl in chunked_list:
                out_file.write(', '.join(cl))
                out_file.write('\n')
        
        out_file.close()
        print 'Finish scraping at %s.' % datetime.now()
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['clal_milk_price'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('monthly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['clal_milk_price'],[success_msg]]
        save_error_to_log('monthly', msg_list)
    
if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
    