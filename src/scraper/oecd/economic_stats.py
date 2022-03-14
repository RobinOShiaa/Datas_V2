'''
Created on 25 Nov 2014

@author: Suzanne
'''
from datetime import datetime
#from datas.db.manager import DBManager
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import create_directory, chunck_list
from datas.web.scraper import WebScraper
from datas.web.path import WEB_OECD_PATH
import lxml.html as lh
from lxml import etree
import time
from io import StringIO

url = 'http://stats.oecd.org/'

def try_scrape(k, this_query, directory):
    scraper = WebScraper('Chrome')
    scraper.web_driver.implicitly_wait(100)
    try:
        scraper.open(url)
        scraper.web_driver.maximize_window()
        
        scraper.click_button('xpath', '//*[@id="browsethemes"]/ul/li[5]') # 'Economic projections'
        scraper.click_button('xpath', '//*[@id="browsethemes"]/ul/li[5]/ul/li') # 'OECD economic outlook'
        scraper.click_button('xpath', '//*[@id="browsethemes"]/ul/li[5]/ul/li/ul/li[2]') # 'OECD economic outlook latest edition'
        scraper.click_button('xpath', '//*[@id="browsethemes"]/ul/li[5]/ul/li/ul/li[2]/ul/li[1]') # most recent projections
        scraper.click_button('link_text', 'EO By Subject (GDP, Unemployment...)')
        time.sleep(10) # implicitly_wait doesn't wait for alert box
        
        try:
            scraper.web_driver.switch_to_alert().accept()
        except:
            pass
        
        scraper.load_field('select', 'id', 'PDim_VARIABLE', k)
        years = []
        #ths = scraper.find_elements('xpath', '//table/thead/tr/th[@class="HDim"]')#'html//div[@id="content"]//div[@id="divcontent"]//div[@id="tabletofreeze"]//table[@class="DataTable"]//thead//tr[3]//th//text')#//*[@id="tabletofreeze"]/table/thead/tr[3]/th[2]
        #ths = scraper.find_elements('xpath', './/*[@id="fixedheader"]/table/thead/tr[3]/th[@class="HDim"]')
        html = scraper.html_source()
        
        tree = lh.fromstring(html)
        print tree
        ths = tree.xpath('.//*[@id="fixedheader"]/table/thead/tr[3]/th[@class="HDim"]')
        for elt in ths:            
            years.append(elt.text)
        
        
        
        
        countries = []    
        #titles = tree.xpath('.//div[@id="divcontent"]//div[@id="contentcenter"]//div[@id="tabletofreeze"]/table[@class="DataTable"]/tbody/tr/td[contains (@class,"RowDimLabel") and not (@rowspan)]')
        titles = tree.xpath('.//*[@id="fixedheader"]/table/tbody/tr/td[contains (@class,"RowDimLabel") or contains (@class,"RowDimLabel2") and not (@rowspan)]')
        title_row = 0
        while title_row < len(titles):
            title_text = titles[title_row].text_content()
            if 'Non-OECD Member Economies' in title_text:
                title_row += 2
            else:
                print titles[title_row].text_content()
                countries.append(titles[title_row].text_content().replace(',', '-'))
                title_row += 1
        
        data_points = []
        time.sleep(5)
        
        # Extract data
        data = tree.xpath('//*[@id="tabletofreeze"]/table/tbody//td[contains (@class,"Data")]')
        for d in data:
            data_points.append(d.text_content().replace(' ', ''))
            
        data = chunck_list(data_points, len(years))
        
    #print 'len of data', len(data)
    except ValueError:
        scraper.close()
        return False
    else:
        scraper.close()
        #print 'Scraped '+this_query

        file_path = '%s/%s.csv' % (directory, this_query)
        with open(file_path, 'w') as out_file:
            out_file.write('url,%s\n' % (url))
            out_file.write(',,'+(','.join(years))+'\n')
            i=0
            j=0
            while j < len(countries)/3:

                out_file.write(countries[i].encode('ascii', 'ignore')+','+countries[i+1].encode('ascii', 'ignore')+',')
                out_file.write(str(','.join(data[j])))
                out_file.write('\n')   
                i = i+3
                j = j+1
       
        return True

def scrape(db_params):
    print 'Start scraping at %s...' % datetime.now()
       
    today = datetime.now().strftime('%Y_%m_%d')
    directory = create_directory(WEB_OECD_PATH+'economic_stats', today)
               
    '''Start scrape'''
    scraper = WebScraper('Chrome')
    scraper.web_driver.implicitly_wait(100)
    scraper.open(url)
    scraper.web_driver.maximize_window()
    
    scraper.click_button('xpath', '//*[@id="browsethemes"]/ul/li[5]') # 'Economic projections'
    scraper.click_button('xpath', '//*[@id="browsethemes"]/ul/li[5]/ul/li') # 'OECD economic outlook'
    scraper.click_button('xpath', '//*[@id="browsethemes"]/ul/li[5]/ul/li/ul/li[2]') # 'OECD economic outlook latest edition'
    scraper.click_button('xpath', '//*[@id="browsethemes"]/ul/li[5]/ul/li/ul/li[2]/ul/li[1]') # most recent projections
    scraper.click_button('link_text', 'EO By Subject (GDP, Unemployment...)')
    time.sleep(5) # implicitly_wait doesn't wait for alert box
    
    try:
        scraper.web_driver.switch_to_alert().accept()
    except:
        pass
   
    keys = scraper.get_dropdown_list('id', 'PDim_VARIABLE')
    values = scraper.get_dropdown_list('id', 'PDim_VARIABLE', 'text')
    features = dict(zip(keys, values))
    scraper.close()
               
    for k,v in features.items()[17:]:
        
        if v[:2]=='  ':
            #if v[2:] =='General government gross financial liabilities, as a percentage of GDP':
                       
            this_query = v[2:].replace(',','')
            
            counter = 0

            while not try_scrape(k, this_query, directory):
                if counter >= 2:
                    raise Exception('web communication error, exceeds max number of attempts, stop scraping')
                else:
                    print 'Trying scrape %s at counter %s...' % (v, counter)
                    counter += 1
 
    print 'Finished at %s.' % datetime.now()


if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
