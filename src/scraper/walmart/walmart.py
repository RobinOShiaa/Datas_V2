'''
Created on 13 Mar 2015

@author: Suzanne
'''
import random
import os
import socket
from datetime import datetime
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import create_directory
from datas.web.path import WEB_WALMART_PATH
import sys
from datas.function.function import save_error_to_log
from bs4 import BeautifulSoup
import urllib2

def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()
        base_url = 'http://www.walmart.com/browse/food/whatever/976759_' # yes, really
        
        today = datetime.strftime(datetime.now(), '%Y_%m_%d')
        dir = create_directory(WEB_WALMART_PATH, today)
        
        # make program act like different browser each time it hits the site
        UserAgents = ['Mozilla/5.0 (Windows NT 6.2; rv:22.0) Gecko/20130405 Firefox/22.0','Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'
                      ,'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; Media Center PC 6.0; InfoPath.3; MS-RTC LM 8; Zune 4.7','Mozilla/5.0 (Linux; U; Android 2.3.3; en-us; HTC_DesireS_S510e Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile'
                      ,'Mozilla/5.0 (BlackBerry; U; BlackBerry 9850; en) AppleWebKit/534.11+ (KHTML, like Gecko) Version/7.0.0.254 Mobile Safari/534.11+','Opera/9.80 (J2ME/MIDP; Opera Mini/9 (Compatible; MSIE:9.0; iPhone; BlackBerry9700; AppleWebKit/24.746; U; en) Presto/2.5.25 Version/10.54'
                      ,'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',"Mozilla/5.0 (Windows NT 6.2; Win64; x64;) Gecko/20100101 Firefox/20.0"]
               
        #restricting urllib to 10 secs
        timeout = 10
        socket.setdefaulttimeout(timeout)
    
        for j in range(1, 26):
            for i in range(976779, 976797):
                data = []
                url = '%s%s?page=%s&soft_sort=false&cat_id=976759_%s&grid=false' % (base_url, str(i), str(j), str(i))
                print '\nsearching url: %s' % url
                index = random.randint(0, 7)
                # try to find current selection to use as filename, else create dummy file to prevent program writing additional lines to useful files
                try:
                    headers = {'User-Agent' : UserAgents[index]}
                    req = urllib2.Request(url,headers=headers)
                    response = urllib2.urlopen(req)
                    #time.sleep(6)
                    html = response.read()
                    soup=BeautifulSoup(html, 'html5')
                    filename = ''
                    #print soup.prettify()
                
                
                    filename = soup.find("h1", class_="breadcrumb-leaf").text.replace('\n','')
                except:
                    filename = 'ignore'
    
                print filename, j
                #time.sleep(3)
                divs = soup.find_all("div", { "class" : "tile-content" })
                for div in divs:
                    data_point = []
                    product = div.find("a", { "class" : "js-product-title" })
                    data_point.append(product.text.encode('ascii','ignore').replace(',','-').replace('\n',''))
                    price = div.find("div", class_="price-aux")
                    
                    try:
                        if '/' in price.text: # ignore items that do not have a price per unit of measure
                            data_point.append(price.text.encode('ascii','ignore'))
                    except AttributeError:
                        pass
                    if len(data_point) > 1:
                        data.append(data_point)
                    #print data_point
    #             prod_names = []
    #             #tags = soup.find_all("a", { "class" : "prodLink ListItemLink" })
    #             tags = soup.find_all("a", { "class" : "js-product-title" })
    #             for tag in tags:
    #                 prod_names.append(tag.text.encode('ascii','ignore').replace(',','').replace('\n',''))
    #             print len(prod_names)    
    #             prices = []    
    #             #tags = soup.find_all("span", class_="ppuPrice")
    #             tags = soup.find_all("div", class_="price-aux")
    #             for tag in tags:
    #                 prices.append(tag.text.encode('ascii','ignore'))
    #             print len(prices)    
                response.close()
                
                with open('%s%s.csv' % (dir, filename),'a') as out:
                    if j == 1:
                        out.write('url,%s\n' % url)
                    for d in data:
                        out.write(','.join(d))
                        out.write('\n')
        os.remove("%s%s/ignore.csv" % (WEB_WALMART_PATH, today))
        print 'Finished scraping at %s.' % datetime.now()
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['walmart.py'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('weekly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['walmart.py'],[success_msg]]
        save_error_to_log('weekly', msg_list)

if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
    
