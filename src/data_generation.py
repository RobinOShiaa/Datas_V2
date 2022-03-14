import pymysql
import pyodbc
import pandas as pd
import pandas.io.sql as pysql
import pandas.tools.pivot as pypivot
import datetime
import sys
import numpy as np
import pyodbc
import time
from datas.db.path import DB_PIG_DATA_PATH

wpath=DB_PIG_DATA_PATH
filename="eu_trade.csv"
sdatabase="Pig_database"

#### MySQL code required to extract relevant information on pig datasets and SQL Server code to extract data from client database

sql_bordbia_pig_price=''.join(["SELECT substr(yearweek(DATE_ADD(DATE, INTERVAL 4 DAY)),1,4) as Year,  ",
    "cast(yearweek(DATE_ADD(DATE, INTERVAL 4 DAY)) as char) as YearWeeknum, ",
    "cast(extract(year_month from date) as char) as YearMonth, ",
    "month(date) as Month, date_format(DATE,'%d/%m/%Y') as Time, ",    
    "AREA,PRICE "                            
    "from raw_db.bordbia_pig_price"])

sql_bordbia_cereal_price=''.join(["SELECT DATE, ",
    "cast(yearweek(DATE_ADD(date, INTERVAL 4 DAY)) as char) as YearWeeknum, ",
    "cast(extract(year_month from date) as char) as YearMonth, ",
    "AREA,PRICE,TYPE,concat(TYPE,AREA) as TYPE_AREA "
    "from raw_db.bordbia_cereal_price"])

sql_slaughter = ''.join([
    "SELECT ",
    "cast(extract(year_month from week_end_date) as char) as YearMonth, ",
    "week_end_date, ",
    "cast(yearweek(DATE_ADD(week_end_date, INTERVAL 4 DAY)) as char) as YearWeeknum, ",
    "member_state,unit,TYPE,slaughter,concat(TYPE,member_state) as TYPE_AREA ",
    "FROM raw_db.bordbia_pig_throughput ",
    "where week_end_date < '2011-01-02' ",
    "union ",
    "Select ",
    "cast(extract(year_month from week_end_date ) as char) as YearMonth,",
    "week_end_date, ",
    "cast(yearweek(DATE_ADD(week_end_date, INTERVAL 4 DAY)) as char) as YearWeeknum, ",
    "member_state, ",
    "unit,TYPE,slaughter, ",
    "concat(if(type='Clean Pigs','Fatterning Pigs',if(type='Cull Sows','Sows Boars','')),member_state) as TYPE_AREA ",
    "FROM raw_db.bpex_weekly_slaughtering ",
    "union ",
    "SELECT ",
    "cast(extract(year_month from week_ending) as char) as YearMonth, ",
    "week_ending as week_end_date, ",
    "cast(yearweek(DATE_ADD(week_ending, INTERVAL 4 DAY)) as char) as YearWeeknum, ",
    "'US' as member_state,'1 head' as unit,'Fatterning Pigs' as TYPE ,value as slaughter,",
    "concat(if(data_item= ",
    "'HOGS- SLAUGHTER- COMMERCIAL- FI - SLAUGHTERED- MEASURED IN HEAD','Fatterning Pigs', ",
    "         if(data_item= 'HOGS- SLAUGHTER- COMMERCIAL- FI - SLAUGHTERED- MEASURED IN LB / HEAD- DRESSED BASIS', ",
    "'Dead_weight','')),'US') as TYPE_AREA  ",
    "FROM raw_db.usda_hog_slaughters ",
    "where geo_level='NATIONAL'"]) 

sql_EU_slaughter = ''.join([
    "SELECT yearmonth as YearMonth,substring(yearmonth,1,4) as year, substring(yearmonth,5,2) as month, ",
    "geo,type,meat_item,unit_ton,value_ton,unit_head,if((value_ton*1000/value_head)<0.2,(value_head/1000),value_head) as value_head, ",
    "concat(type,meat_item,geo) as TYPE_AREA, ",
    "if((value_ton*1000/value_head)<0.2,(value_ton*1000)/(value_head/1000),(value_ton*1000/value_head)) as dead_weight,'AREA 21' as AREA FROM raw_db.eurostat_pig_slaughtering ",
    "where type='pigmeat' and meat_item='Slaughterings' and yearmonth >'199912' ",
    " and geo in ('Austria','Belgium','Croatia','Cyprus','Czech Republic','Denmark','Finland','France','Germany (until 1990 former territory of the FRG)', ",
    "'Greece','Ireland','Italy'," ,
    "'Lithuania','Netherlands','Norway','Poland','Portugal','Romania','Spain','Sweden','United Kingdom') "])

