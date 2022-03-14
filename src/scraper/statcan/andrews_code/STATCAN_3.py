import sys
import requests
from bs4 import BeautifulSoup
import urllib2 
import re
import time
import pandas as pd
import math
import socket
import errno

hscode=[('020110','Bovine carcasses and half carcasses, fresh or chilled'),
    ('020120','Bovine cuts bone in, fresh or chilled'),
    ('020130','Bovine cuts boneless, fresh or chilled'),
    ('020210','Bovine carcasses and half carcasses, frozen'),
    ('020220','Bovine cuts bone in, frozen'),
    ('020230','Bovine cuts boneless, frozen'),
    ('020311','Swine carcasses and half carcasses, fresh or chilled'),
    ('020312','Hams, shoulders and cuts thereof, of swine bone in, fresh or chilled'),
    ('020319','Swine cuts, fresh or chilled, nes'),
    ('020321','Swine carcasses and half carcasses, frozen'),
    ('020322','Hams, shoulders and cuts thereof, of swine, bone in, frozen'),
    ('020329','Swine cuts, frozen, nes'),
    ('020410','Lamb carcasses and half carcasses, fresh or chilled'),
    ('020421','Sheep carcasses and half carcasses, fresh or chilled'),
    ('020422','Sheep cuts, bone in, fresh or chilled'),
    ('020423','Sheep cuts, boneless, fresh or chilled'),
    ('020430','Lamb carcasses and half carcasses, frozen'),
    ('020441','Sheep carcasses and half carcasses, excluding lamb, frozen'),
    ('020442','Sheep cuts, bone in, frozen'),
    ('020443','Sheep cuts, boneless, frozen'),
    ('020450','Goat meat, fresh, chilled or frozen'),
    ('020500','Horse, ass, mule or hinny meat, fresh, chilled or frozen'),
    ('020610','Bovine edible offal, fresh or chilled'),
    ('020621','Bovine tongues, edible offal, frozen'),
    ('020622','Bovine livers, edible offal, frozen'),
    ('020629','Bovine edible offal, frozen, nes'),
    ('020630','Swine edible offal, fresh or chilled'),
    ('020641','Swine livers, edible offal, frozen'),
    ('020649','Swine edible offal, frozen, nes'),
    ('020680','Sheep, goats, asses, mules or hinnies edible offal, fresh or chilled'),
    ('020690','Sheep, goats, asses, mules or hinnies edible offal, frozen'),
    ('020710','Poultry, domestic, whole, fresh or chilled'),
    ('020711','Chickens and capons, whole, fresh or chilled'),
    ('020712','Chickens and capons, whole, frozen'),
    ('020713','Chicken and capon cuts and edible offal, fresh or chilled'),
    ('020714','Chicken and capon cuts and edible offal, frozen'),
    ('020721','Fowls, domestic, whole, frozen'),
    ('020722','Turkeys, domestic, whole, frozen'),
    ('020723','Ducks, geese and guinea fowls, domestic, whole, frozen'),
    ('020724','Turkeys, whole, fresh or chilled'),
    ('020725','Turkeys, whole, frozen'),
    ('020726','Turkey cuts and edible offal, fresh or chilled'),
    ('020727','Turkey, cuts and edible offal, frozen'),
    ('020731','Fatty livers of geese or ducks, domestic fresh or chilled'),
    ('020732','Ducks, geese or guinea fowls, domestic, whole, fresh or chilled'),
    ('020733','Ducks, geese and guinea fowls, domestic, whole, frozen'),
    ('020734','Fatty livers of geese or ducks, domestic, fresh or chilled'),
    ('020735','Ducks,geese/guinea fowl cuts & edible offal, exc fatty livers, fresh or chd'),
    ('020736','Duck, geese or guinea fowl cuts and edible offal, domestic, frozen'),
    ('020739','Poultry cuts and offal, domestic except geese or ducks livers fresh or chilled'),
    ('020741','Meat and edible offal, of domestic ducks, not cut in pieces, fresh or chilled'),
    ('020742','Meat and edible offal, of domestic ducks, not cut in pieces, frozen'),
    ('020743','Fatty livers, of domestic ducks, fresh or chilled'),
    ('020744','Other meat and edible offal, of domestic ducks, fresh or chilled,nes'),
    ('020745','Other meat and edible offal, of domestic ducks, frozen, nes'),
    ('020750','Poultry livers, domestic, frozen'),
    ('020751','Meat & edible offal, of dom geese, not cut in pieces,fresh/chill,o/t fatty liver'),
    ('020752','Meat & edible offal, of domestic geese, not cut in pieces, frozen, o/t liver'),
    ('020753','Fatty livers of domestic geese, fresh or chilled'),
    ('020754','Other meat and edible offal, of dom geese, fresh or chilled,o/t fatty livers,nes'),
    ('020755','Other meat and edible offal, of domestic geese, frozen, nes'),
    ('020760','Meat and edible offal, of domestic guinea fowls, fresh, chilled or frozen'),
    ('020810','Rabbit or hare, meat and edible meat offal, fresh, chilled or frozen'),
    ('020820','Frog legs, fresh, chilled or frozen'),
    ('020830','Meat and edible meat offal, of primates, fresh, chilled or frozen'),
    ('020840','Meat & edbl meat offal,of whale,dolphin,manatee,dugong,seal,etc,fr/chd/frz,nes'),
    ('020850','Meat & edible meat offal,of reptiles, incl snakes & turtles,fresh,chilled/frozen'),
    ('020860','Meat and edible meat offal, of camels and other camelids,fresh,chilled or frozen'),
    ('020890','Other meat and edible meat offal, fresh, chilled or frozen, nes'),
    ('020900','Pig fat lean meat free and poultry fat unrendered,fresh,chilled,frozen/cured'),
    ('020910','Pig fat,lean meat free,n rendered or o/w extrc,fr/chd/frz/sa/in brine/dr/smoked'),
    ('020990','Poultry fat, not rendered or o/w extracted, fr/chd/frz/salted/in brine/dr/smoked'),
    ('021011','Hams, shoulders and cuts thereof, of swine bone in, cured'),
    ('021012','Bellies, streaky and cuts thereof, swine cured'),
    ('021019','Swine meat, cured, nes'),
    ('021020','Bovine meat, cured'),
    ('021090','Meat and edible meat offal cured nes and edible meat or offal, flours & meals'),
    ('021091','Meat and edible meat offal, cured, and flours and meals, of primates'),
    ('021092','Meat&edbl meat offal,sa/in brine/dr/smoked,flours&meals,of whales,dolphins, etc'),
    ('021093','Meat & edible meat offal,cured,and flours & meals,of reptiles,incl snake,turtle'),
    ('021099','Meat and edible meat offal, salted/in brine/dried/smoked,incl flours & meals,nes')]

