'''
Created on 18 Nov 2014

@author: Wenchong

26/11/2014(Wenchong): Fixed excluding some areas problem found during
the QA on 25/11/2014 by downloading all contents from website
instead of scraping. All symbols in the data remain the same.
04/02/3015(Wenchong): Only annually data here. Need to automate?
14/04/2015(Wenchong): Added urls to scrape all animals.
'''
import time
from datetime import datetime
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.web.scraper import WebScraper
import sys
from datas.function.function import save_error_to_log
import os


def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()
        
        file_name = 'population_annual'
        #date_from = '01/01/2015'
        #date_to = datetime.now().strftime('%d/%m/%Y')
        
        # this bookmark_url selects all geo, time, animals and units at month December
        # cattle, equidae, goat, pig, sheep
        bookmark_urls = ['http://appsso.eurostat.ec.europa.eu/nui/show.do?query=BOOKMARK_DS-055310_QID_7232F182_UID_-3F171EB0&layout=TIME,C,X,0;GEO,L,Y,0;ANIMALS,L,Z,0;MONTH,L,Z,1;UNIT,L,Z,2;INDICATORS,C,Z,3;&zSelection=DS-055310ANIMALS,A2000;DS-055310INDICATORS,OBS_FLAG;DS-055310MONTH,M12;DS-055310UNIT,THS_HD;&rankName1=UNIT_1_2_-1_2&rankName2=INDICATORS_1_2_-1_2&rankName3=ANIMALS_1_2_-1_2&rankName4=MONTH_1_2_-1_2&rankName5=TIME_1_0_0_0&rankName6=GEO_1_2_0_1&sortC=ASC_-1_FIRST&rStp=&cStp=&rDCh=&cDCh=&rDM=true&cDM=true&footnes=false&empty=false&wai=false&time_mode=NONE&time_most_recent=false&lang=EN&cfo=%23%23%23%2C%23%23%23.%23%23%23',
                         'http://appsso.eurostat.ec.europa.eu/nui/show.do?query=BOOKMARK_DS-050744_QID_61C96121_UID_-3F171EB0&layout=TIME,C,X,0;GEO,L,Y,0;ANIMALS,L,Z,0;UNIT,L,Z,1;INDICATORS,C,Z,2;&zSelection=DS-050744UNIT,THS_HD;DS-050744INDICATORS,OBS_FLAG;DS-050744ANIMALS,A1000;&rankName1=UNIT_1_2_-1_2&rankName2=INDICATORS_1_2_-1_2&rankName3=ANIMALS_1_2_-1_2&rankName4=TIME_1_0_0_0&rankName5=GEO_1_2_0_1&sortC=ASC_-1_FIRST&rStp=&cStp=&rDCh=&cDCh=&rDM=true&cDM=true&footnes=false&empty=false&wai=false&time_mode=NONE&time_most_recent=false&lang=EN&cfo=%23%23%23%2C%23%23%23.%23%23%23',
                         'http://appsso.eurostat.ec.europa.eu/nui/show.do?query=BOOKMARK_DS-063285_QID_-78783227_UID_-3F171EB0&layout=TIME,C,X,0;GEO,L,Y,0;ANIMALS,L,Z,0;MONTH,L,Z,1;UNIT,L,Z,2;INDICATORS,C,Z,3;&zSelection=DS-063285MONTH,M12;DS-063285ANIMALS,A4200;DS-063285INDICATORS,OBS_FLAG;DS-063285UNIT,THS_HD;&rankName1=INDICATORS_1_2_-1_2&rankName2=UNIT_1_2_0_1&rankName3=ANIMALS_1_2_0_0&rankName4=MONTH_1_2_0_0&rankName5=TIME_1_0_0_0&rankName6=GEO_1_2_0_1&sortC=ASC_-1_FIRST&rStp=&cStp=&rDCh=&cDCh=&rDM=true&cDM=true&footnes=false&empty=false&wai=false&time_mode=NONE&time_most_recent=false&lang=EN&cfo=%23%23%23%2C%23%23%23.%23%23%23',
                         'http://appsso.eurostat.ec.europa.eu/nui/show.do?query=BOOKMARK_DS-056126_QID_7D3AA07D_UID_-3F171EB0&layout=TIME,C,X,0;GEO,L,Y,0;ANIMALS,L,Z,0;MONTH,L,Z,1;UNIT,L,Z,2;INDICATORS,C,Z,3;&zSelection=DS-056126UNIT,THS_HD;DS-056126INDICATORS,OBS_FLAG;DS-056126MONTH,M12;DS-056126ANIMALS,A3100;&rankName1=UNIT_1_2_-1_2&rankName2=INDICATORS_1_2_-1_2&rankName3=ANIMALS_1_2_-1_2&rankName4=MONTH_1_2_-1_2&rankName5=TIME_1_0_0_0&rankName6=GEO_1_2_0_1&sortC=ASC_-1_FIRST&rStp=&cStp=&rDCh=&cDCh=&rDM=true&cDM=true&footnes=false&empty=false&wai=false&time_mode=NONE&time_most_recent=false&lang=EN&cfo=%23%23%23%2C%23%23%23.%23%23%23',
                         'http://appsso.eurostat.ec.europa.eu/nui/show.do?query=BOOKMARK_DS-055312_QID_9FA8649_UID_-3F171EB0&layout=TIME,C,X,0;GEO,L,Y,0;ANIMALS,L,Z,0;MONTH,L,Z,1;UNIT,L,Z,2;INDICATORS,C,Z,3;&zSelection=DS-055312MONTH,M12;DS-055312ANIMALS,A4100;DS-055312UNIT,THS_HD;DS-055312INDICATORS,OBS_FLAG;&rankName1=UNIT_1_2_-1_2&rankName2=INDICATORS_1_2_-1_2&rankName3=ANIMALS_1_2_0_0&rankName4=MONTH_1_2_0_0&rankName5=TIME_1_0_0_0&rankName6=GEO_1_2_0_1&sortC=ASC_-1_FIRST&rStp=&cStp=&rDCh=&cDCh=&rDM=true&cDM=true&footnes=false&empty=false&wai=false&time_mode=NONE&time_most_recent=false&lang=EN&cfo=%23%23%23%2C%23%23%23.%23%23%23']
    
        for bookmark_url in bookmark_urls:
            # open parent window by bookmark url
            wscraper = WebScraper('Chrome')
            wscraper.open(bookmark_url)
            time.sleep(5)
            
            print 'start downloading...'
            #try:
            wscraper.download_eurostat_file(file_name, bookmark_url, 10, '')
    #         except Exception as err:
    #             exc_info = sys.exc_info()
    #             raise Exception('datas.web.scraper.download_eurostat_file() error:', exc_info[0], exc_info[1], exc_info[2])
            
            wscraper.close()
        print 'Finish scraping at %s.' % datetime.now()
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['eurostat.population_annual.py'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        save_error_to_log('monthly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['eurostat.population_annual.py'],[success_msg]]
        save_error_to_log('monthly', msg_list)

if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
    
