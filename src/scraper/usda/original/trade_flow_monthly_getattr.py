'''
Created on 18 Nov 2014

@author: Wenchong
'''


import os
import time
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from datas.functions.functions import *
from datas.web.scraper import *


COUNTER = 0


def click_expand_button(web_scraper, attr_name, attr_value):
    """Click the expand button '+'
    
    Click the all the '+' button to expand the data table.
    Specially designed for the USDA standard query web page.
    """
    global COUNTER
    
    expand_buttons = []
    
    if attr_name == 'xpath':
        expand_buttons = web_scraper.find_elements(attr_name, attr_value)
    else:
        raise ValueError, 'click_expand_button Error: not handled attr_name'
    
    for btn in expand_buttons:
        if btn.get_attribute('value') == '+':
            WebDriverWait(web_scraper.web_driver, 180).until(EC.element_to_be_clickable((By.XPATH, attr_value)))
            time.sleep(15)
            
            btn.click()
            
            WebDriverWait(web_scraper.web_driver, 180).until(EC.element_to_be_clickable((By.XPATH, attr_value)))
            time.sleep(25)
            '''
            def find(web_driver):
                elements = web_driver.find_elements_by_xpath(attr_value)
                for e in elements:
                    if e.get_attribute('value') == '+':
                        if e.get_attribute('disabled') == 'true':
                            return False
                return e
            
            WebDriverWait(web_scraper.web_driver, 180).until(find)
            
            btn.click()
            WebDriverWait(web_scraper.web_driver, 180).until(find)
            '''
            # scroll down and left to '+' button view
            wscraper.web_driver.execute_script('scroll(-300, 0);')
            wscraper.web_driver.execute_script('window.scrollTo(0,Math.max(document.documentElement.scrollHeight,document.body.scrollHeight,document.documentElement.clientHeight));')
            time.sleep(2)
            
            click_expand_button(web_scraper, attr_name, attr_value)
            break


if __name__ == '__main__':
    dir_title = datetime.now().strftime('%Y_%m_%d')
    dir_path = USDA_PATH + 'trade_flow_monthly/'
    
    # read product codes from file
    product_labels = read_from_file('%stitle_options/%s.csv' % (dir_path, 'products'))
    product_codes = [p[0] for p in product_labels[3:]]
    
    dir_path = create_directory(dir_path, dir_title + '_getattr')
    
    download_path = 'C:\Users\Wenchong\Downloads'
    
    url = 'http://apps.fas.usda.gov/gats/ExpressQuery1.aspx'
    
    wscraper = WebScraper('Chrome')
    wscraper.open(url)
    wscraper.web_driver.maximize_window()
    
    # browse standard query page
    wscraper.click_button('id', 'ctl00_ContentPlaceHolder1_lbExpressQuery')
    time.sleep(2)    
    
    # search for products with code containing 0203
    wscraper.load_field('select', 'name', 'ctl00$ContentPlaceHolder1$ddlProductSearch', 'Code')
    wscraper.load_field('input', 'name', 'ctl00$ContentPlaceHolder1$txtProductSearch', '0203')
    wscraper.click_button('id', 'ctl00_ContentPlaceHolder1_btnProductSearch')
    time.sleep(2)
    
    # select value to display
    wscraper.load_field('select', 'name', 'ctl00$ContentPlaceHolder1$ddlValueType', 'GVAL')
    time.sleep(2)
    
    # select dollars as value unit
    wscraper.load_field('select', 'name', 'ctl00$ContentPlaceHolder1$ddlValueUnit', 'D')
    time.sleep(2)
    
    # select quantity to display
    wscraper.load_field('select', 'name', 'ctl00$ContentPlaceHolder1$ddlQuantityType', 'Q1')
    time.sleep(2)
    
    # select FAS Non Converted as quantity unit
    wscraper.load_field('select', 'name', 'ctl00$ContentPlaceHolder1$ddlQuantityUnit', 'FASN')
    time.sleep(2)
    
    # select Monthly to display
    wscraper.load_field('select', 'name', 'ctl00$ContentPlaceHolder1$ddlDateSeries', 'Monthly')
    time.sleep(2)
    
    # select start year
    wscraper.load_field('select', 'name', 'ctl00$ContentPlaceHolder1$ddlStartYear', '1967')
    time.sleep(2)
    
    #expand_btn_xpath = '//td[@cellcontent1="  World Total"]/..//td/input[@class="stdGridExpandCollapseButton" and not(@disabled)]'
    expand_btn_xpath = '//td[@cellcontent1="  World Total"]/..//td/input[@class="stdGridExpandCollapseButton"]'
    
    # scrape data in separate files for different products
    for prod in product_codes:
        print 'scraping %s...' % prod
        
        # select a given product
        wscraper.load_field('select', 'name', 'ctl00$ContentPlaceHolder1$lb_Products', prod)
        time.sleep(2)
        
        # click retrieve data button
        wscraper.click_button('id', 'ctl00_ContentPlaceHolder1_btnRetrieveData')
        wscraper.wait(180, 'xpath', expand_btn_xpath)
        #time.sleep(10)
        
        # expand the '+' button
        click_expand_button(wscraper, 'xpath', expand_btn_xpath)
        
        # click save as csv button
        wscraper.wait(180, 'id', 'ctl00_ContentPlaceHolder1_UltraWebTab1__ctl1_grdExpressQuery_btn_ExportToExcel')
        wscraper.click_button('id', 'ctl00_ContentPlaceHolder1_UltraWebTab1__ctl1_grdExpressQuery_btn_ExportToExcel')
        time.sleep(15)
        
        # find the downloaded file and save it as dest_file and remove the original file
        dest_file = '%s%s_%s.csv' % (dir_path, 'worldtotal', prod)
        save_download_file(download_path, dest_file)
    # end of for-loop
    
    wscraper.close()
    
    
    print 'Finished...'
    
    
