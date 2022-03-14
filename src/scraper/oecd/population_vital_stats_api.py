'''
Created on 13 Apr 2016

@author: Conor O'Sullivan
Abandoned
'''
import pandas as pd
import json
from datas.web.scraper import WebScraper
api_url = 'http://stats.oecd.org/SDMX-JSON/data/ALFS_POP_VITAL/AUS+AUT+BEL+CAN+CHL+CZE+DNK+EST+FIN+FRA+DEU+GRC+HUN+ISL+IRL+ISR+ITA+JPN+KOR+LUX+MEX+NLD+NZL+NOR+POL+PRT+SVK+SVN+ESP+SWE+CHE+TUR+GBR+USA+BRA+CHN+COL+IND+IDN+RUS+ZAF.YP+YPTTTTL1_ST+YPTTTTL1_GY+YPFETTL1_ST+YPMATTL1_ST+YV+YVPO01L1_ST+YVPOI1L1_ST+YVPOBIL1_ST+YVPODEL1_ST+YVPOI2L1_ST+YVPOMIL1_ST+YVPOSAL1_ST+YVPO12L1_ST+YVPOI3R1_ST+YVPOBIR1_ST+YVPODER1_ST+YVPOI2R1_ST+YVPOMIR1_ST.A/all?startTime=1995&endTime=2015&dimensionAtObservation=allDimensions&pid=c31f285c-dc9e-44c3-8497-d7ba620334c1'

scraper = WebScraper('urllib2')
response = scraper.open(api_url)

data= json.load(response)

print data['structure']['dimensions']['observation'][0]['values']

#df= pd.read_json(data['structure']['dimensions']['observation'][1]['values'])
#print df

country_df = pd.DataFrame(data['structure']['dimensions']['observation'][0]['values'])
category_df = pd.DataFrame(data['structure']['dimensions']['observation'][1]['values'])
print  pd.DataFrame(data['structure']['dimensions']['observation'][3]['values'])
print country_df
#for dct in data['structure']['dimensions']['observation'][1]['values']:
data_values = data['dataSets'][0]['observations']
values_list = []
keys_list = []
for dct in data_values:
    values_list.append(data_values[dct][0])
    keys_list.append(dct)
    
data_df = pd.DataFrame({'keys':keys_list,'values':values_list})
key_series = data_df['keys'].str.split(' ').apply(pd.Series, 1).stack()
key_series.name = 'key_index'
key_series.index = key_series.index.droplevel(-1) 
data_df = data_df.join(key_series.apply(lambda x: pd.Series(x.split(':'))))
data_df.to_csv('population_vital_stats.csv')
