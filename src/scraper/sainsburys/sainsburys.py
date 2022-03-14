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

	dir_title = datetime.now().strftime('%Y_%m_%d')
	dir_path = WEB_SAINSBURYS_PATH
	newdir_path = create_directory(dir_path, dir_title)
	links_url = 'http://www.sainsburys.co.uk/shop/gb/groceries'
	
	browser = WebScraper('Chrome')
	browser.open(links_url)
	browser.web_driver.maximize_window()
	
	time.sleep(3)
	urls = []
	i = 1
	#count number of links in primary (horizontal) navigation
	list_primary_nav = browser.find_elements('xpath', '//*[@id="groceriesNav"]/div/ul/li/a')
	num_primary_nav = len(list_primary_nav)
	while i <= num_primary_nav:
		link = browser.find_element("xpath", '//*[@id="groceriesNav"]/div/ul/li[{}]/a'.format(i))
		link_title = link.text
		link = link.get_attribute("href")
		#Summer promotions are available in other categorys, only creates duplicates
		if "Summer" not in str(link_title):
			urls.append(link)
		i += 1
		
	
	browser.close()
	for url in urls: #horizontal nav links
		print 'level 1 -'+url
		#Fruit & veg // Meat & fish // Dairy // Chilled etc
		browser = WebScraper('Chrome')
		browser.open(url)
		time.sleep(3)
		browser.web_driver.maximize_window()
		
		
		urls_underline = []
		i = 1
		list_secondary_nav = browser.find_elements('xpath', '//*[@id="content"]/div[2]/div[1]/ul/li/a')
		num_secondary_nav = len(list_secondary_nav)
		while i <= num_secondary_nav:
			link = browser.find_element("xpath", '//*[@id="content"]/div[2]/div[1]/ul/li[{}]/a'.format(i)).get_attribute("href")
			urls_underline.append(link)
			i += 1
	
		browser.close()
		for url_2 in urls_underline:
			print 'level 2 -'+url_2
			#Top Sellers // Carb alternatives // Flowers & Plants
			#when there is no further sub-lists from the primary navigation
			browser = WebScraper('Chrome')
			browser.open(url_2)
			browser.web_driver.maximize_window()
			
			#try:
			title = browser.find_element('xpath', '//*[@id="resultsHeading"]').text
			file_path = newdir_path + str(title) + ".csv"
			out_file = open(file_path, 'ab')
				
			out_file.write(url_2 + ",\n")
			product_tags = []
			price_tags = []	
			more_products = True
			while more_products:
				tmp_product_tags = []
				tmp_price_tags = []
				tmp_product_tags = browser.find_elements('xpath', '//*[@id="productLister"]/ul/li/div/div/div/h3/a')
				tmp_price_tags = browser.find_elements('xpath','//*[contains(@id,"addItem_")]/div[1]')
				for t in tmp_product_tags:
					product_tags.append(t.text)
				print len(product_tags)
# 					print len(price_tags)
# 					product_tags.append(tmp_product_tags)
# 					price_tags.append(tmp_price_tags)

				try:
					browser.click_button('xpath', '//li[@class="next"]/a')
					#browser.click_button('xpath', '//*[@id="productLister"]/div[1]/ul[2]/li[4]/a')
						
					print 'turning page'
					time.sleep(5)
					
					#next_button = browser.find_element('xpath', '//*[@id="productLister"]/div[1]/ul[2]/li[4]/a')
			
				except:
					print 'no more products'
					#flatten
# 						product_tags = [item for sublist in product_tags for item in sublist]
# 						price_tags = [item for sublist in price_tags for item in sublist]
# 						print product_tags
# 						i=0
# 						while i < len(product_tags):
# 							row = [product_tags[i].text.replace(',',''), price_tags[i].text.encode('ascii','replace').split(' ')[0], price_tags[i].text.encode('ascii','replace').split(' ')[1]]
# 							print row
# 							out_file.write(','.join(row)+'\n')
# 							i = i+1
					more_products = False
					#continue
# 					else:
# 						pass
					#continue
				'''product_pages = []
				list_products_nav = browser.find_elements('xpath', '//*[@class="productInfo"]/div/h3/a')
				num_products_nav = len(list_products_nav)
				for link in list_products_nav:
					link = link.get_attribute('href')
					product_pages.append(link)
				
				file_path = newdir_path + str(title) + ".csv"
				out_file = open(file_path, 'a')
				out_file.write(url_2 + ",\n")
				
				try:
					next_button = browser.find_element('xpath', '//*[@id="productLister"]/div[1]/ul[2]/li[4]/a')
					next_link = next_button.get_attribute("href")
					next = True
				except:
					next = False
				
				
				while next == True:
					for url_3 in product_pages:
						print 'level 3 -'+url_3
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
						#print "product finished"
					
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
				
				for url_4 in product_pages:
					print 'level 4 -'+url_4
					browser = WebScraper('Chrome')
					browser.web_driver.maximize_window()
					browser.open(url_4)
					product_name = browser.find_element('xpath', '//*[@id="content"]/div[2]/div[2]/div/div[1]/h1')
					product_name = product_name.text.replace(",", " ")
					price_per_unit = browser.find_element('xpath', '//*[@class="pricePerUnit"]').text
					price_per_measure = browser.find_element('xpath', '//*[@class="pricePerMeasure"]').text
					price_per_m = price_per_measure.encode('ascii', 'replace')
					price_per_u = price_per_unit.encode('ascii', 'replace')
					content = product_name + ", " + price_per_m + ", " + price_per_u + ",\n "
					out_file.write(content)
					browser.close()
					#print "product finished"
					
				out_file.close()
				'''