#query to extract all primal codes for export data

sql_vtrade_all_codes=''.join(["SELECT *,yearmonth as YearMonth, ",
    "substring(yearmonth,1,4) as year,substring(yearmonth,5,2) as month, ",
    "substring(product_code,1,4) as pork, substring(product_code,1,6) as primal, ",
    "if(length(product_code) > 6,substring(product_code,1,8),'') as subprimal, ",
    "if (reporter = 'EU', ",
    "   if(substring(yearmonth,1,4) >='2007', ",
    "      if(substring(yearmonth,1,4) <='2009',value*10*rate,value*rate), ",
    "   value*rate), ",
    "value*rate) as  cor_Value, "
    "if (reporter = 'EU', ",
    "  if(substring(yearmonth,1,4) >='2007', ",
    "    if(substring(yearmonth,1,4) <='2009', ",
    "      if(quantity = 0,2.5,quantity*100), ",
    "    quantity), ",
    "  quantity), ",
    "quantity) as cor_weight ",
    "FROM raw_db.vtrade_exp_all_codes ",
    "where reporter<> 'EU' or (reporter ='EU' and length(product_code) > 6) and yearmonth >='201001';"])

#query for exporting just the 0203 data from the trade tables

sql_vtrade_exp_0203=''.join(["SELECT reporter,Partner_Reporter,partner,yearmonth as YearMonth,currency, weight_unit, "
    "sum( ",
    "if (reporter = 'EU', ",
    "   if(substring(yearmonth,1,4) >='2007', ",
    "      if(substring(yearmonth,1,4) <='2009',value*10*rate,value*rate), ",
    "   value*rate), ",
    "value*rate)) as value, ",
    "sum( ",
    "if (reporter = 'EU', ",
    "  if(substring(yearmonth,1,4) >='2007', ",
    "    if(substring(yearmonth,1,4) <='2009', ",
    "      if(quantity = 0,2.5,quantity*100), ",
    "    quantity), ",
    "  quantity), ",
    "quantity)) as quantity ",
    "FROM raw_db.vtrade_exp_0203 " ,
    "where yearmonth >= '201001' ",
    "group by partner_reporter,yearmonth,currency, weight_unit "])

sql_sum_vrtrade__par_0203=''.join(["SELECT yearmonth as YearMonth,partner, ",
    "sum( ",
    "if (reporter = 'EU', ",
    "   if(substring(yearmonth,1,4) >='2007', ",
    "      if(substring(yearmonth,1,4) <='2009',value*10*rate,value*rate), ",
    "   value*rate), ",
    "value*rate)) as tot_val, ",
    "sum( ",
    "if (reporter = 'EU', ",
    "  if(substring(yearmonth,1,4) >='2007', ",
    "    if(substring(yearmonth,1,4) <='2009', ",
    "      if(quantity = 0,2.5,quantity*100), ",
    "    quantity), ",
    "  quantity), ",
    "quantity)) as tot_quan ",
    "FROM raw_db.vtrade_exp_0203 ",
    "where yearmonth >= '201001' ",
    "group by yearmonth,partner "])

sql_sum_vrtrade__rep_0203=''.join(["SELECT yearmonth as YearMonth,reporter, " ,
    "sum( ",
    "if (reporter = 'EU', ",
    "   if(substring(yearmonth,1,4) >='2007', ",
    "      if(substring(yearmonth,1,4) <='2009',value*10*rate,value*rate), ",
    "   value*rate), ",
    "value*rate)) as tot_val, ",
    "sum( ",
    "if (reporter = 'EU', ",
    "  if(substring(yearmonth,1,4) >='2007', ",
    "    if(substring(yearmonth,1,4) <='2009', ",
    "      if(quantity = 0,2.5,quantity*100), ",
    "    quantity), ",
    "  quantity), ",
    "quantity)) as tot_quan ",
    "FROM raw_db.vtrade_exp_0203 ",
    "where yearmonth >= '201001' ",
    "group by yearmonth,reporter "])