year=['2014','2013','2012','2011','2010','2009','2008','2007','2006','2005','2004','2002','2001','2000']
month=['12','11','10','9','8','7','6','5','4','3','2','1']
unit=[('Qty','KGM'),('Val','CAN$')]

filename='C:/Users/Andrew/Google Drive/scrape_output/Pig/Trade/statcan/statcan_3_new.csv'
UserAgents = ['Mozilla/5.0 (Windows NT 6.2; rv:22.0) Gecko/20130405 Firefox/22.0','Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'
                       ,'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; Media Center PC 6.0; InfoPath.3; MS-RTC LM 8; Zune 4.7','Mozilla/5.0 (Linux; U; Android 2.3.3; en-us; HTC_DesireS_S510e Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile'
                       ,'Mozilla/5.0 (BlackBerry; U; BlackBerry 9850; en) AppleWebKit/534.11+ (KHTML, like Gecko) Version/7.0.0.254 Mobile Safari/534.11+','Opera/9.80 (J2ME/MIDP; Opera Mini/9 (Compatible; MSIE:9.0; iPhone; BlackBerry9700; AppleWebKit/24.746; U; en) Presto/2.5.25 Version/10.54'
                       ,'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',"Mozilla/5.0 (Windows NT 6.2; Win64; x64;) Gecko/20100101 Firefox/20.0"]


def monthcal(month,datest):
    monthst=''
    if datest =='Date1' :
         monthint=int(month) 
    elif datest =='Date2':
        monthint= int(month)-1
    elif datest=='Date3':
        monthint=int(month)-2
    elif datest == 'Date4':
        monthint=int(month)-3
    if monthint <10:
        return '0' + str(monthint)
    else:
        return str(monthint)
    
    



