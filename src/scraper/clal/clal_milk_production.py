'''
@author: conor

Scrapes milk production data for New Zealand, Argentina and China
NB: urls grouped by html page structure

'''

from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import chunck_list, create_directory
from datas.web.path import WEB_CLAL_PATH
from datas.web.scraper import WebScraper
from datetime import datetime
import time
import sys
import os
from datas.function.function import save_error_to_log
from datas.function.function import save_error_to_log

def write(file_path,country,unit,url,periods,chunked_data):
    with open('%s%s_%s.csv' % (file_path,country,unit),'w') as out_file:
        out_file.write('url,%s\n' % (url))
        out_file.write(','.join(periods))
        out_file.write('\n')
        for d in chunked_data:
                out_file.write(','.join(d))
                out_file.write('\n')

def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()
        
        dir_title = datetime.now().strftime('%Y_%m_%d')
        file_path = create_directory('%smilk_production' % WEB_CLAL_PATH, dir_title)

        urls = ["http://www.clal.it/en/index.php?section=consegne_new_zealand", "http://www.clal.it/en/index.php?section=consegne_argentina",
                "http://www.clal.it/en/index.php?section=produzioni_russia","http://www.clal.it/en/index.php?section=consegne_ucraina"]
        for url in urls:
            browser = WebScraper('Chrome')
            browser.open(url)
            browser.web_driver.maximize_window()
            time.sleep(3)
              
            periods = []
            data = []

            country = url.split('_')[-1].replace('_', ' ')+'_'
            if country=='zealand_':
                country='new zealand_'
            unit = browser.find_element('xpath', '//*[@id="pagina"]/table/tbody//td//table/tbody/tr[1]/td/font').text.replace('"','')
