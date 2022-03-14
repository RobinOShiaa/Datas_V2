'''
Created on 21 Nov 2014

@author: Suzanne
'''
#from selenium import webdriver
from datetime import datetime
#from datas.db.manager import DBManager
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import chunck_list, create_directory
from datas.web.scraper import WebScraper
import time
from datas.web.path import WEB_OECD_PATH
import lxml.html as lh 
#from lxml import etree

#utf8_parser = etree.XMLParser(encoding='unicode')

url = 'http://stats.oecd.org/viewhtml.aspx?QueryId=48184&vh=0000&vf=0&l&il=&lang=en#'
today = datetime.now().strftime("%Y_%m_%d")

def try_scrape(k, v, feature):
    years = []
    data_points = []
    commodities = []
    this_query = []
    scraper = WebScraper('Chrome')
    scraper.web_driver.implicitly_wait(100)
    
    scraper.open(url)
    scraper.web_driver.maximize_window()
    time.sleep(5)
    
    try:
        scraper.web_driver.switch_to_alert().accept()
    except:
        pass

    scraper.load_field('select','id','PDim_COUNTRY', k)
    this_query.append(v)
    time.sleep(5)
    
    html = scraper.html_source()
        
    tree = lh.fromstring(html)
    print feature
    scraper.load_field('select','id', 'PDim_VARIABLE', feature)
    search = tree.xpath('//option[@value="%s"]' % feature)
    print search
    this_query.append(search[0].text_content())

    # Extract years
    ths = tree.xpath('.//*[@id="tabletofreeze"]//table//thead//tr[3]//th[@class="HDim"]')
    
    for th in ths:
        print th.text_content()
        years.append(th.text_content())
    try:
        # Extract commodities
        titles = tree.xpath('//*[@id="tabletofreeze"]/table/tbody//tr/td[contains (@class,"RowDimLabel") and not (@rowspan)]')
        print len(titles)
        for title in xrange(len(titles)):        
            #colspan = titles[title].Element("colspan")
            #print colspan
            #if not title.text.isupper() or colspan is not None:
            #    if title.text not in commodities:
            commodities.append(titles[title].text_content())
        commodities = filter(None, commodities)
        print commodities

        # Extract data
        data = tree.xpath('//*[@id="tabletofreeze"]/table/tbody//td[@class="Data" or @class="Data2"]')
        for d in data:
            #print d.find('table/tbody/tr/td').text_content()
            print d.text_content()            
            #data_points.append(d.text_content().replace(' ', ''))     
            data_points.append(d.text_content().encode('ascii', 'ignore'))       
        data_points = filter(None, data_points)
        print data_points

    except:
        scraper.close()
        return False
    else:
        scraper.close()          
        #print 'Scraped '+(' '.join(this_query))

        data_points = chunck_list(data_points, len(years))
        print commodities
        for i in range(0, len(data_points)):
            data_points[i].insert(0, commodities[i].encode('ascii', 'ignore'))
    
        directory = create_directory('%s/past_forecasts/' % WEB_OECD_PATH, today)
        file_path = directory+('_'.join(this_query))+'.csv'
        with open(file_path, 'w') as out_file:
            out_file.write('url,%s\n' % (url))
            out_file.write('Year,'+(','.join(years))+'\n')
            for d in data_points:
                #print d
                out_file.write(','.join(d)+'\n')
        return True
    

def scrape(db_params):
    print 'Start scraping at %s...' % datetime.now()
       
    scraper = WebScraper('Chrome')
    scraper.web_driver.implicitly_wait(100)
    
    scraper.open(url)
    scraper.web_driver.maximize_window()
    
    time.sleep(5) # implicitly_wait doesn't wait for alert box
    try:
        scraper.switch_to_alert().accept()
        #print "alert accepted"
    except:
        pass
        #print "no alert"
    
    keys = scraper.get_dropdown_list('id', 'PDim_COUNTRY')
    values = scraper.get_dropdown_list('id', 'PDim_COUNTRY', 'text')
    scraper.close()
    countries = dict(zip(keys, values))
    features = ['3~IM', '4~QC', '5~ST','6~EX', '1~QP']
        
    for k,v in countries.items():
        for feature in features:
   
            if '  ' in v:
                counter = 0
                while not try_scrape(k, v, feature):
                    if counter >= 5:
                        raise Exception('web communication error, exceeds max number of attempts, stop scraping')
                    else:
                        print 'Trying scrape %s, %s at counter %s...' % (v, feature, counter)
                        counter += 1
    
    print 'Finished at %s.' % datetime.now()


if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
