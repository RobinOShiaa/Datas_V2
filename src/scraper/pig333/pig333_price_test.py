'''
Created on 20 Apr 2016

@author: Suzanne
'''
import requests
import time
from bs4 import BeautifulSoup
#import html5lib
from datetime import datetime
import sys
from datas.db.manager import DBManager
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import create_directory, save_error_to_log
from datas.web.path import WEB_PIG333_PATH
from datas.web.scraper import WebScraper


def login(browser, username_element, password_element, username, password,remember_me_id, button_id):
    #Uses tag IDs. NB - Must have already registered with site.
    browser.load_field('input', 'id', username_element, username)
    browser.load_field('input', 'id', password_element, password)
#     if remember_me_id is not None:
#         browser.click_button('id', remember_me_id) 
    browser.click_button('id', button_id)

def get_data(elements):
    data_list = []
    for element in elements:
        data_list.append(element.text)
    return data_list    

def scrape(db_params):
    #try:
        print 'Start scraping at %s...' % datetime.now()
        
        # get the latest data date from DB
        dbm = DBManager(db_params[0], db_params[1], db_params[2], db_params[3])
        sql = ('select max(date) as max_date from pig333_pig_price '
               'group by geo order by max_date asc limit 1;')
        date_from = dbm.get_latest_date_record(sql)
        date_from = date_from[0]
        del dbm
        #print date_from
        
        headers = ["Date","Price(Euro/100kg)"]
        
        dir_title = datetime.now().strftime('%Y_%m_%d')
        dir_path = '%spig_price\\' % WEB_PIG333_PATH
                
        links_url = 'http://www.pig333.com/markets_and_prices/'
        #requests.packages.urllib3.disable_warnings()
        r = requests.get(url=links_url, verify=False)
        
        links_soup = BeautifulSoup(r.content)
        a_links = links_soup.find_all("a", {"class":"nom_mercat"})
        
        urls = []
        places = []
        
        for a_link in a_links:
            urls.append(a_link.get('href'))
            places.append(a_link.text.replace(' ','').replace('/','_').strip())
        
        place_num = 0
        
        your_email = 'smccarthy@computing.dcu.ie'
        your_password = '123piggy'
        #your_email = 'cosullivan@computing.dcu.ie'
        #your_password = 'ilovepigs'
        
   
        #logged_in = False
        
        for url in urls:
            #Log in
            browser = WebScraper('Chrome')
            browser.web_driver.maximize_window()
            browser.open(url)
            time.sleep(5)
            #if logged_in == False:
                #button_click(browser, 'boto_area_usuarios')
                
            button = browser.find_element('xpath', '/div[2]/div[1]/div/span[@class="zona_accede"]/a')
            print button.text
            return

            browser.click_button('xpath', '//*[@id="div_barra_usuari"]/div[1]/div/button[2]')
            time.sleep(6)
            login(browser, 'input_email', 'input_pass', your_email, your_password, 'inp_rec_barra_login', 'boto_login_div_registre')
            #logged_in = True
                
            time.sleep(10)
            
            browser.scroll_vertical(0)
            browser.hover('xpath', ".//*[@id='div_wrap_moneda']")
            browser.click_button('xpath', ".//*[@id='div_menu_monedes']/li[4]")
            time.sleep(3)
    #         unit_select = browser.find_element_by_xpath(".//*[@id='select_unitats']")
    #         unit_select.click()
    
            browser.load_field('select', 'id', 'select_unitats', '100kg')
            time.sleep(3)
        
            html = browser.web_driver.page_source
            soup = BeautifulSoup(html)#, 'html5')
            
            dates = []
            prices = []
            
            data_table = soup.find_all("table")[1]
            data_rows = data_table.find_all("tr")
            for data_row in data_rows:
                data_cols = data_row.find_all("td")
                if len(data_cols) != 0:
                    # get the latest data only
                    date_to = data_cols[0].text.strip()
                    if  date_from < datetime.strptime(date_to, '%b %d, %Y').date():
                        dates.append(date_to)
                        prices.append(data_cols[1].text.strip())
            
            browser.close()
            formatted_dates = []
            
            for date in dates:        
                formatted_dates.append(str(datetime.strptime(date,"%b %d, %Y"))[:10])
    
            newdir_path = create_directory(dir_path, dir_title)
            file_path = "%s%s_price_euro_per_100kg.csv" % (newdir_path, places[place_num])
        
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
                out_file.write(',\n')
                price_num += 1
            
            out_file.close()
        
            place_num += 1
            #print 'scraped %s' % url
    
        print 'Finish scraping at %s.' % datetime.now()
#     except Exception as err:
#         exc_info = sys.exc_info()
#         error_msg = 'auto_run() scrape error:\n'
#         msg_list = [['pig333_price'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
#         print msg_list
#         save_error_to_log('weekly', msg_list)
#     else:
#         success_msg = 'auto_run() scraped successfully\n'
#         msg_list = [['pig333_price'],[success_msg]]
#         save_error_to_log('weekly', msg_list)


if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
    