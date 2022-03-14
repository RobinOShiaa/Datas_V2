'''
Created on 28 Nov 2014

@author: Wenchong
'''


import os
import sys
import time
import urllib
import urllib2
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from function.function import create_directory
from function.function import get_download_file_name
from function.function import delete_directory
from function.function import delete_file
from function.function import join_list
from function.function import save_download_file
from function.function import save_to_file
from function.function import unzip
from web.path import DOWNLOAD_PATH
from web.path import WEB_EUROSTAT_PATH


class WebScraper(object):
    """Summary
    
    classdocs
    
    Attributes:
        
    """


    def __init__(self, driver='Chrome', user_agent=''):

        """"""
        self.driver_name = driver
        self.user_agent = user_agent
        
        if driver == 'Firefox':
            if self.user_agent != '':
                profile = webdriver.FirefoxProfile()
                profile.set_preference('general.useragent.override', self.user_agent)
                self.web_driver = webdriver.Firefox(profile)
            else:
                self.web_driver = webdriver.Firefox()
        elif driver == 'Chrome':
            if self.user_agent != '':
                options = webdriver.ChromeOptions()
                options.add_argument('--user-agent=%s' % self.user_agent)
                self.web_driver = webdriver.Chrome(chrome_options=options)
            else:
                self.web_driver = webdriver.Chrome(executable_path=[cd_path for cd_path in os.environ["PATH"].split(";") if "chromedriver" in cd_path][0])
        elif driver == 'urllib':
            self.web_driver = urllib
        elif driver == 'urllib2':
            self.web_driver = urllib2
        

        if driver != 'urllib2':
            self.web_driver.implicitly_wait(100)

    
    def open(self, url):
        if self.driver_name in ['Firefox', 'Chrome']:
            self.web_driver.get(url)
            return True
        elif self.driver_name in ['urllib', 'urllib2']:
            # return response
            if self.user_agent != '':
                headers = {'User-Agent' : self.user_agent}
                req = self.web_driver.Request(url, headers=headers)
                return self.web_driver.urlopen(req)
            else:
                return self.web_driver.urlopen(url)
    
    def close(self):
        if self.driver_name in ['Firefox', 'Chrome']:
            self.web_driver.quit()
        elif self.driver_name in ['urllib', 'urllib2']:
            pass
    
    def find_element(self, attr_name, attr_value):
        if attr_name == 'id':
            element = self.web_driver.find_element_by_id(attr_value)
        elif attr_name == 'name':
            element = self.web_driver.find_element_by_name(attr_value)
        elif attr_name == 'class':
            element = self.web_driver.find_element_by_class_name(attr_value)
        elif attr_name == 'xpath':
            element = self.web_driver.find_element_by_xpath(attr_value)
        elif attr_name == 'tag':
            element = self.web_driver.find_element_by_tag_name(attr_value)
        else:
            raise ValueError, 'find_element() Error: not handled attr_name %s' % attr_name
        
        return element
    
    def find_elements(self, attr_name, attr_value):
        if attr_name == 'id':
            elements = self.web_driver.find_elements_by_id(attr_value)
        elif attr_name == 'name':
            elements = self.web_driver.find_elements_by_name(attr_value)
        elif attr_name == 'class':
            elements = self.web_driver.find_elements_by_class_name(attr_value)
        elif attr_name == 'xpath':
            elements = self.web_driver.find_elements_by_xpath(attr_value)
        elif attr_name == 'tag':
            elements = self.web_driver.find_elements_by_tag_name(attr_value)
        else:
            raise ValueError, 'find_elements() Error: not handled attr_name %s' % attr_name
        
        return elements
    
    def switch_to_popup_window(self):
        """ Switch to popup window
        """
        parent_handle = self.web_driver.current_window_handle
        
        handles = self.web_driver.window_handles
        
        
        handles.remove(parent_handle)
        popup_window_handle = handles.pop()
        self.web_driver.switch_to_window(popup_window_handle)
       
    def switch_to_parent_window(self):
        """Switch back to parent window from popup window
        """
        handles = self.web_driver.window_handles
        parent_handle = handles.pop()
        self.web_driver.switch_to_window(parent_handle)
    
    def switch_browser_window(self,window_num):
        parent_handle = self.web_driver.current_window_handle        
        handles = self.web_driver.window_handles     
        
        self.web_driver.switch_to.window(handles[window_num])
    
    def scroll_vertical(self, x_range):
        self.web_driver.execute_script('scroll(%s, 0);' % x_range)
    
    def scroll_horizontal(self, y_range):
        self.web_driver.execute_script('scroll(0, %s);' % y_range)
    
    def scroll_to_bottom(self):
        self.web_driver.execute_script('window.scrollTo(0,Math.max(document.documentElement.scrollHeight,document.body.scrollHeight,document.documentElement.clientHeight));')
        
    def load_field(self, tag_name, attr_name, attr_value, value):
        """Supply the field with given value and submit"""
        
        if tag_name == 'select':
            if attr_name == 'name': # used to be 'list'
                element = self.web_driver.find_element_by_name(attr_value)
            elif attr_name == 'id':
                element = self.web_driver.find_element_by_id(attr_value)
            select = Select(element)
            select.select_by_value(value)
        elif tag_name == 'input':
            if attr_name == 'name': # used to be 'list'
                element = self.web_driver.find_element_by_name(attr_value)
            elif attr_name == 'id': # used to be 'date'
                element = self.web_driver.find_element_by_id(attr_value)
            element.send_keys(value)
            
    def load_field_multiple(self, xpath, start_index=0, exclude_pattern=''):
        """Selects multiple options with given value"""
        # get all elements in the multiple selection field
        elements = self.web_driver.find_elements_by_xpath(xpath)
        action = ActionChains(self.web_driver)
        action.key_down(Keys.CONTROL)
        
        # take only the elements that don't contain the exclude_pattern
        if exclude_pattern != '':
            elements = [e for e in elements[start_index:] if e.text[0] != exclude_pattern]
        
        # multiple select
        for element in elements:
            action.click(element)
        action.key_up(Keys.CONTROL).perform()
        
    def click_multiple(self,element_list):
        action = ActionChains(self.web_driver)
        action.key_down(Keys.CONTROL)
        for ele in element_list:
