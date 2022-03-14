'''
Created on 26 Feb 2015

@author: Suzanne
'''
# statcan_transform transforms the scrap from statcan_3.py which scrapes the statcan website.
# The results from statcan_3.py are outputted to statcan_3_new.csv. These are then transformed to the directory of the day
# in C:/Users/Andrew/Google Drive/scrape_output/Pig/Trade/statcan/all 02s FAO Andrew/todaysdate as statcan_results.csv

import sys
import re
import time
import pandas as pd
import os
import csv
from datas.web.scraper import create_directory
from datetime import datetime

strdate=str(datetime.now().date())
strtime=str(datetime.now().time())
'''
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

country=    [("542","Afghanistan"),
    ("242","Albania"),
    ("443","Algeria"),
    ("667","American Samoa"),
    ("156","Andorra"),
    ("446","Angola"),
    ("830","Anguilla"),
    ("832","Antigua and Barbuda"),
    ("744","Argentina"),
    ("280","Armenia"),
    ("877","Aruba"),
    ("614","Australia"),
    ("143","Austria"),
    ("281","Azerbaijan"),
    ("813","Bahamas"),
    ("313","Bahrain"),
    ("512","Bangladesh"),
    ("822","Barbados"),
    ("285","Belarus"),
    ("144","Belgium"),
    ("817","Belize"),
    ("455","Benin"),
    ("815","Bermuda"),
    ("747","Bolivia"),
    ("278","Bosnia and Herzegovina"),
    ("752","Brazil"),
    ("434","British Indian Ocean Territory"),
    ("525","Brunei Darussalam"),
    ("245","Bulgaria"),
    ("457","Burkina Faso"),
    ("548","Cambodia"),
    ("447","Cameroon"),
    ("477","Cape Verde"),
    ("825","Cayman Islands"),
    ("450","Central African Republic"),
    ("451","Chad"),
    ("755","Chile"),
    ("553","China"),
    ("615","Christmas Island"),
    ("610","Cocos (Keeling) Islands"),
    ("758","Colombia"),
    ("460","Comoros"),
    ("452","Congo"),
    ("449","Congo, Democratic Republic"),
    ("621","Cook Islands"),
    ("845","Costa Rica"),
    ("290","Croatia"),
    ("848","Cuba"),
    ("870","Curacao"),
    ("316","Cyprus"),
    ("247","Czech Republic"),
    ("246","Czechoslovakia"),
    ("149","Denmark"),
    ("459","Djibouti"),
    ("833","Dominica"),
    ("855","Dominican Republic"),
    ("763","Ecuador"),
    ("385","Egypt"),
    ("857","El Salvador"),
    ("480","Equatorial Guinea"),
    ("345","Eritrea"),
    ("282","Estonia"),
    ("344","Ethiopia"),
    ("150","Faeroe Islands"),
    ("719","Falkland Islands (Malvinas)"),
    ("617","Fiji"),
    ("153","Finland"),
    ("287","Former USSR"),
    ("154","France"),
    ("654","French Polynesia"),
    ("461","French Southern Territories"),
    ("463","Gabon"),
    ("413","Gambia"),
    ("291","Georgia"),
    ("155","Germany"),
    ("258","Germany, East"),
    ("414","Ghana"),
    ("115","Gibraltar"),
    ("159","Greece"),
    ("3","Greenland"),
    ("834","Grenada"),
    ("862","Guadeloupe"),
    ("666","Guam"),
    ("864","Guatemala"),
    ("465","Guinea"),
    ("716","Guyana"),
    ("867","Haiti"),
    ("616","Heard Is. and McDonald Islands"),
    ("869","Honduras"),
    ("516","Hong Kong"),
    ("262","Hungary"),
    ("163","Iceland"),
    ("519","India"),
    ("556","Indonesia"),
    ("347","Iran"),
    ("352","Iraq"),
    ("117","Ireland"),
    ("355","Israel"),
    ("167","Italy"),
    ("466","Ivory Coast"),
    ("824","Jamaica"),
    ("559","Japan"),
    ("358","Jordan"),
    ("292","Kazakhstan"),
    ("415","Kenya"),
    ("625","Kiribati"),
    ("563","Korea, North"),
    ("564","Korea, South"),
    ("359","Kuwait"),
    ("293","Kyrgyzstan"),
    ("283","Latvia"),
    ("363","Lebanon"),
    ("468","Liberia"),
    ("366","Libya"),
    ("284","Lithuania"),
    ("170","Luxembourg"),
    ("575","Macao"),
    ("276","Macedonia (FYROM)"),
    ("469","Madagascar"),
    ("416","Malawi"),
    ("524","Malaysia"),
    ("453","Mali"),
    ("119","Malta"),
    ("863","Martinique"),
    ("417","Mauritius"),
    ("874","Mexico"),
    ("294","Moldova, Republic of"),
    ("552","Mongolia"),
    ("275","Montenegro"),
    ("829","Montserrat"),
    ("473","Morocco"),
    ("476","Mozambique"),
    ("545","Myanmar"),
    ("420","Namibia"),
    ("611","Nauru"),
    ("565","Nepal"),
    ("173","Netherlands"),
    ("876","Netherlands Antilles"),
    ("653","New Caledonia"),
    ("622","New Zealand"),
    ("879","Nicaragua"),
    ("454","Niger"),
    ("418","Nigeria"),
    ("176","Norway"),
    ("527","Pakistan"),
    ("883","Panama"),
    ("613","Papua New Guinea"),
    ("769","Paraguay"),
    ("774","Peru"),
    ("567","Philippines"),
    ("626","Pitcairn"),
    ("277","Poland"),
    ("178","Portugal"),
    ("886","Puerto Rico"),
    ("323","Qatar"),
    ("279","Romania"),
    ("295","Russian Federation"),
    ("456","Rwanda"),
    ("433","Saint Helena"),
    ("831","Saint Kitts and Nevis"),
    ("835","Saint Lucia"),
    ("6","Saint Pierre and Miquelon"),
    ("836","Saint Vincent &amp; the Grenadines"),
    ("478","Sao Tome and Principe"),
    ("369","Saudi Arabia"),
    ("482","Senegal"),
    ("274","Serbia"),
    ("288","Serbia and Montenegro"),
    ("435","Seychelles"),
    ("423","Sierra Leone"),
    ("528","Singapore"),
    ("871","Sint Maarten"),
    ("248","Slovakia"),
    ("289","Slovenia"),
    ("623","Solomon Islands"),
    ("374","Somalia"),
    ("419","South Africa"),
    ("182","Spain"),
    ("513","Sri Lanka"),
    ("377","Sudan"),
    ("777","Suriname"),
    ("432","Swaziland"),
    ("185","Sweden"),
    ("186","Switzerland"),
    ("379","Syria"),
    ("578","Taiwan"),
    ("296","Tajikistan"),
    ("425","Tanzania, United Republic of"),
    ("583","Thailand"),
    ("486","Togo"),
    ("627","Tonga"),
    ("828","Trinidad and Tobago"),
    ("487","Tunisia"),
    ("382","Turkey"),
    ("297","Turkmenistan"),
    ("827","Turks and Caicos Islands"),
    ("668","U.S. Minor Outlying Islands"),
    ("426","Uganda"),
    ("286","Ukraine"),
    ("328","United Arab Emirates"),
    ("101","United Kingdom"),
    ("9","United States"),
    ("782","Uruguay"),
    ("298","Uzbekistan"),
    ("785","Venezuela"),
    ("586","Viet Nam"),
    ("823","Virgin Islands, British"),
    ("887","Virgin Islands, U.S."),
    ("651","Wallis and Futuna"),
    ("999","World"),
    ("428","Zambia"),
    ("422","Zimbabwe")]


#infile='C:/Users/Andrew/Google Drive/scrape_output/Pig/Trade/statcan/statcan_3_new.csv'
#datablock=pd.read_csv(infile)


infile1='C:/Users/suzanne/Google Drive/scrape_output/Pig/Trade/statcan/statcan_1_new.csv'
infile2='C:/Users/suzanne/Google Drive/scrape_output/Pig/Trade/statcan/statcan_2_new.csv'

datablock1=pd.read_csv(infile1)

datablock2=pd.read_csv(infile2)


datablock=datablock1.append(datablock2)
'''
from datas.web.path import WEB_STATCAN_PATH
infile = '%sall_dairy//statcan.csv' % WEB_STATCAN_PATH
datablock=pd.read_csv(infile)