sql_imf_currency=''.join([
    "SELECT cast(yearweek(DATE_ADD(date, INTERVAL 4 DAY)) as char) as YearWeeknum,",
    "year(date) as Year,weekofyear(date) as Weeknum,currency,avg(rate) as rate FROM raw_db.imf_currency ",
    "where currency in ('U.S. dollar(USD)','Brazilian real(BRL)','Canadian dollar(CAD)','Chinese yuan(CNY)','Danish krone(DKK)',",
    "'euro(EUR)','Japanese yen(JPY)','PHILIPPINE PESO(PHP)','Russian ruble(RUB)','Polish zloty(PLN)','Singapore dollar(SGD)',",
    "'South African rand(ZAR)','U.K. pound sterling(GBP)','Australian dollar(AUD)') "
    "group by year(date),weekofyear(date),currency"])

sql_imf_currency_mon=''.join([
    "SELECT if(month(date)<10,concat(year(date),concat('0',month(date))),concat(year(date),month(date))) as YearMonth,",
    "year(date) as Year,month(date) as Month,currency_original,avg(rate) as rate FROM raw_db.imf_currency ",
    "where currency_original in ('U.S. dollar(USD)','Brazilian real(BRL)','Canadian dollar(CAD)','Chinese yuan(CNY)','Danish krone(DKK)',",
    "'euro(EUR)','Japanese yen(JPY)','PHILIPPINE PESO(PHP)','Russian ruble(RUB)','Polish zloty(PLN)','Singapore dollar(SGD)',",
    "'South African rand(ZAR)','U.K. pound sterling(GBP)','Australian dollar(AUD)') "
    "group by year(date),month(date),currency_original"])

#### Open connection to database and extract data into dataframe

conn = pymysql.connect(user='sue', password='123piggy',host='136.206.48.152',database='raw_db')

df_bord_bia_price = pysql.read_sql(sql_bordbia_pig_price, conn)
df_bordbia_cereal_price = pysql.read_sql(sql_bordbia_cereal_price, conn)
df_slaughter= pysql.read_sql(sql_slaughter, conn)
df_EU_slaughter=pysql.read_sql(sql_EU_slaughter,conn)
df_US_slaughter=df_slaughter.loc[(df_slaughter['member_state'] == 'US')]
df_vtrade_all_codes = pysql.read_sql(sql_vtrade_all_codes, conn)
df_vtrade_exp_0203 = pysql.read_sql(sql_vtrade_exp_0203, conn)
df_sum_vtrade_par_0203 = pysql.read_sql(sql_sum_vrtrade__par_0203, conn)
df_sum_vtrade_rep_0203 = pysql.read_sql(sql_sum_vrtrade__rep_0203, conn)
df_imf_currency=pysql.read_sql(sql_imf_currency, conn)
df_imf_currency_mon=pysql.read_sql(sql_imf_currency_mon, conn)

conn.close()



#### Pivot the tables to create columns for each  table

table_BBP=pypivot.pivot_table(df_bord_bia_price,values='PRICE',columns=['AREA'],index=['Year','YearWeeknum','YearMonth','Month','Time'])
table_BBP['TimeRow']=range(1,len(table_BBP)+1)

table_BBCP=pypivot.pivot_table(df_bordbia_cereal_price,values='PRICE',columns=['TYPE_AREA'],index=['YearWeeknum'])

table_EU_slaughterYear = pypivot.pivot_table(df_EU_slaughter,values='value_head',columns=['AREA'],index=['year','geo'])
table_EU_slaughterPkg = pypivot.pivot_table(df_EU_slaughter,values='value_ton',columns=['AREA'],index=['YearMonth'],aggfunc=np.sum)
table_EU_slaughterPhd = pypivot.pivot_table(df_EU_slaughter,values='value_head',columns=['AREA'],index=['YearMonth'],aggfunc=np.sum)
table_EU_slaughterP=pd.merge(table_EU_slaughterPkg,table_EU_slaughterPhd,left_index=True,right_index=True,how ='outer')	
table_EU_slaughterP=table_EU_slaughterP.rename(columns={'AREA 21_x' : 'EUProdkg','AREA 21_y' : 'EUProdhd'})
table_EU_slaughterP['EUDead_Weightkg'] = table_EU_slaughterP['EUProdkg']*1000/table_EU_slaughterP['EUProdhd']

