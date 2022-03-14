'''
Created on 10 Dec 2014

@author: Suzanne
'''
from datetime import datetime
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import create_directory, save_error_to_log
from datas.web.scraper import WebScraper
from datas.web.path import WEB_ACCUWEATHER_PATH
import pandas as pd
import time
import re
import sys

def scrape(db_params):
    #try:
        print 'Start scraping at %s...' % datetime.now()
        
        today = datetime.now().strftime("%Y_%m_%d")
        
        not_scraped = []
        headers = ['Country','City','Time','Temperature', 'Precipitation', 'Rain', 'Snow', 'Ice', 'URL']
                    
        new_directory = create_directory(WEB_ACCUWEATHER_PATH, today)
        out_file = open('%sweather_data.csv' % new_directory, 'a')
        out_file.write(','.join(headers) +'\n')
        
        file = 'searches.csv'
        df = pd.read_csv(file, index_col = None)
    
        codes = df['code']
        countries = df['country']
        
        searches = dict(zip(codes, countries))
        
        '''Start scrape'''
        for code, country in searches.items():
            
            #cities = []
            #temps = []
    
            url = 'http://www.accuweather.com/en/%s/%s-weather' % (code, country)
            try:
                scraper = WebScraper('Chrome')
                scraper.open(url)
            except:
                not_scraped.append(country)   
            else:
                scraper.web_driver.maximize_window()
                
                links = []
                city_tags = scraper.find_elements('xpath', './/ul[@class="top-cities lt"]/li/div/a')
                for c_t in city_tags:
                    links.append(c_t.get_attribute('href'))
                #print links
                scraper.close()
                for link in links:#i in xrange(1, len(city_tags)):
                    city = link.split('/')[5]
                    try:
                        scraper = WebScraper('Chrome')
                        scraper.open(link)
                        #city_tag = scraper.find_element('xpath', './/ul[@class="top-cities lt"]/li[%s]//h6' % i)
                        #temp_tag = scraper.find_element('xpath', './/ul[@class="top-cities lt"]/li[%s]//span' % i)
    
                        
                        
                    except:
                        print 'problem with ', link
                        pass
                    
                    else:
                        temp_tag = scraper.find_element('xpath', '//*[@id="feed-main"]/div[3]/strong')
                        temp = ''.join(re.findall('[-.0-9]' ,temp_tag.text)) + ' deg'
                        scraper.click_button('xpath', './/*[@id="feed-sml-1"]/div/div')
                        time.sleep(5)
                        
                        #city = city_tag.text.encode('utf-8', 'replace')
                        #print city
                        
                        #city_tag.click()
    
                        stats = scraper.find_elements('xpath', './/div[contains(@class, "day")]//ul[@class="stats"]/li') #div[@class="day"]//
                        
                        for stat in stats:
                            if 'Hours of' not in stat.text:
                                if 'Precipitation' in stat.text:
                                    precipitation = stat.text.split(': ')[1]
                                if 'Rain' in stat.text:
                                    rain = stat.text.split(': ')[1]
                                if 'Snow' in stat.text:
                                    snow = stat.text.split(': ')[1]
                                if 'Ice' in stat.text:
                                    ice = stat.text.split(': ')[1]
                                #print stat.text
                            
                        scraper.web_driver.back()
                        scraper.web_driver.back()
    
                        out_file.write(','.join([country, city, datetime.strftime(datetime.now(), '%Y-%m-%d %H-%M-%S'), temp, precipitation, rain, snow, ice, link]))
                        out_file.write('\n')
                    scraper.close()
    
        out_file.close()
        print 'Finished scraping at %s.' % datetime.now()
        print 'Not scraped:'
        print not_scraped
#     except Exception as err:
#         exc_info = sys.exc_info()
#         error_msg = 'auto_run() scrape error:\n'
#         msg_list = [['accuweather.py'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
#         print msg_list
#         save_error_to_log('weekly', msg_list)
#     else:
#         success_msg = 'auto_run() scraped successfully\n'
#         msg_list = [['accuweather.py'],[success_msg]]
#         save_error_to_log('weekly', msg_list)

if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