columnlist=['rank', 'partner_country','hs_code', 'desc', 'Date','Unit','Value']
# country_list=['CountryId','Partner country']
# HS_list=['hs_code','Product']
# countryDf=pd.DataFrame(country)
# countryDf.columns=country_list
# countryDf['CountryId']=countryDf['CountryId'].apply(int)
# countryDf['Partner country']=countryDf['Partner country'].str.replace(',','')
# 
# 
# 
# HS_CodeDf=pd.DataFrame(hscode)
# HS_CodeDf.columns=HS_list
# HS_CodeDf['hs_code']=HS_CodeDf['hs_code'].apply(int)
# HS_CodeDf['Product']=HS_CodeDf['Product'].str.replace(',','')

Data=pd.DataFrame(datablock)
#print Data
Data.columns=columnlist
#print Data
DataQty=Data[Data['Unit']=='Qty']

DataVal=Data[Data['Unit']=='Val']

merge=pd.merge(DataQty,DataVal[['Date','hs_code','partner_country','Value']],how='outer',on=['Date','hs_code','partner_country'])
#print merge
# merge2=pd.merge(merge,countryDf,on='CountryId')
# merge3=pd.merge(merge2,HS_CodeDf,on='hs_code')
index=['Date','hs_code','Product','Partner country','Qty(kgm)','Value(Can$)']
# output=pd.DataFrame({'hs_code':merge['hs_code'],'Date':merge['Date'],'Product':merge3['Product'],
#                      'Partner country':merge2['Partner country'],'Qty(kgm)':merge['Value_x'],'Value(Can$)':merge['Value_y']},columns=index)

output=pd.DataFrame({'hs_code':merge['hs_code'],'Date':merge['Date'],'Product':merge['desc'],
                     'Partner country':merge['partner_country'],'Qty(kgm)':merge['Value_x'],'Value(Can$)':merge['Value_y']},columns=index)

today = datetime.strftime(datetime.now(), '%Y_%m_%d')
dir = create_directory('%sall_dairy' % WEB_STATCAN_PATH, today)
output.to_csv(dir+'statcan_transformed_results.csv')
# if os.path.exists('C:/Users/suzanne/Google Drive/scrape_output/Pig/Trade/statcan/all 02s FAO Andrew/'
#               + strdate[0:4] + '_' + strdate[5:7] + '_' + strdate[8:10] +  '/') ==True:                
#     output.to_csv('C:/Users/suzanne/Google Drive/scrape_output/Pig/Trade/statcan/all 02s FAO Andrew/'
#               + strdate[0:4] + '_' + strdate[5:7] + '_' + strdate[8:10] +  '/statcan_results' + strtime[0:2]+strtime[3:5]+strtime[6:8]
#                 + '.csv' ,sep=',',index=False,encoding='utf-8') #
# else:
#     print 'Directory does not exist'
