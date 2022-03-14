'''
Created on 11 Dec 2014

@author: Suzanne
ABANDONED
'''
from subprocess import call
import os
from datas.functions import *
from datas.web.scraper import USDA_PATH
from selenium import webdriver
<<<<<<< HEAD
=======
from datas.function.functions import *
from datas.web.scraper import *
>>>>>>> e14b217bf2a88fe84a6729657938d5b6eb3a8a94

def pdf_to_html(pdf_file, new_dir):
    """Creates a directory of html pages from a pdf.  Must have Free_PDF_Solutions downloaded from 
        http://www.freepdfsolutions.com/free-pdf-to-html.html
    
        Args: 
            pdf_file - Path to the pdf file to convert.
            new_dir - Path to the directory to save pages to.  This directory is created, should not already exist.
       
       Returns:
           Name of new directory"""
    os.chdir('/Program Files (x86)/Free_PDF_Solutions')
    call(["html", "--src="+pdf_file, "--dest="+new_dir])

<<<<<<< HEAD
web_url = 'http://usda.mannlib.cornell.edu/MannUsda/viewDocumentInfo.do?documentID=1194'    
pdf_to_html('/Users/Suzanne/workspace/DATAS_Code/src/scraper/usda/2014_12_08_1980s/wasde-02-10-1994.pdf', '/users/suzanne/workspace/DATAS_Code/output/usda/agri_economic_stats/2014-12-11-1990s/wasde-02-10-1994')

file_url = '/users/suzanne/workspace/DATAS_Code/output/usda/wasde-01-11-1990/page_004.html' 
#browser = webdriver.Chrome()
data = []
 
# '''Start scrape'''
# browser.get(file_url)
# browser.maximize_window()
=======
if __name__ == '__main__':
    
    file_name = 'agri_economic_stats'
    dir_title = datetime.now().strftime('%Y_%m_%d')
    dest_path = '%s%s/' % (USDA_PATH, file_name)
    dest_path = create_directory(dest_path, dir_title)
    
    url = 'http://usda.mannlib.cornell.edu/MannUsda/viewDocumentInfo.do?documentID=1194'
    
    # open parent window by url
    wscraper = WebScraper('Chrome')
    wscraper.open(url)
    wscraper.web_driver.maximize_window()
    time.sleep(5)
    
    # 
    txt = range(1995, 2001) + [2005, 2007, 2009]
    txt = ['n%s' % d for d in txt]
    
    xls = range(2011, 2015)
    xls = ['n%s' % d for d in xls]
    
    pdf = range(1970, 1995)
    pdf = ['n%s' % d for d in pdf]
    
    txt_xls = range(2001, 2005) + [2008, 2010]
    txt_xls = ['n%s' % d for d in txt_xls]
    
    txt_doc = ['n2006']
    
    decade_texts = ['2010s', '2000s', '1990s', '1980s', '1970s']
    decades = []
    #decade_texts = decade_texts[3:]
    print decade_texts
    
    for text in decade_texts:
        decades.append(wscraper.find_element('xpath', '//a[contains(text(), "%s")]' % text))
    print decades
    
    d_index = 0
    for decade in decades:
        decade_text = decade_texts[d_index]
        print 'start downloading %s ...' % decade_text
        
        decade.click()
        time.sleep(2)
        
        years = wscraper.find_elements('xpath', '//a[contains(text(), "%s")]/..//div/a[@class="boldlink"]' % decade_text)
        year_ids = wscraper.find_elements('xpath', '//a[contains(text(), "%s")]/..//div[@class="dirElement"]' % decade_text)
        #years = years[7:]
        #year_ids = year_ids[7:]
        
        y_index = 0
        for year in years:
            year.click()
            time.sleep(2)
            
            wscraper.scroll_to_bottom()
            time.sleep(2)
            
            year_id = year_ids[y_index].get_attribute('id')
            
            if year_id in pdf:
                months = wscraper.find_elements('xpath', '//a[contains(text(), "%s")]/..//div[@id="%s"]/div/a[contains(text(), "pdf")]' % (decade_text, year_id))
                print 'pdf'
            elif year_id in txt:
                months = wscraper.find_elements('xpath', '//a[contains(text(), "%s")]/..//div[@id="%s"]/div/a[contains(text(), "txt")]' % (decade_text, year_id))
                print 'txt'
            elif year_id in txt_xls:
                months = wscraper.find_elements('xpath', '//a[contains(text(), "%s")]/..//div[@id="%s"]/div/a[contains(text(), "txt") or contains(text(), "xls")]' % (decade_text, year_id))
                print 'txt_xls'
            elif year_id in xls:
                months = wscraper.find_elements('xpath', '//a[contains(text(), "%s")]/..//div[@id="%s"]/div/a[contains(text(), "xls")]' % (decade_text, year_id))
                print 'xls'
            elif year_id in txt_doc:
                months = wscraper.find_elements('xpath', '//a[contains(text(), "%s")]/..//div[@id="%s"]/div/a[contains(text(), "txt") or contains(text(), "doc")]' % (decade_text, year_id))
                print 'txt_doc'
            
            for month in months:
                time.sleep(3)
                if month.text in ['pdf', 'txt']:
                    file_link = month.get_attribute('href')
                    urllib.urlretrieve(file_link, dest_path + file_link.split('/')[-1])
                elif month.text in ['xls', 'doc']:
                    month.click()
                    time.sleep(5)
                    #time.sleep(20) # for year 2002
                    move_download_file(DOWNLOAD_PATH, dest_path)
            # end of inner for-loop
            
            y_index += 1
            year.click()
            time.sleep(2)
        # end of middle for-loop
        
        d_index += 1
        decade.click()
        time.sleep(2)
    # end of outter for-loop
    
    # save url to the given folder dest_path
    save_to_file(dest_path + 'bookmark_url.txt', [['url', url]])
    
    wscraper.close()
    
    print 'finished...'
    
>>>>>>> e14b217bf2a88fe84a6729657938d5b6eb3a8a94

print 'Finished'