table_slaughterP=pypivot.pivot_table(df_slaughter,values='slaughter',columns=['TYPE_AREA'],index=['YearWeeknum'],aggfunc=np.sum)
table_US_slaughter=pypivot.pivot_table(df_US_slaughter,values='slaughter',columns=['TYPE_AREA'],index=['YearWeeknum','YearMonth'],aggfunc=np.sum)

table_trade203P=pypivot.pivot_table(df_vtrade_exp_0203,values=['value','quantity'],columns=['Partner_Reporter'],index=['YearMonth'])
table_sum_PAR203P=pypivot.pivot_table(df_sum_vtrade_par_0203,values=['tot_val','tot_quan'],columns=['partner'],index=['YearMonth'])
table_sum_REP203P=pypivot.pivot_table(df_sum_vtrade_rep_0203,values=['tot_val','tot_quan'],columns=['reporter'],index=['YearMonth'])

table_imf_monP=pypivot.pivot_table(df_imf_currency_mon,values=['rate'],columns=['currency_original'],index=['YearMonth'])


#### Set up tables

table_BBP=table_BBP.rename(columns={'Brazil':'BrazCent', 'Netherlands':'NetCent','EU':'EUCent', 'Ireland':'IreCent','Denmark':'DenCent','France':'FranCent','Germany':'GerCent',
    'United Kingdom':'UKCent','Great Britain':'GBCent','USA':'UsHogCent'})

table_BBP=table_BBP.drop(['Austria', 'Belgium', 'Finland', 'Greece', 'Italy', 'Luxemburg', 'Northern Ireland', 'Poland', 'Portugal', 'Spain', 'Sweden'],axis=1)
table_BBP=table_BBP[['TimeRow','IreCent','DenCent','FranCent','GerCent','NetCent','EUCent','UKCent','GBCent','UsHogCent','BrazCent']]



table_BBCP=table_BBCP.rename(columns={'Canadian ( Thunderbay ) BarleyWorld':'CanBar',
                                      'Feed BarleyFrance':'FranBar',
                                      'Feed BarleyGermany':'GerFeedBar',
                                      'Feed WheatGermany':'GerFeedWh',
                                      'Milling WheatFrance':'FranMill',
                                      'Milling WheatGermany':'GerWheat',
                                      'RapeseedGermany':'GerRape',
                                      'US Maize No.3 yellowWorld':'UsMaize',
                                      'US Soft Red Winter WheatWorld':'UsSoftRed',
                                      'US Soyabeans No.2 yellowWorld':'UsSoyabeans'})


table_slaughterP['DenKill']=table_slaughterP['Total PigsDenmark'].fillna(0)+table_slaughterP['Fatterning PigsDenmark'].fillna(0)
table_slaughterP['NetKill']=table_slaughterP['Total PigsNetherlands'].fillna(0)+table_slaughterP['Fatterning PigsNetherlands'].fillna(0)
table_slaughterP['SowKillIRE']=table_slaughterP['Sows BoarsIreland'].fillna(0)+table_slaughterP['Sows BoarsNorthern Ireland'].fillna(0)

table_slaughterP=table_slaughterP.rename(columns={'Fatterning PigsGermany' : 'GerKill',
                                      'Fatterning PigsGreat Britain' : 'GBKill',
                                      'Fatterning PigsIreland' : 'IrishKill',
                                      'Fatterning PigsNorthern Ireland' : 'NIKill',
                                      'Fatterning PigsUS'  : 'USKill',
                                      'Sows BoarsGermany' : 'SowKillGer',
                                      'Sows BoarsGreat Britain' : 'SowKillGB',
                                      'Dead_weightUS' : 'USDeadWeight'})


table_slaughterP=table_slaughterP[['GerKill','GBKill','IrishKill','NIKill','DenKill','NetKill','USKill',
                                 'SowKillGer','SowKillIRE','SowKillGB','USDeadWeight']]



