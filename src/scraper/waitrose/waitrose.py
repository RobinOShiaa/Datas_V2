# -*- coding: utf-8 -*-
'''

Date Created: 15 Jul 2016
Author: Cliodhna Harrison

'''

import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime
import sys
from datas.db.manager import DBManager
from datas.db.manager import RAW_DB_NAME, HOST, USERNAME, PASSWORD
from datas.function.function import create_directory, save_error_to_log
from datas.web.path import WEB_WAITROSE_PATH
from datas.web.scraper import WebScraper

def scrape(db_params):

	print 'Start scraping at %s...' % datetime.now()
	# get the latest data date from DB

	dir_title = datetime.now().strftime('%Y_%m_%d')
	dir_path =  WEB_WAITROSE_PATH
	newdir_path = create_directory(dir_path, dir_title)
	
	
	
	links_url = 'http://www.waitrose.com/shop/Browse/Groceries'
	
	r = requests.get(url=links_url, verify=False)
	browser = WebScraper('Chrome')
	browser.web_driver.maximize_window()
	#browser.open(links_url)
	links_soup = BeautifulSoup(r.content, "html.parser")
	time.sleep(10)
	urls = []
	a_links = links_soup.find_all('a', {"class": "category js-category clearfix"})
	for a_link in a_links:
		urls.append("http://www.waitrose.com" + a_link.get('href'))
	
	
	
	for url in urls:
		#try:
		browser.open(url)
		time.sleep(3)
		title = browser.find_element('xpath', '//*[@id="content"]/div/div[2]/h1')
		title = title.text
		file_path = newdir_path + str(title) + ".csv"
		with open(file_path, 'a') as out_file:
			out_file.write(url + ',\n')
		i = 0
		while i < 5:
			browser.scroll_to_bottom()
			time.sleep(3)
			i += 1
			
		html = browser.web_driver.page_source
		soup = BeautifulSoup(html, 'html.parser')
		
		'''
		
		

		urls_underline = []
		a_links = soup.find_all('a', {"class": "category js-category clearfix"})
		for a_link in a_links:
			urls_underline.append("http://www.waitrose.com" + a_link.get('href'))	

		
		
		for url_2 in urls_underline:
			#print url_2
			browser.open(url_2)
			time.sleep(3)
			html = browser.web_driver.page_source
			soup = BeautifulSoup(html, 'html.parser')
			
			menu_aisles = []
			a_links = soup.find_all('a', {"class": "category js-category clearfix"})
			for a_link in a_links:
				menu_aisles.append("http://www.waitrose.com" + a_link.get('href'))

			for url_3 in menu_aisles:
				print url_3
				browser.open(url_3)
				time.sleep(3)
				i = 0
				while i < 5:
					browser.scroll_to_bottom()
					time.sleep(3)
					i += 1
				
				title = browser.find_element('xpath', '//*[@id="content"]/div/div[2]/h1')
				title = title.text
				
			'''	
				
				
				
				
		'''
		sue's code
		'''
		product_cells = soup.find_all('div',{"class": "m-product-cell"})
		#product_names = []
		#volumes = []
		#prices = []
		for p_c in product_cells:
			product=p_c.find('div',{"class": "m-product-details-container"}).find('a',{"class": "m-product-open-details"}).text.replace(',','-')
			try:
				volume = ' '+p_c.find('div',{"class": "m-product-details-container"}).find('div',{"class": "m-product-volume"}).text
			except:
				volume=''
			#print volume
			price = p_c.find('div',{"class": "m-product-price-container"}).find('span',{"class": "price trolley-price"}).text.replace('\n','').replace(' ','')
			#print price
			unit_price = p_c.find('div',{"class": "m-product-price-container"}).find_all('span',{"class": "fine-print"})[1].text
			with open(file_path, 'a') as out_file:
				out_file.write(product.encode('ascii', 'replace')+volume+','+price.encode('ascii', 'replace')+','+unit_price.encode('ascii', 'replace')+'\n')
		
		
		
		'''
		product_tags = browser.find_elements('xpath','*//a[@class="m-product-open-details"]')
		for p in product_tags:
			if p.text != None and p.text!='':
				product_names.append(p.text.encode('ascii', 'replace').replace('\n',''))

		volume_tags = browser.find_elements('class','m-product-volume')
		for v in volume_tags:
			if v.text != None and v.text!='':
				volumes.append(v.text.encode('ascii', 'replace').replace('\n',''))
		price_tags = browser.find_elements('class','m-product-price-container')
		for r in price_tags:
			if r.text != None and r.text!='':
				prices.append(r.text.encode('ascii', 'replace').replace('\n',''))	
		
		file_path = newdir_path + str(title) + ".csv"
		with open(file_path, 'a') as out_file:
			#out_file.write(url_3 + ',\n')
			out_file.write(url + ',\n')
			for i in range(0,len(product_names)):
				out_file.write(product_names[i]+' ')
				try:
					out_file.write(volumes[i]+',')
				out_file.write(prices[i].split('(')[0]+',')
				try:
					out_file.write(prices[i].split('(')[1]+'\n')
				except:
					out_file.write('N/A\n')

				
				product_pages_web = browser.find_elements('xpath', '//*[@class="m-product-cell"]/div/div[1]/a')
				product_pages = [page.get_attribute('href') for page in product_pages_web]
				init = True
				for url_5 in product_pages:
					browser.open(url_5)
					time.sleep(3)
					
					product_title_web = browser.find_element('xpath', '//*[@class="hero"]/div[1]/h1/em')
					product_title = product_title_web.text
					product_title = product_title.replace(",", "")
					
					try:
						amounts_web = browser.find_element('xpath', '//*[@class="hero"]/div/h1/span')
						amount = amounts_web.text
					except:
						amount = 'N/A'
					
					price_web = browser.find_element('xpath', '//*[@class="price"]').text
					file_path = newdir_path + str(title) + ".csv"
					out_file = open(file_path, 'a')
					if init:
						out_file.write(url_3 + ',\n')
					init = False
					price = price_web.split('(')[0]
					price = price.replace('\n', ' ')
					try:
						price_per = price_web.split('(')[1]
					except: 
						price_per = 'N/A'
					
					product_title = product_title.encode('ascii', 'replace')
					price = price.encode('ascii', 'replace')
					price_per = price_per.encode('ascii', 'replace')
					content = product_title +", " + price + ", " + amount + ", " + price_per + ", \n"
					out_file.write(content)
					print url_5
				
				print "Page finished: "+url_3
				out_file.close()'''
		#except:
	#		print "Error"
	#		continue
				
	print 'Finish scraping at %s.' % datetime.now()
	browser.close()


if __name__ == '__main__':
	db_params = [RAW_DB_NAME, HOST, USERNAME, PASSWORD]
	scrape(db_params)