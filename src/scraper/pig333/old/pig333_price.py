'''
Created on 17 Nov 2014

@author: Conor O'Sullivan

03/02/2015(Wenchong): Automation completed.
12/02/2015(Wenchong): Fixed sql query to get the correct date as a new scraping point.
'''

import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver 
from selenium.webdriver.common.action_chains import ActionChains
from datas.db.manager import DBManager
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import create_directory
from datas.web.path import WEB_PIG333_PATH


def button_click(browser, button_name):
    element = browser.find_element_by_id(button_name)
    element.click()


def login(browser, username_element, password_element, username, password, remember_me_id, button_id):
    #Uses tag IDs. NB - Must have already registered with site.
    element1 = browser.find_element_by_id(username_element)
    element1.send_keys(username)
    element2 = browser.find_element_by_id(password_element)
    element2.send_keys(password)
    if remember_me_id is not None:
        button_click(browser, remember_me_id) 
    button_click(browser, button_id)
    print 'Logged in.'  


def get_data(elements):
    data_list = []
    for element in elements:
        data_list.append(element.text)
    return data_list    



def scrape(db_params):
    print 'Start scraping at %s...' % datetime.now()
    
    # get the latest data date from DB
    dbm = DBManager(db_params[0], db_params[1], db_params[2], db_params[3])
    sql = ('select max(date) as max_date from pig333_pig_price '
           'group by geo order by max_date asc limit 1;')
    date_from = dbm.get_latest_date_record(sql)
    date_from = date_from[0]
    del dbm
    print date_from
    
    dir_title = datetime.now().strftime('%Y_%m_%d')
    dir_path = '%spig_price\\' % WEB_PIG333_PATH
    dir_path = create_directory(dir_path, dir_title)
    
    links_url = 'http://www.pig333.com/markets_and_prices/'
    r = requests.get(url=links_url, verify=False)
    
    links_soup = BeautifulSoup(r.content)
    a_links = links_soup.find_all("a", {"class":"nom_mercat"})
    
    urls = []
    places = []
    
    for a_link in a_links:
        urls.append(a_link.get('href'))
        places.append(a_link.text.replace(' ','').replace('/','_').strip())
    
    place_num = 0
    
    your_email = 'cosullivan@computing.dcu.ie'
    your_password = 'ilovepigs'
    
    #browser = webdriver.Firefox()
    browser = webdriver.Chrome()
    
    logged_in = False
    
    for url in urls:
        #Log in
        browser.get(url)
        
        if logged_in == False:
            time.sleep(2)
            button_click(browser, 'boto_area_usuarios')
            time.sleep(6)
            login(browser, 'input_email', 'input_pass', your_email, your_password, 'inp_rec_barra_login', 'boto_login_div_registre')
            logged_in = True
            
        time.sleep(10)

        
        currency_menu = browser.find_element_by_xpath(".//*[@id='div_wrap_moneda']")
    
        hover = ActionChains(browser).move_to_element(currency_menu)
        hover.perform()
    
        euro_option = browser.find_element_by_xpath(".//*[@id='div_menu_monedes']/li[4]")
        euro_option.click()
        #mystr = str(euro_option.text)
    
        time.sleep(3)
        unit_select = browser.find_element_by_xpath(".//*[@id='select_unitats']")
        unit_select.click()
        
        for option in unit_select.find_elements_by_tag_name('option'):
            if option.text == '100kg':
                option.click()
        
        time.sleep(3)
    
        html = browser.page_source
    
        soup = BeautifulSoup(html)
        
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
        
        formatted_dates = []
        
        for date in dates:        
            formatted_dates.append(str(datetime.strptime(date,"%b %d, %Y"))[:10])
    
        headers = ["Date","Price(Euro/kg)"]
        
        file_path = "%s%s_price_euro_per_kg.csv" % (dir_path, places[place_num])
    
        out_file = open(file_path,'w')
        out_file.write('url, %s' % (url))
        out_file.write(',\n')
        
        out_file.write(', '.join(headers))
        out_file.write(',\n')
        
        price_num = 0
        for formatted_date in formatted_dates:
            out_file.write(formatted_date)
            out_file.write(',')
            out_file.write(prices[price_num])
            out_file.write(',')
            out_file.write('\n')
            price_num += 1
        
        out_file.close()
    
        place_num += 1
    
    browser.quit() 
    
    print 'Finish scraping at %s...' % datetime.now()


if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)