#### Get proper dead weight for the US slaughter figures

table_US_slaughter=table_US_slaughter.rename(columns={'Fatterning PigsUS' : 'USProdhd',
                                                              'Dead_weightUS' : 'USDeadWeight'})
table_US_slaughter['USProdkg']=table_US_slaughter['USDeadWeight']*table_US_slaughter['USProdhd']/2.2046
t=table_US_slaughter.reset_index()
t=pd.melt(t,id_vars=['YearMonth'],value_vars=['USDeadWeight','USProdhd','USProdkg'])
table_US_slaughter=pypivot.pivot_table(t,values='value',columns=['TYPE_AREA'],index=['YearMonth'],aggfunc=np.sum)
table_US_slaughter['USDeadWeight']=table_US_slaughter['USProdkg']/table_US_slaughter['USProdhd']

#### Set up Imf currency table

cur_list=['Canadian dollar(CAD)','U.S. dollar(USD)','euro(EUR)','Australian dollar(AUD)','Chinese yuan(CNY)','Danish krone(DKK)','U.K. pound sterling(GBP)']

table_imf_monP_mon=table_imf_monP['rate'][cur_list]
table_imf_monP=table_imf_monP.rename(columns={'Canadian dollar(CAD)' : 'CAD',
                           'U.S. dollar(USD)' : 'USD',
                           'euro(EUR)' : 'EUR',
                           'Australian dollar(AUD)':'AUD',
                           'Chinese yuan(CNY)' : 'CNY',
                           'Danish krone(DKK)' : 'DKK',
                           'U.K. pound sterling(GBP)' : 'GBP'})

table_imf_monP=table_imf_monP['rate'][['CAD','USD','EUR','AUD','CNY','DKK','GBP']]


### setting up the trade table

old_list=['Australia','Canada','China','Hong Kong','Japan','Korea','Mexico','Russia','Ukraine','United States']
new_list=['Angola','Mexico','Canada','Chile','Philippines','Singapore', 'Australia','China','Hong Kong','Japan','Korea','Russia','Ukraine','United States']
rep_list=['Australia', 'Brazil', 'Canada', 'EU', 'US']

df=table_sum_PAR203P['tot_quan'][new_list]
df['YearMonth']=df.index
df['EUMarAvaiKg']=df.sum(axis=1)
df['EUMarAvaiKg']=df['EUMarAvaiKg']-df['Mexico']
df['USMarAvaiKg']=df['EUMarAvaiKg']-df['United States']
df['CNMarAvaiKg']=df['EUMarAvaiKg']-df['Canada']


df2=table_sum_PAR203P['tot_val'][new_list]
df['availEuro']=df2.sum(axis=1)
df['availEuro']=df['availEuro']-df['Mexico']
df['availUS']= df['availEuro']-df2['United States']
df['availCN']= df['availEuro']-df2['Canada']
df['RussiaEuro']=df2['Russia']

df3=table_sum_PAR203P['tot_quan'][old_list]
df['YearMonth']=df.index
df['EUMarAvaiKgO']=df3.sum(axis=1)
df['EUMarAvaiKgO']=df['EUMarAvaiKgO']-df['Mexico']
df['USMarAvaiKgO']=df['EUMarAvaiKgO']-df3['United States']
df['CNMarAvaiKgO']=df['EUMarAvaiKgO']-df3['Canada']


df4=table_sum_PAR203P['tot_val'][old_list]
df['availEuroO']=df4.sum(axis=1)
df['availEuroO']=df['availEuroO']-df['Mexico']
df['availUSO']= df['availEuroO']-df4['United States']
df['availCNO']= df['availEuroO']-df4['Canada']



### Market access. Remove countries that are restricting eg russia from the 201401 
##EU

df.loc[(df['YearMonth']>='201401'),'EUMarAvaiKg']=df['EUMarAvaiKg']-df['Russia']
df.loc[(df['YearMonth']>='201401'),'availEuro']=df['availEuro']-df['RussiaEuro']
#old_list
df.loc[(df['YearMonth']>='201401'),'EUMarAvaiKgO']=df['EUMarAvaiKgO']-df['Russia']
df.loc[(df['YearMonth']>='201401'),'availEuroO']=df['availEuroO']-df['RussiaEuro']

