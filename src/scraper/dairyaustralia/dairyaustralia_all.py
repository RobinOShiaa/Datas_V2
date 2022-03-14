'''
Created on 3 Dec 2014

@author: Sue

09/04/2015(Wenchong): Fixed file path bugs and deleted xls files after conversion.
Note that this scraper requires chrome as the browser, cannot run in firefox
'''
import sys
from datas.function.function import save_error_to_log, get_file_paths, delete_file
import pandas as pd
import time
from datetime import datetime
from datas.function.function import create_directory
from datas.function.function import move_download_file
from datas.function.function import get_file_name
from datas.web.path import DOWNLOAD_PATH
from datas.web.path import WEB_DAIRYAUSTRALIA_PATH
from datas.web.scraper import WebScraper
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD


def scrape(db_params):
    try:
        print 'Start scraping at %s ' % (datetime.now())
           
        # open parent window by url
        wscraper = WebScraper('Chrome')
        url = 'http://www.dairyaustralia.com.au/Markets-and-statistics/Production-and-sales/Latest-statistics.aspx'
        wscraper.open(url)
#            
#         # Find date of latest update on website
#         latest_update = wscraper.find_element('xpath', '//em[contains(text(), "Last updated")]').text.split(' ')[2]
#         latest_update = datetime.strptime(latest_update, '%d/%m/%Y')
#             
#         if date_from >= latest_update:
#             print 'No new data.'
#             return
        
        file_name = 'latest_production'
        dir_title = datetime.now().strftime('%Y_%m_%d')
        dest_path = '%s%s\\' % (WEB_DAIRYAUSTRALIA_PATH, file_name)
        dest_path = create_directory(dest_path, dir_title)
     
        # download xls files and save to output folder
        links = wscraper.find_elements('xpath', '//a[contains(text(), "XLS")]')#[:4]
        for link in links:
            link.click()
            time.sleep(5)
            try:
                move_download_file(DOWNLOAD_PATH, dest_path)
            except:
                pass
            time.sleep(2)

        wscraper.close()
    
        # convert from .xls to .csv
        file_names = get_file_name(dest_path, pattern='*', extension='.xls')
        for f in file_names:
            xls = pd.ExcelFile(dest_path+f)
            #if 'Cheese by Type' in f:
            if 'Chs' in f:
                df = xls.parse('Cheese Type', index_col=None)
                df.to_csv('%scheese_production_type.csv' % dest_path, index=False)
            elif 'Milk Sales' in f:
                df = xls.parse('Type', index_col=None)
                df.to_csv('%smilk_sales_type.csv' % dest_path, index=False) 
                df = xls.parse('State', index_col=None)
                df.to_csv('%smilk_sales_state.csv' % dest_path, index=False)                  
            elif 'Nat MilkProduction' in f:
                df = xls.parse('National by State', index_col=None)
                df.to_csv('%smilk_production_state.csv' % dest_path, index=False)
               
            elif 'NSWMilk' in f:
                df = xls.parse('NSW Monthly', index_col=None)
                df.to_csv('%smilk_production_nsw.csv' % dest_path, index=False)
                   
            #elif 'Prod Summary' in f:
            elif 'Manufactured' in f:
                df = xls.parse('Production Summary', index_col=None)
                df.to_csv('%sdairy_production_type.csv' % dest_path, index=False)
               
            elif 'VICMilk' in f:
                df = xls.parse('VIC Monthly', index_col=None)
                df.to_csv('%smilk_production_vic.csv' % dest_path, index=False)
       
          
        # remove all xls files
        xls_paths = get_file_paths(dest_path, pattern='*', extension='.xls')
        for xpath in xls_paths:
            delete_file(xpath)

         
        # scrape pdf files, save to output folder
