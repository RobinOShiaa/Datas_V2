'''
Created on 5 Dec 2014

@author: Suzanne
'''
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from datetime import datetime
import time
from datas.function.function import create_directory#, save_to_file_append
from datas.web.scraper import WebScraper
import sys
#import os
from datas.function.function import save_error_to_log 
from datas.web.path import WEB_SUPERVALU_PATH
from datas.db.manager import RAW_DB_NAME, USERNAME, PASSWORD, HOST

def login(scraper, username_element, password_element, username, password, button_id):
    '''Uses tag IDs. NB - Must have already registered with site.'''
    element1 = scraper.find_element('id', username_element)
    element1.send_keys(username)
    element2 = scraper.find_element('id', password_element)
    element2.send_keys(password)
    scraper.click_button('id', button_id)

def find_next(scraper):
    try:
        next_button = scraper.find_element('xpath', '//div[@class="pagingDisplay"]/a[text()="Next"]')
    except NoSuchElementException:
        return False 
    else:
        next_button.click()
        return True 


def scrape(db_params):
    try:
        print 'Start scrape at %s...' % datetime.now()
        
        url = 'https://shop.supervalu.ie/shopping/'
        today = datetime.now().strftime("%Y_%m_%d")
        headers = ['Product name','Price (euro)', 'per unit']
        
        dir_path = create_directory(WEB_SUPERVALU_PATH, today)
        file_path = '%ssupermarket.csv' % (dir_path)
        
        scraper = WebScraper('Chrome')
        scraper.web_driver.implicitly_wait(0)
        scraper.open(url)
        scraper.web_driver.maximize_window()
    
        #scraper.click_button('id', 'ctl00_ctl00_SideBarControl_btnSignIn')
        #login(scraper, 'ctl00_ctl00_cphContent_cphMain_ucntrlLogin_txtEmailAddress', 'ctl00_ctl00_cphContent_cphMain_ucntrlLogin_txtPassword', 'smccarthy@computing.dcu.ie','iamnot2scrapers', 'ctl00_ctl00_cphContent_cphMain_ucntrlLogin_btnLogin')
    
        links = []
        names = []
        #n_append = names.append
        l_append = links.append
        #tags = scraper.find_elements('xpath', '//*[@id="ctl00_ctl00_cphMenu_MegaMenu1_SVMenu"]/ul/li/ul/div/div/li/a')
        tags = scraper.find_elements('xpath', '//div//li[@class="AspNet-MegaMenu-WithChildren"]/a')
        print tags
        #login(scraper, 'ctl00_ctl00_cphContent_cphMain_ucntrlLogin_txtEmailAddress', 'ctl00_ctl00_cphContent_cphMain_ucntrlLogin_txtPassword', 'smccarthy@computing.dcu.ie','iamnot2scrapers', 'ctl00_ctl00_cphContent_cphMain_ucntrlLogin_btnLogin')
    
        for tag in tags:
            l_append(tag.get_attribute('href'))
        links = filter(None, links)

        scraper.close()
    #     for tag in tags:
    #         n_append(tag.text.replace('\n', '').replace('\t', ''))
    #     names = filter(None, names)
    # 
    #     searches = dict(zip(links, names))
        
        products = []
        prices = []
            
        #for k,v in searches.items():
        for k in links[1:]:
    
            scraper = WebScraper('Chrome')
            scraper.web_driver.maximize_window()
    #         scraper.web_driver.implicitly_wait(8)
            scraper.open(k)
    
#             sorry = ''
#             try:
#                 sorry = scraper.find_element('xpath', '//*[@id="main-content"]/div/div[2]/div[contains(text(), "sorry")]')
#             except:
#                 pass
#              
#             else:
#                 scraper.close()
#                 continue
    #         
    #         print 'about to log in'
    #         try:
    #             login(scraper, 'ctl00_ctl00_cphContent_cphMain_ucntrlLogin_txtEmailAddress', 'ctl00_ctl00_cphContent_cphMain_ucntrlLogin_txtPassword', 'smccarthy@computing.dcu.ie','iamnot2scrapers', 'ctl00_ctl00_cphContent_cphMain_ucntrlLogin_btnLogin')
    #         except:
    #             scraper.close()
    #             continue
    #         
    #         print 'logged in and scraping'
#             more_products = True
#             while more_products == True:
                #button = '' 
            try:
                #print 'entering try'
                #button = scraper.find_element('xpath', '//*/a[text()="Next"]')
                scraper.click_button('class', 'listAllText')
            except (NoSuchElementException, StaleElementReferenceException):
                pass
            else:
                time.sleep(5)
            
            #Extract product names
            product_tags = []
            #product_tags = scraper.find_elements('id', 'divProductTitle')
            try:
                product_tags = scraper.find_elements('class', 'productTitle')
            except:
                scraper.close()
                continue
            for product_tag in product_tags:
                products.append(product_tag.text.encode('utf-8', 'ignore').replace(',',''))
            #print products     
            #Extract price per unit (ignore price of item)  
            price_tags = scraper.find_elements('id', 'productPricePerUnit')
            for price_tag in price_tags:
                prices.append(price_tag.text.encode('ascii', 'ignore').replace(' ','').replace('per',',per ').replace('each', ',each'))
            #print prices
            #check whether 'Next' button is present  
            #more_products = find_next(scraper)
            #print product_tags
                
                
                '''testing'''
#                 try:
#                     next_button = scraper.find_element('xpath','//*[@id="ctl00_ctl00_ctl00_cphContent_cphMain_upnlShopContent"]//div[@class="pagingDisplay"]/a[text()="Next"]')
#                 except  NoSuchElementException:
#                     more_products=False
#                     print 'continuing'
#                     continue
#                 else:
#                     next_button.click()
#                     time.sleep(2)
                '''/testing'''
                    
#                 try:
#                     print 'entering try'
#                     #button = scraper.find_element('xpath', '//*/a[text()="Next"]')
#                     scraper.click_button('xpath', '//*[@id="ctl00_ctl00_ctl00_cphContent_cphMain_upnlShopContent"]//div[@class="pagingDisplay"]/a[text()="Next"]')
#                 except NoSuchElementException:
#                     print 'entering except'
#                     more_products = False
#                     continue 
#                 else:
#                     print 'entering else'
#                     #button.click()
#                     time.sleep(5)
#                     more_products = True
            scraper.close()     
            '''Data output'''
            data = zip(products, prices)
            with open(file_path, 'a') as file:
                file.write('url,'+url+'\n'+','.join(headers)+'\n')
                for d in data:
                    file.write(','.join(d))
                    file.write('\n')
        #scraper.close()
        print 'Finished scrape at %s.' % datetime.now()
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['supervalu'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('weekly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['supervalu'],[success_msg]]
        save_error_to_log('weekly', msg_list)
       

if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)

    