##US

df.loc[(df['YearMonth']>='201303') & (df['YearMonth']<='201402'),'USMarAvaiKg']=df['USMarAvaiKg']-df['Russia']
df.loc[(df['YearMonth']>='201303') & (df['YearMonth']<='201402'),'availUS']=df['availUS']-df['RussiaEuro']
df.loc[(df['YearMonth']>='201409') ,'USMarAvaiKg']=df['USMarAvaiKg']-df['Russia']
df.loc[(df['YearMonth']>='201409') ,'availUS']=df['availUS']-df['RussiaEuro']

#old_list
df.loc[(df['YearMonth']>='201303') & (df['YearMonth']<='201402'),'USMarAvaiKgO']=df['USMarAvaiKgO']-df['Russia']
df.loc[(df['YearMonth']>='201303') & (df['YearMonth']<='201402'),'availUSO']=df['availUSO']-df['RussiaEuro']
df.loc[(df['YearMonth']>='201409') ,'USMarAvaiKgO']=df['USMarAvaiKgO']-df['Russia']
df.loc[(df['YearMonth']>='201409') ,'availUSO']=df['availUSO']-df['RussiaEuro']


## Canada
df.loc[(df['YearMonth']>='201409'),'CNMarAvaiKg']=df['CNMarAvaiKg']-df['Russia']
df.loc[(df['YearMonth']>='201409'),'availCN']=df['availCN']-df['RussiaEuro']

#old_list
df.loc[(df['YearMonth']>='201409'),'CNMarAvaiKgO']=df['CNMarAvaiKgO']-df['Russia']
df.loc[(df['YearMonth']>='201409'),'availCNO']=df['availCNO']-df['RussiaEuro']

## Caclulating Prices

df['EUPricePKg']=df['availEuro']/(df['EUMarAvaiKg']*1000)
df['USPricePKg']=df['availUS']/(df['CNMarAvaiKg']*1000)
df['CNPricePKg']=df['availCN']/(df['CNMarAvaiKg']*1000)

#### Calculating reporters exports tonnage
print rep_list
print table_sum_REP203P.columns
dfExKg=table_sum_REP203P['tot_quan'][rep_list]
print dfExKg.columns

dfExKg=dfExKg.rename(columns={'Australia' : 'AusKg','Brazil' : 'BrazilKg','Canada' : 'Canadakg', 'EU' : 'EUKg', 'US' : 'USKg'})
dfExKg['ReporterKg']=dfExKg.sum(axis=1)

### Calculating reporters Values SSD
dfExSSD=table_sum_REP203P['tot_val'][rep_list]
dfExSSD=dfExSSD.rename(columns={'Australia' : 'AusEuro','Brazil' : 'BrazilEuro','Canada' : 'CanadaEuro', 'EU' : 'EUEuro', 'US' : 'USEuro'})
dfExSSD['ReporterV']=dfExSSD.sum(axis=1)



#### Merging tables to produce dataframe that can be used for Datatransform 
					
join1=pd.merge(table_BBP,table_BBCP,left_index=True,right_index=True,how ='outer')				
join2=pd.merge(join1,table_slaughterP,left_index=True,right_index=True,how ='outer')
join3=pd.merge(join2,table_imf_monP,left_index=True,right_index=True,how ='outer')
join4=pd.merge(join3,df,left_index=True,right_index=True,how ='outer')
join4b=pd.merge(join4,dfExKg,left_index=True,right_index=True,how ='outer')
join4c=pd.merge(join4b,dfExSSD,left_index=True,right_index=True,how ='outer')
join4d=pd.merge(join4c,table_EU_slaughterP,left_index=True,right_index=True,how ='outer')
join5=pd.merge(join4d,table_US_slaughter,left_index=True,right_index=True,how ='outer')


EUR=pd.DataFrame(table_imf_monP['EUR'])