#         pdf_links = wscraper.find_elements('xpath', '//a[contains(text(), "PDF")]')[4:]
#         for link in pdf_links:
#             response = urllib2.urlopen(link.get_attribute('href'))
#             file = open(dest_path+link.get_attribute('href').split('/')[-1].replace('%20',''), 'wb')
#             file.write(response.read())
#             file.close()
#             time.sleep(5)
#         # convert to html 
#         pdf_file_names = get_file_name(dest_path, pattern='*', extension='.pdf')
#         for pdf in pdf_file_names:
#             os.chdir("C:\Users\Suzanne\PdfToHtml")
#             call(["pdftohtml.exe", "%s" % (dest_path+pdf), "%s" % (dest_path+pdf.replace('.pdf','.html'))])
#  
#  
#         #dest_path = '%s%s\\' % (WEB_DAIRYAUSTRALIA_PATH, 'latest_production/2016_04_22')
#         
#         # scrape html
#         all_years = ['2014', '2015', '2016']
#          
#         '''cheese production'''
#         data_tmp = []
#         data = []
#         with open(dest_path+'CheeseProductionJanuary2016s.html', 'r') as f:
#             lines = f.readlines()
#             products = [l.strip('\n').split('>')[1].split('<')[0] for l in lines[9:17]]
#             row = []
#             for line in lines[41:]:
#                 line = line.strip('\n').strip('<b>').strip('</b>').strip('<br>').strip('</')
#                   
#                 if 'Year Total' in line:
#                     data_tmp.append(row)
#                     break 
#                   
#                 if '%' in line and ' ' not in line:
#                     continue
#                   
#                 if '%' in line and ' ' in line:
#                     row.append(line.split(' ')[0])
#                     continue
#                   
#                 try:
#                     month = datetime.strptime(line, '%B')
#                 except:
#                     row.append(line.replace(',',''))
#                 else:
#                     data_tmp.append(row)
#                     row = []
#                     row.append(line)
#                       
#         data_tmp = data_tmp[1:]
#         for d in data_tmp:
#             month = datetime.strptime(d[0], '%B')
#             month = datetime.strftime(month, '%m')
#               
#             data_row = d[1:d.index('YTD')]
#             if len(data_row) == 8:
#                 for d_r in data_row:
#                     record = [all_years[1], month, all_years[1]+month,'Australia',products[data_row.index(d_r)],d_r,'tonnes']
#                     data.append(record)
#                 continue
#           
#             elif int(month) in range(7,13):
#                 years = all_years[:2]
#                 #continue
#             elif int(month) in range(1,7) and len(data_row) == 16:
#                 years = all_years[1:]
#                 #continue
#  
#             d_r = 0
#             while d_r < len(products):
#                 record = [years[0], month, years[0]+month,'Australia',products[d_r],data_row[d_r*2],'tonnes']
#                 #print record
#                 data.append(record)
#                 record = [years[1], month, years[1]+month,'Australia',products[d_r],data_row[d_r*2+1],'tonnes']
#                 #print record
#                 data.append(record)
#                 d_r = d_r+1
#           
#         #save_to_file('%sproduction_cheese.csv' % dest_path,data)
#          
#         '''production by type'''
#         data_tmp = []
#         data = []
#         with open(dest_path+'ProductionJanuary2016s.html', 'r') as f:
#             lines = f.readlines()
#             products = [l.strip('\n').split('>')[1].split('<')[0] for l in lines[8:15]]
#             row = []
#             for line in lines[36:]:
#                 line = line.strip('\n').strip('<b>').strip('</b>').strip('<br>').strip('</')
#                   
#                 if 'Year Total' in line:
#                     data_tmp.append(row)
#                     break
#                   
#                 if '%' in line:
#                     continue
#                 try:
#                     month = datetime.strptime(line, '%B')
#                 except:
#                     row.append(line.replace(',',''))
#                 else:
#                     data_tmp.append(row)
#                     row = []
#                     row.append(line)
#                       
#         data_tmp = data_tmp[1:]
#         for d in data_tmp:
#               
#             month = datetime.strptime(d[0], '%B')
#             month = datetime.strftime(month, '%m')
#               
#             data_row = d[1:d.index('YTD')]
# 
#             if len(data_row) == 7:
#                 for d_r in data_row:
#                     record = [all_years[1], month, all_years[1]+month,'Australia',products[data_row.index(d_r)],d_r,'tonnes']
#                     data.append(record)
#                 continue
#           
#             elif int(month) in range(7,13):
#                 years = all_years[:2]
#             elif int(month) in range(1,7) and len(data_row) == 14:
#                 years = all_years[1:]
#               
#             d_r = 0
#             while d_r < len(products):
#                 record = [years[0], month, years[0]+month,'Australia',products[d_r],data_row[d_r*2],'tonnes']
#                 #print record
#                 data.append(record)
#                 record = [years[1], month, years[1]+month,'Australia',products[d_r],data_row[d_r*2+1],'tonnes']
#                 #print record
#                 data.append(record)
#                 d_r = d_r+1
#       
#         save_to_file('%sproduction_type.csv' % dest_path,data)

        print 'Finished scraping at %s.' % (datetime.now())
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['dairyaustralia_all.py'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('monthly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['dairyaustralia_all.py'],[success_msg]]
        save_error_to_log('monthly', msg_list)

if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)
    
