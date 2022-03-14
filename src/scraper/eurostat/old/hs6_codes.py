'''
Created on 25 Feb 2015

@author: Suzanne
'''
from datetime import datetime
from bs4 import BeautifulSoup
from datas.db.manager import DBManager
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.web.path import WEB_EUROSTAT_PATH
import time
from datas.function.function import *
from datas.web.scraper import *


def click_expand_button(wscraper, attr_name, attr_value):

    expand_buttons = wscraper.find_elements(attr_name, attr_value)
    
    for btn in expand_buttons:
        btn.click()
        time.sleep(3)
        click_expand_button(attr_name, attr_value)
        break

def scrape(db_params):
    print 'Start scraping at %s...' % datetime.now()
    
    hs_codes = []
    descs = []
    bookmark_url = 'http://appsso.eurostat.ec.europa.eu/nui/show.do?query=BOOKMARK_DS-016893_QID_434869AC_UID_-3F171EB0&layout=PERIOD,L,X,0;REPORTER,L,Y,0;PARTNER,L,Z,0;PRODUCT,C,Z,1;FLOW,L,Z,2;INDICATORS,C,Z,3;&zSelection=DS-016893PARTNER,EU28_EXTRA;DS-016893INDICATORS,VALUE_IN_EUROS;DS-016893PRODUCT,TOTAL;DS-016893FLOW,1;&rankName1=PARTNER_1_2_-1_2&rankName2=INDICATORS_1_2_-1_2&rankName3=FLOW_1_2_-1_2&rankName4=REPORTER_1_2_0_1&rankName5=PERIOD_1_0_0_0&rankName6=PRODUCT_1_2_-1_2&sortR=DND_-1&prRK=FIRST&prSO=PROTOCOL&ppcRK=FIRST&ppcSO=ASC&sortC=ASC_-1_FIRST&rLShi=0:2-26,27:0,29:1,28:29&rStp=&cStp=&rDCh=&cDCh=&rDM=true&cDM=true&footnes=false&empty=false&wai=false&time_mode=NONE&time_most_recent=false&lang=EN&cfo=%23%23%23%2C%23%23%23.%23%23%23'
    
    wscraper = WebScraper('Chrome')
      
    # open parent window by bookmark url
    wscraper.open(bookmark_url)
    wscraper.wait(30, 'class', 'selectDataButton')
      
    # open option window
    wscraper.click_button('class', 'selectDataButton')
      
    # get control of the popup option window
    wscraper.switch_to_popup_window()
    time.sleep(2)
     
    wscraper.click_button('xpath', '//div/a/span[contains(text(), "PRODUCT")]')
    time.sleep(2)
    click_expand_button(wscraper, 'class', 'middle_branch_plus')

    source = wscraper.web_driver.page_source
    with open ('hs_source.txt', 'w') as outfile:
        outfile.write(source.encode('ascii', 'ignore'))
        
    with open ('hs_source.txt', 'rb') as infile:
        html = infile.read()
    
    
    soup=BeautifulSoup(html, 'html5lib')

    tags_a = soup.findAll("td")
    for tag in tags_a:
        if tag.get('title') is not None:
            descs.append(tag.get('title').replace(',','-')) # DON'T use .text 
    
    #tags_b = soup.findAll("input", { "type" : "checkbox" })
    tags_b = soup.findAll("a")
    for tag in tags_b:
        if '  ' not in tag.text:
            hs_codes.append(tag.text)
    
    
#     print hs_codes
#     print descs
#     print len(descs)
    
    with open('%s\hs_codes.csv' %WEB_EUROSTAT_PATH,'w') as outfile:
        x=0
        while x < len(hs_codes):
            outfile.write('%s,%s\n' % (hs_codes[x],descs[x]) )
            x+=1
    
    print 'finished scraping at %s' % datetime.now()


if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)