"""
GDELT Scraper

Created 21 June 2016
"""

import requests
import csv
import sys
from bs4 import BeautifulSoup
from urllib import urlretrieve
from urlparse import urljoin
from datetime import datetime
from datas.db.manager import DBManager
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import create_directory, save_error_to_log, unzip
from datas.web.path import WEB_GDELT_PATH
from datas.web.scraper import WebScraper

def get_data(elements):
	data_list = []
	for element in elements:
		data_list.append(element.text)
		return data_list

def scrape(db_params):
	try:
		print 'Start scraping at %s...' % datetime.now()

		# get the latest data date from DB

		dbm = DBManager(db_params[0], db_params[1], db_params[2], db_params[3])
		sql = ('SELECT load_date FROM datas_gdelt.gdelt_data WHERE id = (SELECT max(id) FROM datas_gdelt.gdelt_data)')
		date_from = dbm.get_latest_date_record(sql)
		date_from = date_from[0]
		del dbm
		#date_from = '2016-06-01'
		dir_title = datetime.now().strftime('%Y_%m_%d')
		dir_path = WEB_GDELT_PATH

		links_url = 'http://data.gdeltproject.org/events/index.html'
		browser = WebScraper('Chrome')
		browser.web_driver.maximize_window()
		browser.open(links_url)

		r = requests.get(url=links_url, verify=False)
		urls = []
		links_soup = BeautifulSoup(r.content, "html.parser")
		urls = links_soup.find_all("a")
		#top 3 links and last link are not data files
		urls = urls[3:-1]
		
		place_num = 0
		filenames = []
		for url in urls:
			filenames.append(url.text)
		
		newdir_path = create_directory(dir_path, dir_title)
		
		#Loops through each url to download each file
		for url in urls:
			href = url.get('href')
			filename = href.rsplit('/', 1)[-1]
			href = urljoin(links_url, href)
			try:
				if len(filename) > 20:
					filename_d = filename[:8]
					filename_date = filename[:8]
					filename_date = datetime.strptime(filename_date,"%Y%m%d")
				elif len(filename) < 11 and len(filename) > 8:
					filename_d = filename[:6]
					filename_date = filename[:6]
					filename_date = datetime.strptime(filename_date,"%Y-%m")
				elif len(filename) < 10:
					filename_d = filename[:4]
					filename_date = filename[:4]
					filename_date = datetime.strptime(filename_date,"%Y")
				else:
					print "Couldn't find date"
				
				#checks that it only downloads files that are not previously downloaded
				if filename_date.date() > date_from:
					file = urlretrieve(href, filename)
					unzip(filename, newdir_path + "\\raw_files")
					file_path = newdir_path + "\\raw_files" + "\\" + str(filename_d) + ".export.csv"
					file_date_print = datetime.strftime(filename_date, "%Y%m%d")
					data_file = open(file_path, "rb")
					convert_raw_file(data_file, newdir_path, href, filename, file_date_print)
					print "Downloaded " + str(filename)
				#else:
					#print "File not wanted"

			except:
				#print('Failed to download')
				continue
		browser.close()
		place_num += 1

		print 'Finish scraping at %s.' % datetime.now()
	except Exception as err:
		exc_info = sys.exc_info()
		error_msg = 'auto_run() scrape error:\n'
		msg_list = [['gdelt_data'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n']]
		print msg_list
		save_error_to_log('weekly', msg_list)
	else:
		success_msg = 'auto_run() scraped successfully\n'
		msg_list = [['gdelt_data'],[success_msg]]
		save_error_to_log('weekly', msg_list)
		
		
def convert_raw_file(data_file, newdir_path, href, filename, file_date_print):
	rows = data_file.readlines()
	filename_output = filename.split(".")
	output_file = str(filename_output[0]) + ".csv"
	csv_file = open(newdir_path + output_file, "w")
	csv_file.write(str(href) + ",\n")
	#Loops through each row of the csv file
	for i, row in enumerate(rows):
		articles = []
		text = row.replace("\t", ",")
		text = " ,".join(text.split(","))
		text = text.split(",")
		location_unsorted = text[30:46]
		locations = []
		location = True
		#Loops through location_unsorted to find any names of cities or countries
		for item in location_unsorted:
			for char in item:
				if str(char).isdigit() == False:
					location = True
				else:
					location = False
					break
			if location == True:
				locations.append(item)
			else:
				continue
		for item in text:
			if "http" in item:
				articles.append(item)
		#headers = "Date," + "CAMEO Code," + "Average Tone," + "Location," + "Load Date," + "\n"
		info = file_date_print + "," + str(text[26]) + "," + str(text[34])+ "," + str("".join(set(locations))) + "," + datetime.strftime(datetime.now(), "%Y-%m-%d")+ "," + str("".join(set(articles))) + ",\n"
		
		csv_file.write(info)

	csv_file.close()
	data_file.close()
		
		
		
		
if __name__ == '__main__':
	db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
	scrape(db_params)    

