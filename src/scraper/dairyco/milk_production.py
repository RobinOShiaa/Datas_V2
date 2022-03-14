'''
@author: Conor
'''
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import sys
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import chunck_list, create_directory, is_number, save_error_to_log
from datas.web.path import WEB_DAIRYCO_PATH

def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()
        #url = 'http://www.dairyco.org.uk/market-information/supply-production/milk-production/milk-deliveries-selected-countries/australia/#.VGR5BJCsW9_'
        url = 'http://dairy.ahdb.org.uk/market-information/supply-production/milk-production/milk-deliveries-selected-regions/australia/#.Vwy9hfkrKUl'    
        r = requests.get(url)
        
        soup = BeautifulSoup(r.content)
        
        table = soup.find("table")
        headers = []
        data = []
                
        tr_elements = table.findAll("tr")
    
        for tr_element in tr_elements[1:2]:
            td_elements = tr_element.findAll("td")
            headers.append(td_elements[4].text.strip().replace(',', ''))
            
        for tr_element in tr_elements[2:]:
            td_elements = tr_element.findAll("td")
            data.append(td_elements[0].text.strip()) #extract month names
            data.append(td_elements[4].text.strip().replace(',', '') if is_number(td_elements[4].text) else 'NA') #extract most recent data and check for blanks
       
        data = chunck_list(data,2)
       
        today = datetime.now().strftime('%Y_%m_%d')
        dir_path = WEB_DAIRYCO_PATH
        dir_title = create_directory(dir_path, today)
        
        file_path = "%sAUS_million_litres.csv" % dir_title
        out_file = open(file_path,'w')
        out_file.write('url,%s\n,' % (url))
        out_file.write(','.join(headers))
        out_file.write('\n')
        
        for d in data:
            out_file.write(','.join(d))
            out_file.write('\n')
        out_file.close() 
        print 'Finish scraping at %s.' % datetime.now()   
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['dairyco.milk_production'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('monthly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['dairyco.milk_production'],[success_msg]]
        save_error_to_log('monthly', msg_list)

if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
    