'''
Created on 13 May 2016

@author: Suzanne
'''
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from datas.function.function import chunck_list, create_directory
from datas.web.path import WEB_CME_PATH

def scrape():
    print 'Start scraping at %s...' % datetime.now()
    data = []
    url = 'http://www.cmegroup.com/trading/agricultural/grain-and-oilseed/corn_quotes_settlements_futures.html'

    request = requests.get(url)
    page = request.text
    soup = BeautifulSoup(page, "lxml")
    get_tags = soup.findAll(['td', 'th'])
    for each in get_tags:
        if 'Last Updated' in each.text:
            continue
        if each.text=='About This Report':
            continue
        if each.text=='Total':
            break
        else:
            data.append(each.text.replace(',',''))
    
    data_chunked = chunck_list(data, 9)
    dir_path = WEB_CME_PATH + 'corn/'
     
    today = datetime.strftime(datetime.now(), '%Y_%m_%d')
     
    dir_path = create_directory(dir_path,today) 
     
    with open ('%scorn.csv' % (dir_path), 'wb') as file:
        for w in data_chunked:
            file.write(','.join(w))
            file.write('\n')

    print 'Finished scraping at %s.' % datetime.now()

if __name__ == '__main__':
    scrape()
