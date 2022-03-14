'''
Created on 11 Nov 2014

@author: Suzanne

08/01/2015(Wenchong): Automation completed.
27/01/2015(Wenchong): Website rebuilt, adapted the changes.
11/02/2015(Wenchong): Fixed sql query to get the correct date as a new scraping point.
'''

import re
import urllib2
from bs4 import BeautifulSoup
from datetime import datetime
from datas.db.manager import DBManager
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import chunck_list
from datas.function.function import create_directory
from datas.web.path import WEB_BPEX_PATH


def scrape():
    print 'Start scraping at %s...' % datetime.now()
    
    # get the latest data date from DB
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    dbm = DBManager(db_params[0], db_params[1], db_params[2], db_params[3])
    sql = ('select max(week_end_date) as max_date from bpex_weekly_slaughtering '
           'group by member_state, type order by max_date asc limit 1;')
    date_from = dbm.get_latest_date_record(sql)
    date_from = date_from[0]
    del dbm
    
    # website rebuilt, url changed
    #url = 'http://www.bpex.org.uk/prices-facts-figures/production/EUweeklypigslaughterings.aspx'
    url = 'http://www.bpex.org.uk/prices-stats/production/eu-weekly-pig-slaughterings/'
    flag = 0
    animal = ''
    
    # Start scraping
    req = urllib2.Request(url)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page)
    #table = soup.find("table")
    hregex = '^\w+\s\w+$'
    
    # get the latest data date from web
    web_date = soup.findAll("table")[0].findAll('tr')[1].findAll('td')[1]
    web_date = web_date.text.strip().replace('      ', ' ')
    web_date = datetime.strptime(web_date, '%d %B %Y').date()
    
    # TODO(Wenchong): 27/01/2015 need to check the date for every record with db
    if date_from >= web_date:
        print 'No new data found, terminated at %s...' % datetime.now()
        return
    
    tables = soup.findAll("table")
    for table in tables:
        headers = []
        data = []
        if flag == 0:
            flag = 1
            animal = 'Clean Pigs'
        else:
            animal = 'Cull Sows'
        heads = table.findAll('th')
        for th in heads:
            match = re.match (hregex, th.text)
            if match:
                headers.append(th.text)
        
        rows = table.findAll('tr')
        for tr in rows:
            cols = tr.findAll('td')[0:3]
            for td in cols:
                data.append(td.text.replace(',', '').replace('      ', ' '))
    
        data = chunck_list(data, 3)
        
        dir_title = datetime.now().strftime('%Y_%m_%d')
        dir_path = '%sslaughtering\\' % WEB_BPEX_PATH
        dir_path = create_directory(dir_path, dir_title)
        file_path = '%sweekly_slaughterings_%s_1 head.csv' % (dir_path, animal)
        
        out_file = open(file_path, 'w')
        out_file.write('url, %s' % (url))
        out_file.write('\n')
        out_file.write(', '.join(headers))
        out_file.write('\n')
        
        for d in data:
            out_file.write(', '.join(d))
            out_file.write('\n')
    
    # Alternative to download file
    # source_file = '/users/suzanne/downloads/EUweeklyslaughter091114.xls'
    # dest_file = BPEX_PATH + 'EUweeklyslaughter'+today+'.xls'
    # browser = webdriver.Chrome() 
    # browser.get(url)       
    # element = browser.find_element_by_xpath('//*[@id="rightcol"]/p[5]/a')
    # element.click 
    # os.rename(source_file, dest_file)               
    
    print 'Finish scraping at %s...' % datetime.now()


if __name__ == '__main__':
    scrape()