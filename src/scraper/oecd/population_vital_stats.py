'''
Created on 1 Dec 2014

@author: Suzanne
'''

from datetime import datetime
#from datas.db.manager import DBManager
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import chunck_list, create_directory
from datas.web.scraper import WebScraper
import time
from datas.web.path import WEB_OECD_PATH

url = 'http://stats.oecd.org/'

def try_scrape(country):
    years = []
    subjects = []
    data_points = []
    scraper = WebScraper('Chrome')
    scraper.web_driver.implicitly_wait(100)
    try:
        scraper.open(url)
        scraper.web_driver.maximize_window()
        scraper.click_button('xpath', '//*[@id="browsethemes"]/ul/li[3]/span') # 'Demography and Population'
        scraper.click_button('xpath', '//*[@id="browsethemes"]/ul/li[3]/ul/li[2]/span') # 'Population Statistics'
        scraper.click_button('link_text', 'Population and Vital Statistics')
        time.sleep(5)
        try:
            scraper.web_driver.switch_to_alert().accept()
        except:
            pass
        
        
        scraper.load_field('select', 'id', 'PDim_LOCATION', country)
        time.sleep(5)
        this_query = country
        
        # Extract years
        ths = scraper.find_elements('xpath','//table/thead/tr/th[@class="HDim"]')
        for th in ths:
            years.append(th.text)
        years = filter(None, years)
        years = list(set(years))
        #print years           
        # Extract subjects
        titles = scraper.find_elements('xpath','//*[@id="tabletofreeze"]//table[@class="DataTable"]/tbody/tr/td[contains (@class,"RowDimLabel") and not (@rowspan)]')
        for title in titles:
            subjects.append(title.text.replace(',','-'))
        subjects = filter(None, subjects)
        if 'Net migration' in subjects:
            subjects.insert(subjects.index('Net migration')+1, 'NA') # to compensate for lack of unit measure, otherwise while loop for output crashes
        #print subjects
        # Extract data
        data = scraper.find_elements('xpath','//*[@id="tabletofreeze"]//table[@class="DataTable"]/tbody/tr/td[@class="Data" or @class="Data2"]')
        for d in data:
            data_points.append(d.text.replace(' ', '').replace('..','NA'))
        data_points = filter(None, data_points)
        print len(data_points)
    except Exception as e:
        print e
        scraper.close()
        return False
    else:
        scraper.close()
        #print 'Scraped '+this_query
    
        data = chunck_list(data_points, len(years))
        
        today = datetime.now().strftime('%Y_%m_%d')
        directory = create_directory('%spopulation_vital_stats' % (WEB_OECD_PATH), today)
        file_path = directory + this_query+'.csv'
        with open(file_path, 'w') as out_file:
            out_file.write('url,%s\n' % (url))
            out_file.write(',,'+(','.join(years))+'\n')
            i=0
            j=0
            while j < (len(subjects)/2):
                out_file.write(subjects[i]+','+subjects[i+1]+',')
                out_file.write(','.join(data[j]))
                out_file.write('\n')
                i=i+2
                j=j+1
        return True


def scrape(db_params):
    print 'Start scraping at %s...' % datetime.now()
       
    scraper = WebScraper('Chrome')
    scraper.web_driver.implicitly_wait(100)
    
    scraper.open(url)
    scraper.web_driver.maximize_window()
    scraper.click_button('xpath', '//*[@id="browsethemes"]/ul/li[3]/span') # 'Demography and Population'
    scraper.click_button('xpath', '//*[@id="browsethemes"]/ul/li[3]/ul/li[2]/span') # 'Population Statistics'
    scraper.click_button('link_text', 'Population and Vital Statistics')
    time.sleep(5) # implicitly_wait doesn't wait for alert box
    try:
        scraper.web_driver.switch_to_alert().accept()
    except:
        pass

    countries = scraper.get_dropdown_list('id', 'PDim_LOCATION')
    #print countries
    scraper.close()
    
    for country in countries:
        counter = 0
        while not try_scrape(country):
            print 'Trying scrape %s at counter %s...' % (country, counter)
        #while not try_scrape('35~CHN'):
            if counter >= 5:
                raise Exception('web communication error, exceeds max number of attempts, stop scraping')
            else:
                counter += 1
        
    print '...Finished at %s' % datetime.now()
    

if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params) 