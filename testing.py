import csv
import grequests
import requests

def GrabAllStoreNumbers():
	ListOfStores = []
	with open('Walmarts.csv', 'r') as f:
		reader = csv.reader(f)
		your_list = list(reader)
	for line in your_list:
		if 'Walmart Supercenter' in str(line[1]):
			ListOfStores.append(line[0])
	return ListOfStores

a = GrabAllStoreNumbers()
session = requests.Session()
req = []
for i in a:
	sku = '123353374'
	store = i

	url = 'https://search.mobile.walmart.com/search?query={}&store={}&size=20&mode=setStore&offset=0&searchType=entered'.format(sku, store)
	req.append(grequests.get(url, session=session))

grequests.map(req, size=50)
for r in req:
    print("done")