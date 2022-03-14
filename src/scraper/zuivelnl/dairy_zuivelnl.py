'''
Created on 19 Jun 2015

@author: Conor O'Sullivan
'''

from datas.web.scraper import WebScraper, create_directory
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD, DBManager
import time

import os

from bs4 import BeautifulSoup
import pdfquery
'''
def document_to_html(file_path):
    tmp = "/tmp"
    guid = str(uuid.uuid1())
    # convert the file, using a temporary file w/ a random name
    command = "abiword -t %(tmp)s/%(guid)s.html %(file_path)s; cat %(tmp)s/%(guid)s.html" % locals()
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=os.path.join(settings.PROJECT_DIR, "website/templates"))
    error = p.stderr.readlines()
    if error:
        raise Exception("".join(error))
    html = p.stdout.readlines()
    return "".join(html)
'''





def scrape(db_parmas):
    
    browser = WebScraper('Chrome')

    url = "http://www.zuivelnl.org/zuivelnl-organisation-of-the-dutch-dairy-supply-chain/"
    
    file = "http://www.zuivelnl.org/wp-content/uploads/2015/06/Prijzen-2015-en-2014.pdf"
    
    #wget.download(file)
    filename = os.path.abspath('Prijzen-2015-en-2014.pdf')
    
    print os.path.abspath(filename)
    
    time.sleep(5)
    
    browser.open(url)

    #browser.click_button('xpath', ".//*[@id='post-1572']/div/p[6]/a[5]")
    
    
    #subprocess.call("pdftotext Prijzen-2015-en-2014.pdf zuivenl_market_prices.txt",shell=True)
    
    
    
    time.sleep(20)
    pdf = pdfquery.PDFQuery("http://www.zuivelnl.org/wp-content/uploads/2015/06/Prijzen-2015-en-2014.pdf")
    print pdf
    #element = browser.find_elements('css', ".textLayer>div")
    #print element 
    

    html = browser.html_source()
    
    soup = BeautifulSoup(html, 'html5')
    
    #print soup.prettify()
    
    #print soup.findAll("div",{"class":"textLayer"})
    
    
    browser.close()

if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)