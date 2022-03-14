'''

Modifying pig333_price.py
Remove logging in and use of drop down menu
Scrape from table of Last Prices

'''

import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime
import sys
from datas.db.manager import DBManager
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import create_directory, save_error_to_log
from datas.web.path import WEB_PIG333_PATH
from datas.web.scraper import WebScraper

def get_data(elements):
    data_list = []
    for element in elements:
        data_list.append(element.text)
    return data_list    

def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()

        # get the latest data date from DB
        dbm = DBManager(db_params[0], db_params[1], db_params[2], db_params[3])
        sql = ('select max(date) as max_date from pig333_pig_price '
               'group by geo order by max_date asc limit 1;')
        date_from = dbm.get_latest_date_record(sql)
        date_from = date_from[0]
        del dbm

        dir_title = datetime.now().strftime('%Y_%m_%d')
        dir_path = '%spig_price\\' % WEB_PIG333_PATH

        links_url = 'https://www.pig333.com/markets_and_prices/'
		
        r = requests.get(url=links_url, verify=False)

        links_soup = BeautifulSoup(r.content, "html.parser")
        a_links = links_soup.find_all("a", {"class":"nom_mercat"})
        
        urls = []
        places = []
        
        for a_link in a_links:
            urls.append(a_link.get('href'))
            places.append(a_link.text.replace(' ','').replace('/','_').strip())
        
        place_num = 0
        
        for url in urls:
			browser = WebScraper('Chrome')
			browser.web_driver.maximize_window()
			browser.open(url)
			time.sleep(3)
			time.sleep(3)
			html = browser.web_driver.page_source
			soup = BeautifulSoup(html, 'html.parser')

			dates = []
			prices = []
			element = browser.find_element('xpath', '//*[@id="div_taula"]/div[1]/span/span[2]')
			currency_and_weight = element.text
			currency = currency_and_weight[:3]
			index = currency_and_weight.index('/')
			weight = currency_and_weight[index+1:]
			weight = weight.strip()
			priceheader = "Price({}/{})".format(currency, weight)
			headers = ["Date", priceheader] 
			
			data_table = soup.find_all("div", {"class":"reg_valor_mercat"})
			#It's a table made of div tags within div tags
			
			for data_row in data_table:
				data_cols = data_row.find_all("span", {"class":"data"})
				if len(data_cols) != 0:
					# get the latest data only
					date_to = data_cols[0].text.strip()
					data_prices = data_row.find_all("span", {"class":"preu"})
					if date_from < datetime.strptime(date_to, '%d-%b-%Y').date() and "-" not in data_prices[0].text.strip().replace(",",""):
						dates.append(date_to)
						prices.append(data_prices[0].text.strip().replace(",",""))
						
			browser.close()
			formatted_dates = []
			
			for date in dates:
				formatted_dates.append(str(datetime.strptime(date,"%d-%b-%Y"))[:10])
				
			newdir_path = create_directory(dir_path, dir_title)
			file_path = "%s%s_price_" % (newdir_path, places[place_num])
			file_path += currency + "_per_" + weight + ".csv" 
			
			out_file = open(file_path,'w')
			out_file.write('url, %s' % (url))
			out_file.write(',\n')
			
			out_file.write(','.join(headers))
			out_file.write(',\n')
			
			price_num = 0
			
			for formatted_date in formatted_dates:
				out_file.write(formatted_date)
				out_file.write(',')
				out_file.write(prices[price_num].split(' ')[0])
				out_file.write(',')
				out_file.write('\n')
				price_num += 1
				
			out_file.close()
			place_num += 1
    
        print 'Finish scraping at %s.' % datetime.now()
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['pig333_price'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('weekly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['pig333_price'],[success_msg]]
        save_error_to_log('weekly', msg_list)


if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
    