df_vtrade_all_codes.index=df_vtrade_all_codes['YearMonth']
df_vtrade_all_codes=pd.merge(df_vtrade_all_codes,EUR,left_index=True,right_index=True,how ='left')
df_vtrade_all_codes['cor_Value']=df_vtrade_all_codes['cor_Value']/df_vtrade_all_codes['EUR']
df_vtrade_all_codes['ParRepYM']=df_vtrade_all_codes.apply(lambda x: '%s - %s' % (x['Partner_Reporter'],x['YearMonth']),axis=1)



#### Setting up the exports for vtrade

table_vtrade_all_codesExportKg=pypivot.pivot_table(df_vtrade_all_codes,values=['quantity'],columns='reporter',
                                             index=['YearMonth'],aggfunc=np.sum)
table_vtrade_all_codesExportKg=table_vtrade_all_codesExportKg['quantity']


table_vtrade_all_codesImportKg=pypivot.pivot_table(df_vtrade_all_codes,values=['quantity'],columns='partner',
                                             index=['YearMonth'],aggfunc=np.sum)


#,'partner','Partner_Reporter','ParRepYM'

table_vtrade_all_codesImportKg=table_vtrade_all_codesImportKg['quantity']

table_vtrade_all_codesKg=pd.merge(table_vtrade_all_codesImportKg,table_vtrade_all_codesExportKg,left_index=True,
                                  right_index=True,how ='left')

#table_vtrade_all_codesKg['TotAvail']=table_vtrade_all_codesKg.sum(axis=1)
#

df_vtrade_all_codes=df_vtrade_all_codes.drop('YearMonth',1)

#### Convert all currency variables to EURO's

join5['EUPricePKg']=join5['EUPricePKg']/join5['EUR']
join5['availEuro']=join5['availEuro']/join5['EUR']
join5['USPricePKg']=join5['USPricePKg']/join5['EUR']
join5['availUS']=join5['availUS']/join5['EUR']
join5['CNPricePKg']=join5['CNPricePKg']/join5['EUR']
join5['availCN']=join5['availCN']/join5['EUR']
join5['EUavailRatio']=join5['EUMarAvaiKg']/(join5['EUProdkg']*1000)
join5['USavailRatio']=join5['USMarAvaiKg']*1000/join5['USProdkg']
# old_list
join5['EUavailRatioO']=join5['EUMarAvaiKgO']/(join5['EUProdkg']*1000)
join5['USavailRatioO']=join5['USMarAvaiKgO']*1000/join5['USProdkg']

join5=join5.replace(0,np.nan) # replace columns with ZERO's with missing values
join5=join5.drop('YearMonth',1)

#### Output to csv files for qlik sense

df_bord_bia_price.to_csv(wpath + '/bord_bia_price.csv',index_label='Row' )
df_bordbia_cereal_price.to_csv(wpath + '/bordbia_cereal_price.csv')
df_slaughter=df_slaughter.to_csv(wpath + '/slaughter.csv' ,index_label='Rows')
table_slaughterP.to_csv(wpath + '/table_slaughter.csv' ,index_label='Rows')
df_EU_slaughter.to_csv(wpath + '/EU_slaughter.csv',index_label='Rowd' )
table_EU_slaughterP.to_csv(wpath + '/table_EU_slaughter.csv',index_label='Rowe' )

df_vtrade_all_codes.to_csv(wpath + '/vtrade_all_codes.csv',index_label='Time Row' )

table_vtrade_all_codesKg.to_csv(wpath + '/table_vtrade_all_codesKg.csv')

df_vtrade_exp_0203.to_csv(wpath + '/vtrade_exp_0203.csv' )
df_sum_vtrade_par_0203.to_csv(wpath + '/vtrade_par_0203.csv' )
df_sum_vtrade_rep_0203.to_csv(wpath + '/vtrade_rep_0203.csv' )

df_imf_currency.to_csv(wpath + '/imf_currency.csv' )
df_imf_currency_mon.to_csv(wpath + '/imf_currency_mon.csv' )

join5.to_csv(wpath+filename)
join5=join5.reset_index()
eu_trade_test2=join5.loc[(join5['YearMonth']>='200701')]
#eu_trade_test2=eu_trade_test2.loc[(eu_trade_test2['YearWeeknum']<='201438')]
eu_trade_test2.to_csv(wpath + '/eu_trade_test2.csv',index_label='Row')
print 'finished'





