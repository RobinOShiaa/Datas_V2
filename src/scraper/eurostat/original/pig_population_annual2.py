'''
Created on 18 Nov 2014

@author: Wenchong

26/11/2014(Wenchong): Fixed excluding some areas problem found during
the QA on 25/11/2014 by downloading all contents from website
instead of scraping. All symbols in the data remain the same.
04/02/3015(Wenchong): Only annually data here. Need to automate?
'''


import time
from datetime import datetime
from datas.db.manager import DBManager
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.web.scraper import WebScraper


def scrape(db_params):
    print 'Start scraping at %s...' % datetime.now()
    
    file_name = 'pig_population_annual'
    date_from = '01/01/2007'
    date_to = datetime.now().strftime('%d/%m/%Y')
    
    # this bookmark_url selects all geo, time, animals and units at month December
    bookmark_url = 'http://appsso.eurostat.ec.europa.eu/nui/show.do?query=BOOKMARK_DS-056126_QID_70303D4B_UID_-3F171EB0&layout=TIME,C,X,0;GEO,L,Y,0;ANIMALS,L,Z,0;MONTH,L,Z,1;UNIT,L,Z,2;INDICATORS,C,Z,3;&zSelection=DS-056126UNIT,THS_HD;DS-056126INDICATORS,OBS_FLAG;DS-056126MONTH,M12;DS-056126ANIMALS,A3100;&rankName1=UNIT_1_2_-1_2&rankName2=INDICATORS_1_2_-1_2&rankName3=ANIMALS_1_2_-1_2&rankName4=MONTH_1_2_-1_2&rankName5=TIME_1_0_0_0&rankName6=GEO_1_2_0_1&sortC=ASC_-1_FIRST&rStp=&cStp=&rDCh=&cDCh=&rDM=true&cDM=true&footnes=false&empty=false&wai=false&time_mode=NONE&time_most_recent=false&lang=EN&cfo=%23%23%23%2C%23%23%23.%23%23%23'
    
    # open parent window by bookmark url
    wscraper = WebScraper('Chrome')
    wscraper.open(bookmark_url)
    time.sleep(5)
    
    print 'start downloading...'
    wscraper.download_eurostat_file(file_name, bookmark_url, 10, '')
    
    wscraper.close()
    
    print 'Finish scraping at %s...' % datetime.now()


if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)