#             if element_type=='xpath':
#                 element = self.web_driver.find_element_by_xpath(ele)
#             elif element_type=='text':
#                 element = self.web_driver.find_element_by_link_text(ele)
#             elif element_type=='id':
            element = self.web_driver.find_element_by_xpath(ele)
            action.click(element)
        action.key_up(Keys.CONTROL).perform()    
            
            
    def wait(self, seconds_to_wait, attr_name, attr_value):
        if attr_name == 'id':
            WebDriverWait(self.web_driver, seconds_to_wait).until(lambda d: d.find_element_by_id(attr_value))
        elif attr_name == 'name':
            WebDriverWait(self.web_driver, seconds_to_wait).until(lambda d: d.find_element_by_name(attr_value))
        elif attr_name == 'xpath':
            WebDriverWait(self.web_driver, seconds_to_wait).until(lambda d: d.find_element_by_xpath(attr_value))
        elif attr_name == 'class':
            WebDriverWait(self.web_driver, seconds_to_wait).until(lambda d: d.find_element_by_class_name(attr_value))
        else:
            raise ValueError, 'wait() Error: not handled attr_name %s' % attr_name
    
    def html_source(self):
        return self.web_driver.page_source
    
    def save_html(self, url, file_path):
        file(file_path, "wb").write(urllib2.urlopen(url).read())
    
    def hover(self,  target_type, target):
        if target_type=='xpath':
            element = self.web_driver.find_element_by_xpath(target)
        elif target_type=='element':
            element = target
        else:
            raise Exception, 'hover() error, incorrect target type %s' % target_type
        
        hov = ActionChains(self.web_driver).move_to_element(element)
        hov.perform()
        time.sleep(2)
            
    def hover_css(self,css):
        element = self.web_driver.find_element_by_class_name(css)
        hov = ActionChains(self.web_driver).move_to_element(element)
        hov.perform()
        time.sleep(2)
    
    def click_button(self, attr_name, attr_value):
        """Click button by tag attribute"""
        if attr_name == 'name':
            self.web_driver.find_element_by_name(attr_value).click()
        elif attr_name == 'class':
            self.web_driver.find_element_by_class_name(attr_value).click()
        elif attr_name == 'id':
            self.web_driver.find_element_by_id(attr_value).click()
        elif attr_name == 'xpath':
            self.web_driver.find_element_by_xpath(attr_value).click()
        elif attr_name == 'link_text':
            self.web_driver.find_element_by_link_text(attr_value).click()
    
    def click_checkbox_by_xpath(self, xpath):
        elements = self.find_elements('xpath', xpath)
        
        for element in elements:
            element.click()
    
    def click_checkbox(self, title_xpath, checkall_tag_id, checkbox_xpath, ids):
        """Click specified checkboxes
        
        Click checkboxes with given ids.
        Specially designed for eurostat.
        """
        # select the given 12 months under Period label
        self.click_button('xpath', title_xpath)
        
        # TODO(Wenchong): automate this piece of code
        self.click_button('id', checkall_tag_id)
        self.click_button('id', checkall_tag_id)
        
        for i in ids:
            self.click_button('xpath', checkbox_xpath % (i))
    
    def click_eurostat_checkbox(self, title_xpath, checkbox_xpath, ids, default_id):
        """Click specified checkboxes
        
        Click checkboxes with given ids.
        Specially designed for eurostat.
        """
        # select the given 12 months under Period label
        self.wait(30, 'xpath', title_xpath)
        self.click_button('xpath', title_xpath)
        time.sleep(1)
        
        # unselect the checkbox with the default_id
        self.wait(30, 'xpath', checkbox_xpath % (default_id))
        self.click_button('xpath', checkbox_xpath % (default_id))
        time.sleep(1)
        
        # select all given ids
        for i in ids:
            self.click_button('xpath', checkbox_xpath % (i))
        
        time.sleep(1)
    
    def click_expand_button(self, attr_name, attr_value):
        """Click the expand button '+'
        
        Click the all the '+' button to expand the data table.
        Specially designed for the USDA standard query web page.
        """
        '''
        if attr_name == 'xpath':
            expand_buttons = self.web_driver.find_elements_by_xpath(attr_value)
        else:
            raise ValueError, 'click_expand_button Error: not handled attr_name'
        '''
        expand_buttons = self.web_driver.find_elements_by_xpath(attr_value)
        
        for btn in expand_buttons:
            if str(btn.get_attribute('value')) == '+':
                btn.click()
                time.sleep(5)
                self.click_expand_button(attr_name, attr_value)
                break
    
    def switch_frame(self,frame):
        #print self.web_driver.frames
        self.web_driver.switch_to_frame(frame)
        
    
    def get_dropdown_list(self, attr_name, attr_value, result_type='value'):
        """Get all option values in a dropdown list"""
        dropdown_box = None
        
        if attr_name == 'id':
            dropdown_box = self.web_driver.find_element_by_id(attr_value)
        elif attr_name == 'name':
            dropdown_box = self.web_driver.find_element_by_name(attr_value)
        
        # get all objects in the dropdown list
        # TODO(Wenchong): add more find_elements_by options
        
        options = [x for x in dropdown_box.find_elements_by_tag_name('option')]
        results = []
        
        if result_type == 'value':
            # get the values of all dropdown list objects
            for option in options:
                results.append(str(option.get_attribute('value')))
        elif result_type == 'text':
            # get the texts of all dropdown list objects
            for option in options:
                results.append(str(option.text))
        
        return results
    
    def get_title_attributes(self, bookmark_url, dir_path, title):
        """
        Designed for Eurostat
        """
        # get title checkbox_ids
        tags = self.web_driver.find_elements_by_xpath('//td/input[starts-with(@id, "ck_")]')
        checkbox_ids = [[str(r.get_attribute('id'))] for r in tags]
        
        # get title codes
        tags = self.web_driver.find_elements_by_xpath('//td/label[starts-with(@for, "ck_")]')
        codes = []
        if title == 'indicators':
            codes = [[str(r.text).replace('_IN_', '_')] for r in tags]
        else:
            codes = [[str(r.text)] for r in tags]
        
        # get title labels, replace ',' with '/' 
        tags = self.web_driver.find_elements_by_tag_name('td')
        labels = [[str(r.text).replace(',', '/')] for r in tags if r.get_attribute('title')]
        
        # join checkbox_ids, codes and labels
        title_attrs = join_list(checkbox_ids, codes)
        title_attrs = join_list(title_attrs, labels)

        # remove annual data
        if title == 'periods':
            removes = [r for r in title_attrs if int(r[1][4:]) > 12]
            for r in removes:
                title_attrs.remove(r)

        title_attrs.insert(0, ['url', bookmark_url])
        title_attrs.insert(1, ['checkbox_id', 'code', 'label'])

        file_path = '%s%s.csv' % (dir_path, title)
        delete_file(file_path)
        save_to_file(file_path, title_attrs)
    
    def save_to_file(self, file_path, source_url, headers, data_list):
        """"""
        out_file = None
        
        if os.path.isfile(file_path):
            out_file = open(file_path, 'a')
        else:
            out_file = open(file_path, 'w')
            out_file.write('url,%s\n' % (source_url))
            out_file.write(','.join(headers))
            out_file.write('\n')
        
        for d in data_list:
            out_file.write(','.join(d))
            out_file.write('\n')
        
        out_file.close()
    
    def download_file(self, url, file_path):
        url_conn = self.open(url)
        out_file = open(file_path, 'w')
        out_file.write(url_conn.read())
        out_file.close()
        url_conn.close()
    
    def download_eurostat_file(self, file_name, bookmark_url, seconds_to_sleep, part):
        # open the download window
        self.wait(30, 'class', 'download')
        self.click_button('class', 'download')
        #time.sleep(5)
        
        # select file format as multiple csv files
        #self.wait(30, 'id', 'csvFULL_EXTRACTION')
        if not self.find_element('id', 'csvFULL_EXTRACTION').is_selected():
            self.click_button('id', 'csvFULL_EXTRACTION')
        time.sleep(1)
        self.click_button('id', 'csvFULL_EXTRACTION_CSV_SINGLE_FILE')
        time.sleep(1)
                
        # download file to default download path
        self.click_button('xpath', '//input[@value="Download in CSV Format"]')
        #time.sleep(2)
        #self.wait(10, 'xpath', '//button[contains(text(), "Ok")]')
        #self.click_button('xpath', '//button[contains(text(), "Ok")]')
        time.sleep(seconds_to_sleep)

        # save file to the given file dest_file
        dir_title = datetime.now().strftime('%Y_%m_%d') + part
        dest_path = '%s%s\\' % (WEB_EUROSTAT_PATH, file_name)
        dest_path = create_directory(dest_path, dir_title)
        
        # get the downloaded file extension
        download_file = get_download_file_name(DOWNLOAD_PATH)
        file_extension = download_file.split('.')[-1]
        #print file_extension
        if file_extension == 'zip':
            dest_file = '%s%s.zip' % (dest_path, file_name)
        elif file_extension == 'csv':
            dest_file = '%s%s.csv' % (dest_path, file_name)
        else:
            raise Exception('datas.web.scraper.download_eurostat_file() error:', 'invalid downloaded file extension')
        
        # the downloaded zip file is saved to the output_web here
        # if save_download_file() fails, delete any files written
        # to the output_web folder, otherwise, it may cause file
        # can't write error in the next scrape within the same day
        try:
            save_download_file(DOWNLOAD_PATH, dest_file)
        except Exception as err:
            delete_directory(dest_path.split('part')[0])
            exc_info = sys.exc_info()
            raise Exception('datas.web.scraper.download_eurostat_file() error:', exc_info[0], exc_info[1], exc_info[2])
        
        # if donwloaded file is a zip file, unzip all contents of
        # the zip file dest_file to the given folder dest_path,
        # then delete the original zip file.
        # if unzip() fails, delete any files written
        # to the output_web folder, otherwise, it may cause file
        # can't write error in the next scrape within the same day
        if file_extension == 'zip':
            try:
                unzip(dest_file, dest_path)
            except Exception as err:
                delete_directory(dest_path.split('part')[0])
                exc_info = sys.exc_info()
                raise Exception('datas.web.scraper.download_eurostat_file() error:', exc_info[0], exc_info[1], exc_info[2])
            else:
                delete_file(dest_file)
        
        # save bookmark_url to the given folder dest_path
        try:
            save_to_file(dest_path + 'bookmark_url.txt', [['url', bookmark_url]])
        except Exception as err:
            exc_info = sys.exc_info()
            raise Exception('datas.web.scraper.download_eurostat_file() error:', exc_info[0], exc_info[1], exc_info[2])
        
    def login_eurostat_query(self, email, password):
        self.click_button('xpath', ".//*[@id='content']/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr/td[4]/div/a") # login
        time.sleep(3)
        self.click_button('xpath',".//*[@id='responsive-main-nav']/div[6]/a[2]") # External
        self.load_field('input', 'name', 'username', email)
        self.load_field('input','name','password',password)
        time.sleep(1)
        #//*[@id="loginForm"]/input[13]
        self.click_button('xpath',".//*[@id='loginForm']/input[@title='Login!']") # login button
        time.sleep(3)
        
    def delete_eurostat_queries(self):
        self.hover('xpath',".//*[@id='selectAll1']")
        time.sleep(2)
        self.click_button('xpath',".//*[@id='selectAll1']")
        self.hover('xpath',".//*[@id='deletes1']")
        time.sleep(2)
        self.click_button('xpath',".//*[@id='deletes1']")
        
    def select_eurostat_output_options(self,):
        self.click_button('xpath', ".//*[@id='setBatchOutputFormat']")
        self.click_button('xpath', ".//*[@id='batchOptions']/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr[2]/td[2]/input[3]") # labels
        self.click_button('xpath', ".//*[@id='batchFormats']/option[1]")
        
    def accept_alert(self):
        # wait until alert is present, seems EC is not working, abandoned
#         while not EC.alert_is_present:
#             time.sleep(1)
        
        # click OK/Enter/Yes button to accept the alert
        alert = self.web_driver.switch_to_alert()
        alert.accept()
        

# end of file

