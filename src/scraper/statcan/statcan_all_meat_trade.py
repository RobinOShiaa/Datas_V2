'''
Created on 6 Feb 2015

@author: Suzanne

16/04/2015(Wenchong): Fixed the file can't download bug caused by the years/months problem.
'''
import sys
import os
from datas.function.function import save_error_to_log
from bs4 import BeautifulSoup
import urllib2 
import re
import time
import pandas as pd
import math
import socket
from datas.web.scraper import WebScraper, create_directory
from datas.db.manager import DBManager, RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.web.path import WEB_STATCAN_PATH
from datetime import datetime
from datas.function.function import delete_file


def monthcal(month,datest):
    if datest == 'Date1' :
        monthint = int(month) 
    elif datest == 'Date2':
        monthint = int(month) - 1
    elif datest == 'Date3':
        monthint = int(month) - 2
    elif datest == 'Date4':
        monthint = int(month) - 3
    
    if monthint < 10:
        return '0' + str(monthint)
    else:
        return str(monthint)

def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()
        
        # get the latest data date from DB
        dbm = DBManager(db_params[0], db_params[1], db_params[2], db_params[3])
        date_from = dbm.get_latest_date_record('select max(yearmonth) from statcan_all_meat_trade;')
        date_from = datetime.strptime(str(date_from[0]), '%Y%m')
        year_from = date_from.year
        month_from = date_from.month
        #print month_from
        del dbm
    
        #year_from = datetime.strptime('2015','%Y').year
        #month_from = datetime.strptime('01','%m').month
        
        today = datetime.strftime(datetime.now(), '%Y_%m_%d')
        dir_path = create_directory(WEB_STATCAN_PATH+'all_meat_trade\\', today)
        filename='%sstatcan.csv' % dir_path
        
        # get hs codes from dropdown menu
        wscraper = WebScraper('Chrome')
        temp_url = ('http://www5.statcan.gc.ca/cimt-cicm/topNCountryCommodities-marchandises?'
                    'countryId=999&tradeType=1&usaState=&topNDefault=10&freq=6&commodityName='
                    'Swine+carcasses+and+half+carcasses%2C+fresh+or+chilled&lang=eng&refYr=2015'
                    '&sectionId=&chapterId=2&arrayId=9800000&provId=1&refMonth=1&commodityId=20311')
        wscraper.open(temp_url)
        wscraper.wait(10, 'id', 'commodityIdAndName')
        hscode = wscraper.get_dropdown_list('id', "commodityIdAndName", 'text')
        wscraper.close()
            
        this_year = datetime.now().year
        this_month = datetime.now().month
        years = xrange(year_from, this_year + 1)
        
        # make program act like different browser each time it hits the site
        UserAgents = ['Mozilla/5.0 (Windows NT 6.2; rv:22.0) Gecko/20130405 Firefox/22.0','Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'
                      ,'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; Media Center PC 6.0; InfoPath.3; MS-RTC LM 8; Zune 4.7','Mozilla/5.0 (Linux; U; Android 2.3.3; en-us; HTC_DesireS_S510e Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile'
                    ,'Mozilla/5.0 (BlackBerry; U; BlackBerry 9850; en) AppleWebKit/534.11+ (KHTML, like Gecko) Version/7.0.0.254 Mobile Safari/534.11+','Opera/9.80 (J2ME/MIDP; Opera Mini/9 (Compatible; MSIE:9.0; iPhone; BlackBerry9700; AppleWebKit/24.746; U; en) Presto/2.5.25 Version/10.54'
                    ,'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',"Mozilla/5.0 (Windows NT 6.2; Win64; x64;) Gecko/20100101 Firefox/20.0"]
    
        #restricting urllib to 10 secs
        timeout = 10
        socket.setdefaulttimeout(timeout)
        
        # input year, month and hs code to url
        for k in range(1,len(hscode)): # ignore first code to avoid duplicate data - DON'T CHANGE THIS
            for year in years: 
                time.sleep(2)
                
                if len(years) == 1:
                    months = xrange(month_from, this_month + 1)
                elif len(years) == 2:
                    if year < this_year:
                        months = xrange(month_from, 13)
                    elif year == this_year:
                        months = xrange(1, this_month + 1)
                elif len(years) >= 3:
                    if year < this_year - 1:
                        months = xrange(month_from, 13)
                    elif year == this_year - 1:
                        months = xrange(1, 13)
                    elif year == this_year:
                        months = xrange(1, this_month + 1)
                else:
                    break
                
                for month in months: 
                    datablock=[]
                    
                    url = ('http://www5.statcan.gc.ca/cimt-cicm/topNCountryCommodities-marchandises?countryId=999&'
                           'tradeType=1&usaState=&topNDefault=250&freq=6&commodityName=Swine+carcasses+and+half+'
                           'carcasses%2C+fresh+or+chilled&lang=eng&refYr=' + str(year) + '&sectionId=&chapterId=2&arrayId='
                           '9800000&provId=1&refMonth=' + str(month) +'&commodityId=' +hscode[k][:6])
                    
                    #url='http://www5.statcan.gc.ca/cimt-cicm/topNCountries-pays?lang=eng&sectionId=1&dataTransformation=0&refYr=' + year[i] + '&refMonth=' + month[j] + '&freq=6&countryId=0&usaState=0&provId=1&retrieve=Retrieve&save=null&country=null&tradeType=1&topNDefault=250&monthStr=null&chapterId=2&arrayId=0&sectionLabel=I%20-%20Live%20animals%20and%20animal%20products.&scaleValue=0&scaleQuantity=0&commodityId=' + hscode[k][0]
                    test=False
                    x=0
                    while test == False and x<11:
                        try:
                            time.sleep(2)
                            x+=1
                            
                            headers = {'User-Agent' : UserAgents[x]}
                            req = urllib2.Request(url,headers=headers)
                            response = urllib2.urlopen(req)
                            #resp=response.getcode()          # need this??          
                            #print resp
                            
                            html = response.read()
                            test=True
        
                            #print "read html ",test
                        except:
                            print "having a sleep will try again" 
                            time.sleep(5)                  
                            if x==10:
                                test = True
                            x+=1
        
                    regex='countryId=(.+?)\&tradeType'
                    pattern=re.compile(str.encode(regex))
        
                    soup=BeautifulSoup(html)
                    countryList=[]
                    #z=0
                    previous =''
                    # find only links that are countries
                    for link in soup.find_all('a'):
                        if (link.get('href')<>None) and (link.get('title')<>'Show trade for individual states'):
                            if "countryId" in link['href']:
                                row=pattern.findall(link.get('href'))
                                if row <> []:
                                    if row[0].decode("utf-8") <> '0':
                                        if str(row[0].decode("utf-8")) <> previous:
                                            if link.get('lang') is None:
                                                #print row
                                                countryList.append(link.text.encode('ascii','ignore').replace('(+Show States)', '').replace(',', ''))
                                                #print link.text
                                                #countryList.append(str(row[0].decode("utf-8")))
                                                #previous=str(row[0].decode("utf-8"))
                                                #z+=1
                                                #print str(row[0].decode("utf-8"))
        
                    regex=r'\b\d+\b'
                    patternU=re.compile(str.encode(regex))
                    links=soup.find_all('td')
                    y=0   
                    for link in links:
                        if link.get('headers')<> None:
                            if link.get('headers')[1]=="Date1":
                                if len(patternU.findall(link.text))==4:
                                    datablock.append([countryList[int(math.floor(y/2))],hscode[k][:6],hscode[k][6:],str(year)+monthcal(month,link.get('headers')[1]),link.get('headers')[2], patternU.findall(link.text)[0]+patternU.findall(link.text)[1]+patternU.findall(link.text)[2]+patternU.findall(link.text)[3]])
                                elif len(patternU.findall(link.text))==3:
                                    datablock.append([countryList[int(math.floor(y/2))],hscode[k][:6],hscode[k][6:],str(year)+monthcal(month,link.get('headers')[1]),link.get('headers')[2], patternU.findall(link.text)[0]+patternU.findall(link.text)[1]+patternU.findall(link.text)[2]])
                                elif len(patternU.findall(link.text))==2:
                                    datablock.append([countryList[int(math.floor(y/2))],hscode[k][:6],hscode[k][6:],str(year)+monthcal(month,link.get('headers')[1]),link.get('headers')[2], patternU.findall(link.text)[0]+patternU.findall(link.text)[1]])
                                else:
                                    datablock.append([countryList[int(math.floor(y/2))],hscode[k][:6],hscode[k][6:],str(year)+monthcal(month,link.get('headers')[1]),link.get('headers')[2], patternU.findall(link.text)[0]])
                                
                                y+=1
                    Data=pd.DataFrame(datablock)
                    f=open(filename,'a')
                    Data.to_csv(f,header=False)
                    f.close()
    
        # transform output
        dataset=pd.read_csv(filename)
        delete_file(filename)
    
        columnlist=['rank', 'partner_country','hs_code', 'desc', 'Date','Unit','Value']
        
        Data=pd.DataFrame(dataset)
        Data.columns=columnlist
    
        DataQty=Data[Data['Unit']=='Qty']
        DataVal=Data[Data['Unit']=='Val']
        
        merge=pd.merge(DataQty,DataVal[['Date','hs_code','partner_country','Value']],how='outer',on=['Date','hs_code','partner_country'])
    
        index=['Date','hs_code','Product','Partner country','Qty(kgm)','Value(Can$)']
       
        output=pd.DataFrame({'hs_code':merge['hs_code'],'Date':merge['Date'],'Product':merge['desc'],
                             'Partner country':merge['partner_country'],'Qty(kgm)':merge['Value_x'],'Value(Can$)':merge['Value_y']},columns=index)
    
        output.to_csv(dir_path+'statcan_transformed_results.csv', index=False)
        print 'Finished scraping at %s.' % datetime.now()
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['statcan_all_meat_trade'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('monthly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['statcan_all_meat_trade'],[success_msg]]
        save_error_to_log('monthly', msg_list)
   

if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
    
