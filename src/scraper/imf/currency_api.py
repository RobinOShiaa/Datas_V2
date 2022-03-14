'''
Created on 21 Nov 2016

@author: Suzanne
'''
from datas.function.function import create_directory, save_error_to_log
from datas.web.path import DOWNLOAD_PATH, WEB_IMF_PATH
import xml.etree.ElementTree as ET
import csv
import os, sys, time
from datetime import datetime, timedelta
from datas.web.scraper import WebScraper
from datas.db.manager import DBManager, RAW_DB_NAME, HOST, USERNAME, PASSWORD

def scrape(db_params):
    try:
        print 'Start scraping at %s...' % datetime.now()
        # get the latest data date from DB
        dbm = DBManager(db_params[0], db_params[1], db_params[2], db_params[3])
        sql = ('select max(date) as max_date from imf_currency '
               'group by currency order by max_date asc limit 1;')
        date_from = dbm.get_latest_date_record(sql)
         
         
        if not date_from:
            date_from = "01/01/1994"
            date_from = datetime.strptime(date_from, '%d/%m/%Y')
        else:
         
            date_from = date_from[0]
            date_from += timedelta(days=1)
        del dbm
        
        #represents 01-01-2016
        start_date_num = 635872032000000000 
        start_date_dt = datetime.strptime('01-01-2016','%d-%m-%Y')

        loop_date_dt = start_date_dt
        loop_date_num = start_date_num
        
        today_dt = datetime.now()
        
        while loop_date_dt < today_dt:
            loop_date_num = loop_date_num+864000000000
            loop_date_dt = loop_date_dt+ timedelta(days=1)

        date_to = loop_date_num
        date_from = start_date_num
        
        print date_to
        print date_from
        #636152832000000000
        
        my_str='&P=DateRange&Fr=%s&To=%s&CF=UnCompressed&CUF=Period&DS=Ascending&DT=NA' % (str(date_from),str(date_to))
        
        url = ('http://www.imf.org/external/np/fin/ert/GUI/Pages/Report.aspx?CT=%27DZA%27,%27AUS%27,%27AUT%27,%27BHR%27,'\
               '%27BEL%27,%27BWA%27,%27BRA%27,%27BRN%27,%27CAN%27,%27CHL%27,%27CHN%27,%27COL%27,%27CYP%27,%27CZE%27,%27DNK%27,'\
               '%27EST%27,%27EMU%27,%27FIN%27,%27FRA%27,%27DEU%27,%27GRC%27,%27HUN%27,%27ISL%27,%27IND%27,%27IDN%27,%27IRN%27,'\
               '%27IRL%27,%27ISR%27,%27ITA%27,%27JPN%27,%27KAZ%27,%27KOR%27,%27KWT%27,%27LBY%27,%27LUX%27,%27MYS%27,%27MLT%27,'\
               '%27MUS%27,%27MEX%27,%27NPL%27,%27NLD%27,%27NZL%27,%27NOR%27,%27OMN%27,%27PER%27,%27PHL%27,%27PAK%27,%27POL%27,'\
               '%27PRT%27,%27QAT%27,%27RUS%27,%27SMR%27,%27SAU%27,%27SGP%27,%27SVK%27,%27SVN%27,%27ZAF%27,%27ESP%27,%27LKA%27,'\
               '%27SWE%27,%27CHE%27,%27TUN%27,%27THA%27,%27TTO%27,%27URY%27,%27ARE%27,%27GBR%27,%27USA%27,%27VEN%27&EX=SDRC')
        
        url = url+my_str
       
        scraper = WebScraper('Chrome')
        scraper.open(url)
        scraper.click_button('xpath', '//a[@href="ReportData.aspx?Type=TSV"]') # downloads as .tsv
        time.sleep(5)
        dir_title = datetime.now().strftime('%Y_%m_%d')
        dir_path = '%scurrency\\' % WEB_IMF_PATH
        dir_path = create_directory(dir_path, dir_title)
        dest_file = '%sExchange_Rate_Report_api.csv' % (dir_path)
         
        source_file = '%s\\Exchange_Rate_Report.tsv' % DOWNLOAD_PATH
        csv.writer(file(dest_file, 'wb')).writerows(csv.reader(open(source_file), delimiter="\t"))
        os.remove(DOWNLOAD_PATH+'Exchange_Rate_Report.tsv')
        scraper.close() 
        print 'Finish scraping at %s.' % datetime.now()
    except Exception as err:
        exc_info = sys.exc_info()
        error_msg = 'auto_run() scrape error:\n'
        msg_list = [['imf.currency_api.py'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
        print msg_list
        save_error_to_log('daily', msg_list)
    else:
        success_msg = 'auto_run() scraped successfully\n'
        msg_list = [['imf.currency_api.py'],[success_msg]]
        save_error_to_log('daily', msg_list)


if __name__ == '__main__':
    db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
    scrape(db_params)


'''
dir_title = datetime.now().strftime('%Y_%m_%d')
dir_path = '%scurrency\\' % WEB_IMF_PATH
dir_path = create_directory(dir_path, dir_title)
dest_file = '%sExchange_Rate_Report.csv' % (dir_path)
source_file = '%s\\Exchange_Rate_Report.xls' % DOWNLOAD_PATH

tree = ET.parse(source_file)
root = tree.getroot()
# open a file for writing

Resident_data = open(dest_file, 'w')

# create the csv writer object

csvwriter = csv.writer(Resident_data)
resident_head = []

count = 0
for member in root.findall('Resident'):
    resident = []
    address_list = []
    if count == 0:
        name = member.find('Name').tag
        resident_head.append(name)
        PhoneNumber = member.find('PhoneNumber').tag
        resident_head.append(PhoneNumber)
        EmailAddress = member.find('EmailAddress').tag
        resident_head.append(EmailAddress)
        Address = member[3].tag
        resident_head.append(Address)
        csvwriter.writerow(resident_head)
        count = count + 1

    name = member.find('Name').text
    resident.append(name)
    PhoneNumber = member.find('PhoneNumber').text
    resident.append(PhoneNumber)
    EmailAddress = member.find('EmailAddress').text
    resident.append(EmailAddress)
    Address = member[3][0].text
    address_list.append(Address)
    City = member[3][1].text
    address_list.append(City)
    StateCode = member[3][2].text
    address_list.append(StateCode)
    PostalCode = member[3][3].text
    address_list.append(PostalCode)
    resident.append(address_list)
    csvwriter.writerow(resident)
Resident_data.close()'''
