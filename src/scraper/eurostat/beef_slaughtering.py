'''
Created on 18 Jan 2016

@author: Suzanne
'''
from datetime import datetime
import time
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.web.scraper import WebScraper
import sys
from datas.function.function import save_error_to_log


def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()
        
        file_name = 'beef_slaughtering'
        bookmark_url='http://appsso.eurostat.ec.europa.eu/nui/show.do?query=BOOKMARK_DS-056124_QID_5D7FD6EE_UID_-3F171EB0&layout=TIME,C,X,0;GEO,L,Y,0;MEAT,L,Z,0;MEATITEM,L,Z,1;UNIT,L,Z,2;INDICATORS,C,Z,3;&zSelection=DS-056124MEAT,B3100;DS-056124INDICATORS,OBS_FLAG;DS-056124MEATITEM,SL;DS-056124UNIT,THS_T;&rankName1=MEAT_1_2_-1_2&rankName2=UNIT_1_2_-1_2&rankName3=MEATITEM_1_2_-1_2&rankName4=INDICATORS_1_2_-1_2&rankName5=TIME_1_0_0_0&rankName6=GEO_1_0_0_1&sortR=ASC_-1_FIRST&sortC=ASC_-1_FIRST&rStp=&cStp=&rDCh=&cDCh=&rDM=true&cDM=true&footnes=false&empty=false&wai=false&time_mode=ROLLING&time_most_recent=true&lang=EN&cfo=%23%23%23%2C%23%23%23.%23%23%23'
        wscraper = WebScraper('Chrome')
        wscraper.open(bookmark_url)
        time.sleep(5)
        
        print 'start downloading...'

        wscraper.download_eurostat_file(file_name, bookmark_url, 20, '')
        
        wscraper.close()
        
        print 'Finish scraping at %s...' % datetime.now()
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['eurostat.beef_slaughtering'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n\n']]
        save_error_to_log('monthly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['eurostat.beef_slaughtering'],[success_msg]]
        save_error_to_log('monthly', msg_list)


if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
    

