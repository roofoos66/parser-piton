import requests

from bs4 import BeautifulSoup


import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import csv

from multiprocessing import Pool

def get_html(url):
	r = requests.get(url)
	return r.text

def get_all_links(html):
	soup = BeautifulSoup(html, 'lxml')

	tds = soup.find('table', class_='list_product').find_all('td', class_='block_product')

	links = []

	for td in tds:
		a = td.find('a').get('href')
		link = 'http://optimus-cctv.ru' + a
		links.append(link)

	return links	

def get_page_data(html):
	soup = BeautifulSoup(html, 'lxml')

	try:
		name = soup.find('h1', class_='').text.strip()
	except:
		name = ''

	try:
		opis = soup.find('div', class_='cat_price').find('span').text.strip()
	except:
		opis = ''

	data = {'name': name,
		    'opis': opis}

	return data			

def write_csv(data):
	with open('csv3.csv', 'a') as f:
		writer = csv.writer(f)

		writer.writerow( (data['name'],data['opis']) )

		print(data['name'],['opis'],'parsed')

def make_all(url):
	html = get_html(url)
	data = get_page_data(html)
	write_csv(data)


def main():

	url = 'http://optimus-cctv.ru/catalog/ip-videokamery'

	all_links = get_all_links( get_html(url) )

	# for index, url in enumerate(all_links):
	# 	html = get_html(url)
	# 	data = get_page_data(html)
	# 	write_csv(data)
	# 	# print(url)
	# 	print(index)

	p = Pool(40)
	p.map(make_all, all_links)


if __name__ == '__main__':

	main()
