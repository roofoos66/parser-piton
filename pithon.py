import requests

from bs4 import BeautifulSoup


import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import csv

from multiprocessing import Pool
urls = [
	'https://cs7.pikabu.ru/post_img/2017/11/14/3/1510631664167520623.jpg'
	'https://cs8.pikabu.ru/post_img/2017/11/14/4/1510637913128867791.jpg'
]

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

def get_all_catalog(html):
	soup = BeautifulSoup(html, 'lxml')

	cat = soup.find('table', class_='jshop').find_all('td', class_='')

	cat_links = []

	for td in cat:
		a = td.find('a').get('href')
		link = 'http://optimus-cctv.ru' + a
		cat_links.append(link)

		data = {'links': cat_links}
	return data

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
	with open('csv.csv', 'a') as f:
		writer = csv.writer(f)

		writer.writerow( (data['name'],data['opis']) )

		print(data['name'],['opis'],'parsed')

def make_all(url):
	html = get_html(url)
	data = get_page_data(html)
	# write_csv(data)

def get_file(url):
	r = requests.get(url, stream=True)
	return r

def get_name(url):
	name = url.split('/')[-1]
	return name   		

def save_image(name, file_object):
	with open(name, 'w') as f:
		for chunk in file_object.iter_content(8192):
			f.write(chunk)

def main():
	for url in urls:
		save_image(get_name(url),get_file(url))

	url = 'http://optimus-cctv.ru/catalog/'
	all_catalog = get_all_catalog(get_html(url))
	# i = 1
	# while i <= len(all_catalog['links']):
	# 		y = all_catalog['links'][i]
	# 		all_links = get_all_links( get_html(y) )
	# 		print(y)
	# 		p = Pool(40)
	# 		p.map(make_all, all_links)
	# 		i += 1

	
	# print('\n'.join(all_catalog['links']))

	# all_links = get_all_links( get_html(y) )
	# print(all_links)
	# for index, url in enumerate(all_links):
	# 	html = get_html(url)
	# 	data = get_page_data(html)
	# 	write_csv(data)
	# 	# print(url)
	# 	print(index)

	# p = Pool(40)
	# p.map(make_all, all_links)
	# p.map(make_all, all_catalog)


if __name__ == '__main__':
	main()
