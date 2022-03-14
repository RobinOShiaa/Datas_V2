'''
Created on 1 Dec 2014

@author: Suzanne

10/04/2015(Wenchong): Data truncate problem solved.
14/10/2015(Sue): put opening of scraper inside gender loop
'''

import time
from datetime import datetime
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import chunck_list
from datas.function.function import create_directory
from datas.web.scraper import WebScraper
from datas.web.path import WEB_OECD_PATH

def try_scrape(k,v,gender):
    years = []
    data_points = []
    countries = []
    this_query = []
    url = 'http://stats.oecd.org/'  
    scraper = WebScraper('Chrome')
    scraper.web_driver.implicitly_wait(100)
    
    try:
        scraper.open(url)
        scraper.web_driver.maximize_window()
        
        scraper.click_button('xpath', '//*[@id="browsethemes"]/ul/li[3]/span') # 'Demography and Population'
        scraper.click_button('xpath', '//*[@id="browsethemes"]/ul/li[3]/ul/li[2]/span') # 'Population Statistics'
        scraper.click_button('link_text', 'Population')
        time.sleep(5) # implicitly_wait doesn't wait for alert box
        
        try:
            scraper.web_driver.switch_to_alert().accept()
        except:
            pass
        
        #print k
        scraper.load_field('select', 'id', 'PDim_SUBJECT', k)
        time.sleep(8)
        this_query.append(v)
        #print this_query
        #print gender
        scraper.load_field('select', 'name', 'PDim_SEX', gender)
        time.sleep(8)
        this_query.append(gender)
        #print this_query
        
        # Extract years
        ths = scraper.find_elements('xpath','//table/thead/tr/th[@class="HDim"]')
        y_append = years.append
        for th in ths:
            if th.text not in years:
                y_append(th.text)
        years = filter(None, years)
        #years = list(set(years))
        #print years
        # Extract countries
        titles = scraper.find_elements('xpath','//table/tbody/tr[contains(@id, "row")]/td[contains (@class,"RowDimLabel")]')
        c_append = countries.append
        for title in titles:
            if title.text not in countries:
                c_append(title.text)
        #print countries
        countries = filter(None, countries)
        #print countries
        # Extract unit
        unit = scraper.find_element('xpath','//*[@id="tabletofreeze"]/table/thead/tr[4]/th[2]').text
        this_query.append(unit)
        #print this_query,'finding data'
        # Extract data
        #data = scraper.find_elements('xpath','//*[@id="tabletofreeze"]/table/tbody/tr/td[contains(@class,"Data"]')
        data = scraper.find_elements('xpath','//*[@id="tabletofreeze"]/table/tbody/tr/td[@class="Data" or @class="Data2"]')
        #print 'found them'
        d_append = data_points.append
        for d in data:
            d_append(d.text.replace(' ', ''))
        data_points = filter(None, data_points)
    except:
        scraper.close()
        return False
    else:
        scraper.close()                 
        #print 'Scraped '+('_'.join(this_query))
                             
        '''Output data'''
        data = chunck_list(data_points, len(years))
        
        today = datetime.now().strftime('%Y_%m_%d')
        directory = create_directory('%spopulation' % WEB_OECD_PATH, today)
        file_path = directory+('_'.join(this_query))+'.csv'
        with open(file_path, 'w') as out_file:
            out_file.write('url, %s \n' % (url))
            out_file.write('Year,'+(' , '.join(years))+'\n')
            i=0
            while i < len(countries):
                out_file.write(countries[i].encode('ascii', 'ignore')+',')
                out_file.write(str(', '.join(data[i])))
                out_file.write('\n')   
                i=i+1
        return True


def scrape(db_params):
    print 'Start scraping at %s...' % datetime.now()
    
    url = 'http://stats.oecd.org/'  
    scraper = WebScraper('Chrome')
    scraper.web_driver.implicitly_wait(100)
    
    scraper.open(url)
    scraper.web_driver.maximize_window()
    
    scraper.click_button('xpath', '//*[@id="browsethemes"]/ul/li[3]/span') # 'Demography and Population'
    scraper.click_button('xpath', '//*[@id="browsethemes"]/ul/li[3]/ul/li[2]/span') # 'Population Statistics'
    scraper.click_button('link_text', 'Population')
    time.sleep(5) # implicitly_wait doesn't wait for alert box
    
    try:
        scraper.web_driver.switch_to_alert().accept()
    except:
        pass
    
    genders = scraper.get_dropdown_list('id', 'PDim_SEX') 
    
    for gender in genders[2:]:
        # Deal with different subjects available for gender options
        if '2' in gender:
            keys = scraper.get_dropdown_list('id', 'PDim_SUBJECT')[1:]
            values = scraper.get_dropdown_list('id', 'PDim_SUBJECT', 'text')[1:]
            subjects = dict(zip(keys, values))
        else:
            keys = scraper.get_dropdown_list('id', 'PDim_SUBJECT')[1:19]
            values = scraper.get_dropdown_list('id', 'PDim_SUBJECT', 'text')[1:19]
            subjects = dict(zip(keys, values))
        scraper.close()    
        
        for k,v in subjects.items():
            counter = 0
            while not try_scrape(k,v,gender):
                if counter >= 5:
                    raise Exception('web communication error, exceeds max number of attempts, stop scraping')
                else:
                    print 'Trying scrape %s, %s at counter %s...' % (v, gender, counter)
                    counter += 1
                    
    #scraper.close()
    print '...Finished at %s' % datetime.now()

if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)