#             if country=='ucraina_':
#                 unit = browser.find_element('xpath', '//*[@id="pagina"]/table/tbody/tr[8]/td//table/tbody/tr[1]/td/font').text.replace('"','')
#             else:
#                 unit = browser.find_element('xpath', ".//*[@id='pagina']/table/tbody/tr[7]/td//table/tbody/tr[1]/td/font").text.replace('"',"").replace(' ','_')

            # extract years
            headers = browser.find_elements('class', 'intestazione')[2:]
            for header in headers:
                if '%' in header.text:
                    break
                periods.append(header.text)
            periods.insert(0, 'Month')
     
            # extract data in table
            for row_num in xrange(3,15):
                for col_num in xrange(1,len(periods)+1):

                    col_element = browser.find_element('xpath', './/*[@id="pagina"]/table//tr[7]//table//tr[%s]/td[%s]'% (str(row_num), str(col_num))) 
                    data_value = str(col_element.text if col_element.text else 'NA').replace(".","").replace(",",".").strip()
                    #print data_value

                    if country=='ucraina_':
                        col_element = browser.find_element('xpath', './/*[@id="pagina"]/table//tr[8]//table//tr[%s]/td[%s]'% (str(row_num), str(col_num)))
                    else:
                        col_element = browser.find_element('xpath', './/*[@id="pagina"]/table//tr[7]//table//tr[%s]/td[%s]'% (str(row_num), str(col_num)))
                    data_value = str(col_element.text if col_element.text else 'NA').replace(".","").replace(",",".").strip()

                    data.append(data_value)
             
            browser.close()
             
            chunked_data = chunck_list(data,len(periods))
             
            dir_title = datetime.now().strftime('%Y_%m_%d')
            file_path = create_directory('%smilk_production' % WEB_CLAL_PATH, dir_title)
                 
            with open('%s%s_%s.csv' % (file_path,country,unit),'w') as out_file:
                out_file.write('url,%s\n' % (url))
                out_file.write(','.join(periods))
                out_file.write('\n')
                for d in chunked_data:
                        out_file.write(','.join(d))
                        out_file.write('\n')
             
        urls_lst = ["http://www.clal.it/en/index.php?section=produzioni_russia","http://www.clal.it/en/index.php?section=consegne_ucraina"]
             
        for url in urls_lst:
            browser = WebScraper('Chrome')
            browser.open(url)
            time.sleep(3)
                 
            periods = []
            data = []
                 
            if url == "http://www.clal.it/en/index.php?section=produzioni_russia":
                country = url.split('produzioni_')[-1].replace('_', ' ')+'_'
            elif url == "http://www.clal.it/en/index.php?section=consegne_ucraina":
                country = url.split('consegne_')[-1].replace('_', ' ')+'_'
                             
            if url == "http://www.clal.it/en/index.php?section=produzioni_russia":
                unit = browser.find_element('xpath', ".//*[@id='pagina']/table/tbody/tr[7]/td/div/table/tbody/tr[1]/td/font").text.replace('"',"").replace(' ','_')
            elif url == "http://www.clal.it/en/index.php?section=consegne_ucraina":
                unit = browser.find_element('xpath', ".//*[@id='pagina']/table/tbody/tr[8]/td/div/table/tbody/tr[1]/td/font").text.replace("'","").replace(' ','_')
                                        
            headers = browser.find_elements('class', 'intestazione')[2:]
                                         
            for header in headers:
                if '%' in header.text:
                    break
                periods.append(header.text)
                periods.insert(0, 'Month')
                             
                             
            for row_num in xrange(3,15):
                for col_num in xrange(1,len(periods)+1):
                    if url == "http://www.clal.it/en/index.php?section=produzioni_russia":
                        col_element = browser.find_element('xpath', './/*[@id="pagina"]/table//tr[7]//table//tr[%s]/td[%s]'% (str(row_num), str(col_num)))
                    elif url == "http://www.clal.it/en/index.php?section=consegne_ucraina":
                        col_element = browser.find_element('xpath', './/*[@id="pagina"]/table//tr[8]//table//tr[%s]/td[%s]'% (str(row_num), str(col_num))) 
                    data_value = str(col_element.text if col_element.text else 'NA').replace(".","").replace(",",".").strip()
                    data.append(data_value)
                             
            chunked_data = chunck_list(data,len(periods))
                             
            dir_title = datetime.now().strftime('%Y_%m_%d')
            file_path = create_directory('%smilk_production' % WEB_CLAL_PATH, dir_title)
                                     
                             
            with open('%s%s_%s.csv' % (file_path,country,unit),'w') as out_file:
                out_file.write('url,%s\n' % (url))
                out_file.write(','.join(periods))
                out_file.write('\n')
                for d in chunked_data:
                        out_file.write(','.join(d))
                        out_file.write('\n')
                             
            browser.close()

        write(file_path,country,unit,url,periods,chunked_data)
        browser.close()

        '''Different scraper for China'''
        url = "http://www.clal.it/en/index.php?section=latte_alimentare_cina"
            
        browser = WebScraper('Chrome')
        browser.open(url)
        
        periods = []
        months = []
        data = []

        country='china_'
        unit = 'liquid milk production('

        
        # extract unit
        unit_elements = browser.find_elements('xpath', '//*[@id="pagina"]/table/tbody/tr/td/table/tbody/tr[4]/td[1]/table/tbody/tr/td/table[1]/tbody/tr/td[@align="center"]/small')
        for unit_element in unit_elements:
            unit = unit + unit_element.text
        
        # extract years
        headers = browser.find_elements('class', 'intestazione')[3:]
        for header in headers:
            if 'vs' in header.text:
                break
            periods.append(header.text)
    
        periods.insert(0, 'Month')
    
        for j in range(2,14):
            for i in range(1,10):
                col_elements = browser.find_elements('xpath', '//*[@id="table-scroll"]/table/tbody/tr[%s]/td[%s]' %(str(j), str(i)))
                for col in col_elements:
                    data_value = str(col.text if col.text else 'NA').strip()
                    data.append(data_value)
    
        month_elements = browser.find_elements('xpath', './/*[@id="pagina"]/table//tr[4]//table[2]//tr/td[contains(@class, "data")]')
        for month_element in month_elements:
            if '%' not in month_element.text:
                months.append(month_element.text)
        
        browser.close()

        #print data    
        chunked_data = chunck_list(data,len(periods)-1)
    
        #print chunked_data
        i=0 # combine month and data lists and avoid output problems with join_list function
        while i < len(months):
            print months[i]
            print chunked_data[i]
            chunked_data[i].insert(0, months[i])
            i+=1
     
        #print chunked_data
        
        dir_title = datetime.now().strftime('%Y_%m_%d')
        file_path = create_directory('%smilk_production' % WEB_CLAL_PATH, dir_title)
                   
        with open('%s%s.csv' % (file_path, unit),'w') as out_file:
            out_file.write('url,%s\n' % (url))
            out_file.write(','.join(periods))
            out_file.write('\n')
            for d in chunked_data:
                out_file.write(','.join(d))
                out_file.write('\n')

   
        chunked_data = chunck_list(data,len(periods)-1)

        i=0 # combine month and data lists and avoid output problems with join_list function
        while i < len(months):
            chunked_data[i].insert(0, months[i])
            i+=1
                   
        write(file_path,country,unit,url,periods,chunked_data)
            
        print 'Finish scraping at %s.' % datetime.now()
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['clal_milk_production'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('monthly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['clal_milk_production'],[success_msg]]
        save_error_to_log('monthly', msg_list) 


if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
    
