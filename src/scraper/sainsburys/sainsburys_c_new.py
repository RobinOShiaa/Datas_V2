# -*- coding: utf-8 -*-
'''

Date Created: 15 Jul 2016
Author: Cliodhna Harrison

'''

import requests
import time
from datetime import datetime
import sys
from datas.db.manager import DBManager
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import create_directory, save_error_to_log
from datas.web.path import WEB_SAINSBURYS_PATH
from datas.web.scraper import WebScraper

def scrape(db_params):

	print 'Start scraping at %s...' % datetime.now()
	# get the latest data date from DB
	dbm = DBManager(db_params[0], db_params[1], db_params[2], db_params[3])
	sql = ('select max(date) as max_date from pig333_pig_price '
	'group by geo order by max_date asc limit 1;')
	date_from = dbm.get_latest_date_record(sql)
	date_from = date_from[0]
	del dbm

	dir_title = datetime.now().strftime('%Y_%m_%d')
	dir_path = '%ssainsburys\\' % WEB_SAINSBURYS_PATH

	links_url = 'http://www.sainsburys.co.uk/shop/gb/groceries'
	
	browser = WebScraper('Chrome')
	browser.web_driver.maximize_window()
	browser.open(links_url)
	time.sleep(3)
	urls = []
	i = 1
	#count number of links in primary navigation
	list_primary_nav = browser.find_elements('xpath', '//*[@id="groceriesNav"]/div/ul/li/a')
	num_primary_nav = len(list_primary_nav)
	while i <= num_primary_nav:
		link = browser.find_element("xpath", '//*[@id="groceriesNav"]/div/ul/li[{}]/a'.format(i))
		link = link.get_attribute("href")
		urls.append(link)
		i += 1
		
	newdir_path = create_directory(dir_path, dir_title)
	
	for url in urls:
		#Fruit & veg // Meat & fish // Dairy // Chilled etc
		browser = WebScraper('Chrome')
		browser.web_driver.maximize_window()
		browser.open(url)
		time.sleep(3)
		
		urls_underline = []
		i = 1
		list_secondary_nav = browser.find_elements('xpath', '//*[@id="content"]/div[2]/div[1]/ul/li/a')
		num_secondary_nav = len(list_secondary_nav)
		while i <= num_secondary_nav:
			link = browser.find_element("xpath", '//*[@id="content"]/div[2]/div[1]/ul/li[{}]/a'.format(i)).get_attribute("href")
			urls_underline.append(link)
			i += 1
			
		
		for url_2 in urls_underline:
			#Top Sellers // Carb alternatives // Flowers & Plants
			browser = WebScraper('Chrome')
			browser.web_driver.maximize_window()
			browser.open(url_2)
			try:
				title = browser.find_element('xpath', '//*[@id="resultsHeading"]')
				product_pages = []
				list_products_nav = browser.find_elements('xpath', '//*[@class="productInfo"]/div/h3/a')
				num_products_nav = len(list_products_nav)
				for link in list_products_nav:
					link = link.get_attribute('href')
					product_pages.append(link)
				title = title.text
				file_path = newdir_path + str(title) + ".csv"
				out_file = open(file_path, 'a')
				out_file.write(url_2 + ", \n")
				
				try:
					next_button = browser.find_element('xpath', '//*[@id="productLister"]/div[1]/ul[2]/li[4]/a')
					next_link = next_button.get_attribute("href")
					next = True
				except:
					next = False
				
				
				while next == True:
					for url_3 in product_pages:
						browser = WebScraper('Chrome')
						browser.web_driver.maximize_window()
						browser.open(url_3)
						product_name = browser.find_element('xpath', '//*[@id="content"]/div[2]/div[2]/div/div[1]/h1')
						product_name = product_name.text.replace(",", " ")
						price_per_unit = browser.find_element('xpath', '//*[@class="pricePerUnit"]').text
						price_per_measure = browser.find_element('xpath', '//*[@class="pricePerMeasure"]').text
						price_per_m = price_per_measure.encode('ascii', 'replace')
						price_per_u = price_per_unit.encode('ascii', 'replace')
						content = product_name + ", " + price_per_m + ", " + price_per_u + ",\n "
						out_file.write(content)
						browser.close()
						print "product finished"
					
					browser = WebScraper('Chrome')
					browser.web_driver.maximize_window()
					browser.open(next_link)
					product_pages = []
					list_products_nav = browser.find_elements('xpath', '//*[@class="productInfo"]/div/h3/a')
					num_products_nav = len(list_products_nav)
					for link in list_products_nav:
						link = link.get_attribute('href')
						product_pages.append(link)
					try:
						next_button = browser.find_element('xpath', '//*[@id="productLister"]/div[1]/ul[2]/li[4]/a')
						next_link = next_button.get_attribute("href")
						next = True
					except:
						next = False
				
				for url_6 in product_pages:
					browser = WebScraper('Chrome')
					browser.web_driver.maximize_window()
					browser.open(url_6)
					product_name = browser.find_element('xpath', '//*[@id="content"]/div[2]/div[2]/div/div[1]/h1')
					product_name = product_name.text.replace(",", " ")
					price_per_unit = browser.find_element('xpath', '//*[@class="pricePerUnit"]').text
					price_per_measure = browser.find_element('xpath', '//*[@class="pricePerMeasure"]').text
					price_per_m = price_per_measure.encode('ascii', 'replace')
					price_per_u = price_per_unit.encode('ascii', 'replace')
					content = product_name + ", " + price_per_m + ", " + price_per_u + ",\n "
					out_file.write(content)
					browser.close()
					print "product finished"
					
				out_file.close()
				
			except:
				browser = WebScraper('Chrome')
				browser.web_driver.maximize_window()
				browser.open(url_2)
				urls_tertiary = []
				i = 1
				list_tertiary_nav = browser.find_elements('xpath', '//*[@id="content"]/div[2]/div[1]/ul[2]/li/a')
				num_tertiary_nav = len(list_tertiary_nav)
				while i <= num_tertiary_nav:
					link = browser.find_element("xpath", '//*[@id="content"]/div[2]/div[1]/ul[2]/li[{}]/a'.format(i)).get_attribute("href")
					urls_tertiary.append(link)
					i += 1

				for url_4 in urls_tertiary:
					browser = WebScraper('Chrome')
					browser.web_driver.maximize_window()
					browser.open(url_4)
					product_pages = []
					i = 1
					list_products_nav = browser.find_elements('xpath', '//*[@class="productLister gridView"]/li/div/div/div/h3/a')
					num_products_nav = len(list_products_nav)
					while i <= num_products_nav:
						link = browser.find_element("xpath", '//*[@class="productLister gridView"]/li[{}]/div/div/div/h3/a'.format(i)).get_attribute("href")
						product_pages.append(link)
						i += 1
					title = browser.find_element('xpath', '//*[@id="resultsHeading"]')
					title = title.text
					file_path = newdir_path + str(title) + ".csv"
					out_file = open(file_path, 'a')
					out_file.write(url_4)
					
					try:
						next_button = browser.find_element('xpath', '//*[@id="productLister"]/div[1]/ul[2]/li[4]/a')
						next_link = next_button.get_attribute("href")
						next = True
					except:
						next = False
				
						
					while next == True:
						for url_5 in product_pages:
							browser = WebScraper('Chrome')
							browser.web_driver.maximize_window()
							browser.open(url_5)
							product_name = browser.find_element('xpath', '//*[@id="content"]/div[2]/div[2]/div/div[1]/h1')
							product_name = product_name.text.replace(",", " ")
							price_per_unit = browser.find_element('xpath', '//*[@class="pricePerUnit"]').text
							price_per_measure = browser.find_element('xpath', '//*[@class="pricePerMeasure"]').text
							price_per_m = price_per_measure.encode('ascii', 'replace')
							price_per_u = price_per_unit.encode('ascii', 'replace')
							content = product_name + ", " + price_per_m + ", " + price_per_u + ",\n "
							out_file.write(content)
							browser.close()
							print "product finished"
						
						r = requests.get(url=next_link, verify=False)
						browser = WebScraper('Chrome')
						browser.web_driver.maximize_window()
						browser.open(next_link)
						product_pages = []
						i = 1
						list_products_nav = browser.find_elements('xpath', '//*[@class="productLister gridView"]/li/div/div/div/h3/a')
						num_products_nav = len(list_products_nav)
						while i <= num_products_nav:
							link = browser.find_element("xpath", '//*[@class="productLister gridView"]/li[{}]/div/div/div/h3/a'.format(i)).get_attribute("href")
							product_pages.append(link)
							i += 1
						try:
							next_button = browser.find_element('xpath', '//*[@id="productLister"]/div[1]/ul[2]/li[9]/a')
							next = True
						except:
							next = False
					
				
					for url_6 in product_pages:
						browser = WebScraper('Chrome')
						browser.web_driver.maximize_window()
						browser.open(url_6)
						product_name = browser.find_element('xpath', '//*[@id="content"]/div[2]/div[2]/div/div[1]/h1')
						product_name = product_name.text.replace(",", " ")
						price_per_unit = browser.find_element('xpath', '//*[@class="pricePerUnit"]').text
						price_per_measure = browser.find_element('xpath', '//*[@class="pricePerMeasure"]').text
						price_per_m = price_per_measure.encode('ascii', 'replace')
						price_per_u = price_per_unit.encode('ascii', 'replace')
						content = product_name + ", " + price_per_m + ", " + price_per_u + ",\n "
						out_file.write(content)
						browser.close()
						print "product finished"
						
				print "page finished"	
				out_file.close()
				browser.close()
			
	print 'Finish scraping at %s.' % datetime.now()
	browser.close()


if __name__ == '__main__':
	db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
	scrape(db_params)