#restricting urlib to 10 secs
timeout = 10
socket.setdefaulttimeout(timeout)


for k in range(36,len(hscode)):
#for k in range(1,2): #test
    for i in range(0,14): 
        time.sleep(2)
        for j in range(0,12): 
            datablock=[]
#            url='http://www5.statcan.gc.ca/cimt-cicm/topNCountryCommodities-marchandises?countryId=117&tradeType=1&usaState=0&topNDefault=10&freq=6&commodityName=Milk%2C+not+concentrated+and+unsweetened%2C+not+exceeding+1%25+fat&lang=eng&refYr=' + year[i] + '&sectionId=1&monthStr=August&chapterId=4&arrayId=9800000&sectionLabel=I+-+Live+animals+and+animal+products.&provId=1&refMonth=' + month[j] +'&commodityId=' +hscode[k][0]
            url='http://www5.statcan.gc.ca/cimt-cicm/topNCountries-pays?lang=eng&sectionId=1&dataTransformation=0&refYr=' + year[i] + '&refMonth=' + month[j] + '&freq=6&countryId=0&usaState=0&provId=1&retrieve=Retrieve&save=null&country=null&tradeType=1&topNDefault=250&monthStr=null&chapterId=2&arrayId=0&sectionLabel=I%20-%20Live%20animals%20and%20animal%20products.&scaleValue=0&scaleQuantity=0&commodityId=' + hscode[k][0]
            test=False
            x=0
            while test ==False and x<11:
                try:
                    time.sleep(2)
                    x+=1
                    print "trying to get html"
                    print UserAgents[x]
                    
                    headers = {'User-Agent' : UserAgents[x]}
                    req = urllib2.Request(url,headers=headers)
                    response = urllib2.urlopen(req)
                    resp=response.getcode()                    
                    print resp
                    
                    html = response.read()
                    test=True

                    print "read html ",test
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
            z=0
            previous =''
            for link in soup.find_all('a'):
                if link.get('href')<>None:
                    if "countryId" in link['href']:
                        row=pattern.findall(link.get('href'))
                        if row <> []:
                            if row[0].decode("utf-8") <> '0':
                                if str(row[0].decode("utf-8")) <> previous:
                                    countryList.append(str(row[0].decode("utf-8")))
                                    previous=str(row[0].decode("utf-8"))
                                    z+=1
                                    print str(row[0].decode("utf-8"))

            regex=r'\b\d+\b'
            patternU=re.compile(str.encode(regex))
            links=soup.find_all('td')
            y=0   
            for link in links:
                if link.get('headers')<> None:
                    if link.get('headers')[1]=="Date1":
                        if len(patternU.findall(link.text))==4:
                            datablock.append([countryList[int(math.floor(y/2))],hscode[k][0],year[i]+monthcal(month[j],link.get('headers')[1]),link.get('headers')[2], patternU.findall(link.text)[0]+patternU.findall(link.text)[1]+patternU.findall(link.text)[2]+patternU.findall(link.text)[3]])
                        elif len(patternU.findall(link.text))==3:
                            datablock.append([countryList[int(math.floor(y/2))],hscode[k][0],year[i]+monthcal(month[j],link.get('headers')[1]),link.get('headers')[2], patternU.findall(link.text)[0]+patternU.findall(link.text)[1]+patternU.findall(link.text)[2]])
                        elif len(patternU.findall(link.text))==2:
                            datablock.append([countryList[int(math.floor(y/2))],hscode[k][0],year[i]+monthcal(month[j],link.get('headers')[1]),link.get('headers')[2], patternU.findall(link.text)[0]+patternU.findall(link.text)[1]])
                        else:
                            datablock.append([countryList[int(math.floor(y/2))],hscode[k][0],year[i]+monthcal(month[j],link.get('headers')[1]),link.get('headers')[2], patternU.findall(link.text)[0]])
                        print y,countryList[int(math.floor(y/2))],hscode[k][0],year[i]+monthcal(month[j],link.get('headers')[1]),link.get('headers')[2]
                        y+=1
            Data=pd.DataFrame(datablock)
            f=open(filename,'a')
            Data.to_csv(f,header=False)
            f.close()

                    
