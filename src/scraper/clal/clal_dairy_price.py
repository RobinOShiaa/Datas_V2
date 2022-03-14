'''
Created on 28 May 2015

@author: Conor O'Sullivan
'''
import time
from datetime import datetime
from datas.function.function import chunck_list
from datas.web.path import WEB_CLAL_PATH
from datas.web.scraper import WebScraper, create_directory
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD, DBManager
from bs4 import BeautifulSoup
import sys
from datas.function.function import save_error_to_log

def scrape(db_params):
    #try:
        print 'Start scraping at %s...' % datetime.now()
        
        dbm = DBManager(db_params[0], db_params[1], db_params[2], db_params[3])
        
        del dbm
        
        urls = ["http://www.clal.it/en/?section=burro_francia","http://www.clal.it/en/index.php?section=poudre",
                "http://www.clal.it/en/index.php?section=burro_usa","http://www.clal.it/en/index.php?section=whole","http://www.clal.it/en/index.php?section=susmolken#lebens",
                "http://www.clal.it/en/index.php?section=caseine#acida"]
        
    
        for url in urls:    
            browser = WebScraper('Chrome')
            browser.open(url)
            browser.web_driver.maximize_window()
            
            
            if url == urls[-1]:
                #//*[@id="pagina"]/table/tbody/tr[12]/td/div/a
                browser.click_button('xpath', ".//*[@id='pagina']/table/tbody/tr[12]/td/div/a")
            
            time.sleep(5)
            
            html = browser.html_source()
            if url == urls[1]:
                title = browser.find_element('xpath',".//*[@id='pagina']/table/tbody/tr[1]/td/h2").text.encode('UTF-8').split('-')[1].strip().replace(" ","_")
            
            else:
                title = browser.find_element('xpath',".//*[@id='pagina']/table/tbody/tr[1]/td/h2").text.replace(",","").replace(" ","_")

            # (Sue) This line needs to specify html5 on my computer.  Not anyone else's?
            soup = BeautifulSoup(html, "html.parser")

            tr_headers = soup.findAll("tr",{"style":"text-align:center;"})[1]
            #print tr_headers
            td_headers = tr_headers.findAll("td")
            headers = []
            
            for td_header in td_headers:
                if '%' not in td_header.text.encode('UTF-8'):
                    headers.append(td_header.text.encode('UTF-8'))
                else:
                    break
            
            
            
            #for header in headers:
            #    print header 
            data = []
            
            if url == urls[0]:
                trs = soup.findAll("tr",{"style":"text-align:right;"})
                
                
                for tr in trs:
                    tds = tr.findAll("td")
                    for td_num in xrange(0,len(headers)+1):
                        data.append(tds[td_num].text.encode('UTF-8'))
            
            elif url == urls[5]:
                div_table = soup.findAll("div",{"class":"showHideContents"})[0]
                data_table = div_table.findAll('table')[0]
                trs = data_table.findAll('tr')
                for tr_num in xrange(2,14):
                    tds = trs[tr_num].findAll("td")
                    for td_num in xrange(0,len(headers)+1):
                        data.append(tds[td_num].text)
                
            else:       
                td_table = soup.findAll("td",{"class":"showHideContents"})[0]
                
                trs = td_table.findAll("tr",)
                for tr_num in xrange(2,14):
                    tds = trs[tr_num].findAll("td")
                    for td_num in xrange(0,len(headers)+1):
                        #print tds[td_num].text
                        data.append(tds[td_num].text)
            
            chunked_list = chunck_list(data,len(headers)+1)
            
            dir_title = datetime.now().strftime('%Y_%m_%d')
            file_path = create_directory('%sdairy_price' % WEB_CLAL_PATH, dir_title)
            
            if (url == urls[0]) or (url == urls[1]) or (url == urls[4]):
                unit = 'euro'
            else:
                unit = 'dollar'
            
            out_file = open(file_path + title + '_' + unit + '_per_ton.csv', 'w')
            out_file.write('url,%s\nmonth,' % (url))
            out_file.write(','.join(headers))
            out_file.write('\n')
            for d in chunked_list:
                
                out_file.write(','.join(d))
                out_file.write('\n')
            out_file.close()
            
            browser.close()
        print 'Finish scraping at %s.' % datetime.now()
#     except Exception as err:
#         exc_info = sys.exc_info()
#         error_msg = 'auto_run() scrape error:\n'
#         msg_list = [['clal_dairy_price.py'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
#         print msg_list
#         save_error_to_log('monthly', msg_list)
#     else:
#         success_msg = 'auto_run() scraped successfully\n'
#         msg_list = [['clal_dairy_price.py'],[success_msg]]
#         save_error_to_log('monthly', msg_list)

if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)

    