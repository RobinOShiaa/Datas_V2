'''
Created on 19 Nov 2014

@author: Wenchong

28/01/2015(Wenchong): Updated to get ids for both exports and imports

'''


import re
import time
from datas.function.function import create_directory
from datas.web.path import WEB_USDA_PATH
from datas.web.scraper import WebScraper


def scrape():
    url = 'http://apps.fas.usda.gov/gats/ExpressQuery1.aspx'
    
    wscraper = WebScraper('Chrome')
    wscraper.open(url)
    
    wscraper.click_button('id','ctl00_ContentPlaceHolder1_lbExpressQuery')
    time.sleep(2)
    
    # flow ids in the web page and labels
    flows = {'X':'exports', 'G':'imports'}
    for flow_id in flows:
        # select flow type
        wscraper.load_field('select', 'name', 'ctl00$ContentPlaceHolder1$ddlProductType', flow_id)
        time.sleep(4)
        
        # search code 0203
        wscraper.load_field('select','name','ctl00$ContentPlaceHolder1$ddlProductSearch', 'Code')
        wscraper.load_field( 'input','name','ctl00$ContentPlaceHolder1$txtProductSearch', '0203')
        wscraper.click_button('id','ctl00_ContentPlaceHolder1_btnProductSearch')
        time.sleep(2)
        
        # get ids and lables of products
        dropdown_texts = wscraper.get_dropdown_list('id','ctl00_ContentPlaceHolder1_lb_Products', 'text')
        
        dropdown_texts = [d.strip(' ') for d in dropdown_texts]
        dropdown_texts = [d.split(' - ') for d in dropdown_texts if re.match('^\d+', d)]
        
        # insert id and label of the parent catalogue
        if flows[flow_id] == 'imports':
            dropdown_texts.insert(0, ['0140AT', 'Red Meats, FR/CH/FR'])
        else:
            dropdown_texts.insert(0, ['0150AT', 'Pork & Pork Products'])
        
        # wrap the labels with double quotes
        for d in dropdown_texts:
            d[1] = '"%s"' % d[1]
        
        # save ids and labels to file
        dir_path = create_directory(WEB_USDA_PATH, 'trade_flow_monthly/title_options')
        file_path = '%sproducts_%s.csv' % (dir_path, flows[flow_id])
        wscraper.save_to_file(file_path, url, ['code', 'label'], dropdown_texts)
    
    wscraper.close()
    
    
    print 'Finished...'


if __name__ == '__main__':    
    scrape()