# 			except:
# 				#continue
# 				# when there are additional sub-lists in vertical nav links
# 				#browser = WebScraper('Chrome')
# 				#browser.web_driver.maximize_window()
# 				#browser.open(url_2)
# 				urls_tertiary = []
# 				i = 1
# 				list_tertiary_nav = browser.find_elements('xpath', '//*[@id="content"]/div[2]/div[1]/ul[2]/li/a')
# 				num_tertiary_nav = len(list_tertiary_nav)
# 				while i <= num_tertiary_nav:
# 					link = browser.find_element("xpath", '//*[@id="content"]/div[2]/div[1]/ul[2]/li[{}]/a'.format(i)).get_attribute("href")
# 					urls_tertiary.append(link)
# 					i += 1
# 
# 				for url_5 in urls_tertiary:
# 					print 'level 5 -'+url_5
# 					browser = WebScraper('Chrome')
# 					browser.web_driver.maximize_window()
# 					browser.open(url_5)
# 					title = browser.find_element('xpath', '//*[@id="resultsHeading"]').text
# 					file_path = newdir_path + str(title) + ".csv"
# 					
# 					with open(file_path, 'a') as out_file:
# 						out_file.write(url_5 + ",\n")
# 						
# 						more_products = True
# 						while more_products:
# 							product_tags = browser.find_elements('xpath', '//*[@id="productLister"]/ul/li/div/div/div/h3/a')
# 							price_tags = browser.find_elements('xpath','//*[contains(@id,"addItem_")]/div[1]/p[2]')
# 							with open(file_path, 'a') as out_file:
# 								for i in range(0,len(product_tags)):
# 									out_file.write(product_tags[i].text+','+price_tags[i].text.split('/')[0]+','+price_tags[i].text.split('/')[1])
# 						
# 							try:
# 								browser.click_button('xpath', '//li[@class="next"]/a')
# 								#browser.click_button('xpath', '//*[@id="productLister"]/div[1]/ul[2]/li[4]/a')
# 								
# 								print 'turning page' 
# 								#next_button = browser.find_element('xpath', '//*[@id="productLister"]/div[1]/ul[2]/li[4]/a')
# 					
# 							except:
# 								print 'no more products'
# 								more_products = False
# 								#continue
				
				
				'''product_pages = []
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
				out_file.write(url_5+'\n')
				
				try:
					next_button = browser.find_element('xpath', '//*[@id="productLister"]/div[1]/ul[2]/li[4]/a')
					next_link = next_button.get_attribute("href")
					next = True
				except:
					next = False
			
					
				while next == True:
					for url_6 in product_pages:
						print 'level 6 -'+url_6
						browser = WebScraper('Chrome')
						browser.open(url_6)
						browser.web_driver.maximize_window()
						
						product_name = browser.find_element('xpath', '//*[@id="content"]/div[2]/div[2]/div/div[1]/h1').text.replace(",", " ")
						#product_name = product_name.text.replace(",", " ")
						price_per_unit = browser.find_element('xpath', '//*[@class="pricePerUnit"]').text
						price_per_measure = browser.find_element('xpath', '//*[@class="pricePerMeasure"]').text
						price_per_m = price_per_measure.encode('ascii', 'replace')
						price_per_u = price_per_unit.encode('ascii', 'replace')
						content = product_name + ", " + price_per_m + ", " + price_per_u + ",\n "
						out_file.write(content)
						browser.close()
						#print "product finished"
					
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
				
			
				for url_7 in product_pages:
					print 'level 7 -'+url_7
					browser = WebScraper('Chrome')
					browser.open(url_7)
					browser.web_driver.maximize_window()
					
					product_name = browser.find_element('xpath', '//*[@id="content"]/div[2]/div[2]/div/div[1]/h1').text
					product_name = product_name.text.replace(",", " ")
					price_per_unit = browser.find_element('xpath', '//*[@class="pricePerUnit"]').text
					price_per_measure = browser.find_element('xpath', '//*[@class="pricePerMeasure"]').text
					price_per_m = price_per_measure.encode('ascii', 'replace')
					price_per_u = price_per_unit.encode('ascii', 'replace')
					content = product_name + ", " + price_per_m + ", " + price_per_u + ",\n "
					out_file.write(content)
					browser.close()

					
			print "page finished "+url_2	
			out_file.close()'''
				browser.close()
			
	print 'Finish scraping at %s.' % datetime.now()
	browser.close()


if __name__ == '__main__':
	db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
	scrape(db_params)