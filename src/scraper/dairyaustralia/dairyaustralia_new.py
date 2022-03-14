'''
Created on 11 Apr 2016

@author: Suzanne
20-04-16 Sue: Incorporated into existing scraper
'''
import sys
from datetime import datetime
from datas.web.path import WEB_DAIRYAUSTRALIA_PATH
from datas.function.function import save_to_file, save_error_to_log


def scrape():
    try:
        print 'Start scraping at %s...' % datetime.now()
        #mother_url = 'http://www.dairyaustralia.com.au/Markets-and-statistics/Production-and-sales/Latest-statistics.aspx'
        url = 'http://www.dairyaustralia.com.au/~/media/Documents/Stats%20and%20markets/Production%20and%20sales/Latest%20stats/Prod%20Summary%20January%202016.xls'
        
        file_path = '%slatest_production//2016_07_27//' % WEB_DAIRYAUSTRALIA_PATH
        all_years = ['2014', '2015', '2016']
        
        '''cheese production'''
        data_tmp = []
        data = []
        data_insert = []
        data_update = []
        with open(file_path+'CheeseProductionJanuary2016s.html', 'r') as f:
            lines = f.readlines()
            products = [l.strip('\n').split('>')[1].split('<')[0] for l in lines[9:17]]
            #print products
            row = []
            for line in lines[41:]:
                line = line.strip('\n').strip('<b>').strip('</b>').strip('<br>').strip('</')
                #print line
                 
                if 'Year Total' in line:
                    data_tmp.append(row)
                    break 
                 
                if '%' in line and ' ' not in line:
                    continue
                 
                if '%' in line and ' ' in line:
                    row.append(line.split(' ')[0])
                    continue
                 
                try:
                    month = datetime.strptime(line, '%B')
                except:
                    #print line
                    row.append(line.replace(',',''))
                else:
                    #print line
                    data_tmp.append(row)
                    row = []
                    row.append(line)
                     
        data_tmp = data_tmp[1:]
        for d in data_tmp:
            #print d
            month = datetime.strptime(d[0], '%B')
            month = datetime.strftime(month, '%m')
             
            data_row = d[1:d.index('YTD')]
            #print len(data_row)
            if len(data_row) == 8:
                #print data_row
                for d_r in data_row:
                    record = [all_years[1], month, all_years[1]+month,'Australia',products[data_row.index(d_r)],d_r,'tonnes']
                    data.append(record)
                continue
         
            elif int(month) in range(7,13):
                years = all_years[:2]
                #continue
            elif int(month) in range(1,7) and len(data_row) == 16:
                years = all_years[1:]
                #continue
             
            #print years
            d_r = 0
            while d_r < len(products):
                #print products[d_r],data_row[d_r*2]
                     
                record = [years[0], month, years[0]+month,'Australia',products[d_r],data_row[d_r*2],'tonnes']
                #print record
                data.append(record)
                record = [years[1], month, years[1]+month,'Australia',products[d_r],data_row[d_r*2+1],'tonnes']
                #print record
                data.append(record)
                d_r = d_r+1
         
        save_to_file('%sproduction_cheese.csv' % file_path,data)
        
        '''production by type'''
        data_tmp = []
        data = []
        data_insert = []
        data_update = []
        with open(file_path+'ProductionJanuary2016s.html', 'r') as f:
            lines = f.readlines()
            products = [l.strip('\n').split('>')[1].split('<')[0] for l in lines[8:15]]
            row = []
            for line in lines[36:]:
                line = line.strip('\n').strip('<b>').strip('</b>').strip('<br>').strip('</')
                 
                if 'Year Total' in line:
                    data_tmp.append(row)
                    break
                 
                if '%' in line:
                    continue
                try:
                    month = datetime.strptime(line, '%B')
                except:
                    row.append(line.replace(',',''))
                else:
                    data_tmp.append(row)
                    row = []
                    row.append(line)
                     
        data_tmp = data_tmp[1:]
        for d in data_tmp:
             
            month = datetime.strptime(d[0], '%B')
            month = datetime.strftime(month, '%m')
             
            data_row = d[1:d.index('YTD')]
         
            if len(data_row) == 7:
                for d_r in data_row:
                    record = [all_years[1], month, all_years[1]+month,'Australia',products[data_row.index(d_r)],d_r,'tonnes']
                    data.append(record)
                continue
         
            elif int(month) in range(7,13):
                years = all_years[:2]
            elif int(month) in range(1,7) and len(d) == 15:
                years = years[1:]
             
            d_r = 0
            while d_r < len(products):
                record = [years[0], month, years[0]+month,'Australia',products[d_r],data_row[d_r*2],'tonnes']
                data.append(record)
                record = [years[1], month, years[1]+month,'Australia',products[d_r],data_row[d_r*2+1],'tonnes']
                data.append(record)
                d_r = d_r+1
     
        save_to_file('%sproduction_type.csv' % file_path,data)

    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['dairyaustralia_new.py'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('monthly', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['dairyaustralia_new.py'],[success_msg]]
        save_error_to_log('monthly', msg_list)

if __name__ == '__main__':
    scrape()


