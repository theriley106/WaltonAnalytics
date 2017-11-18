from datetime import datetime
from flatten_json import flatten
from time import gmtime, strftime
import time
import requests
import os
import json
import sys
import random
import csv
reload(sys)
sys.setdefaultencoding('utf-8')
import threading

r = requests.post("http://138.197.123.15:8888/proxies/{}".format(open('./SecretCode.txt').read().strip())).json()
proxies = r["proxies"]
LengthOfProxies = len(proxies)

ListOfStores = ['2266']
directory = strftime('%d%b%Y', gmtime())


if not os.path.exists(directory):
    os.makedirs(directory)



def GrabFromSpreadsheet(spreadsheet):
	with open(spreadsheet, 'r') as f:
		reader = csv.reader(f)
		your_list = list(reader)
	for line in your_list:
		if 'Walmart Supercenter' in str(line[1]):
			ListOfStores.append(line[0])

GrabFromSpreadsheet("{}/static/Walmarts.csv".format(os.getcwd()))



lis = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '*']

def GrabStore():
	StoreChoice = random.choice(ListOfStores)
	ListOfStores.remove(StoreChoice)
	return str(StoreChoice)
def SaveToCSV(store):
	prevsku = len(sku)
	keys = sku[0].keys()
	with open(directory + str(store) + '.csv', 'wb') as output_file:
		dict_writer = csv.DictWriter(output_file, keys)
		dict_writer.writeheader()
		for s in sku:
			data = {key: value for key, value in s.items() if key in keys}
			dict_writer.writerow(data)
	print(store)

def Fin(searchterm, store):
	print searchterm, store
	payload = {"storeId":store,"searchTerm":searchterm,"size":49,"dept":1000,"newIndex":1, 'offset': 0, "query":searchterm,"idx":1}
	res = requests.post('https://www.walmart.com/store/electrode/api/search', data=payload, proxies=random.choice(proxies))
	Quantity = res.json()['result']['totalCount']

	af = 0
	for i in range(0, int(Quantity), 49):
		prevsku = len(sku)
		try:
			payload = {"storeId":store,"searchTerm":searchterm,"size":49,"dept":1000,"newIndex":1, 'offset': i, "query":searchterm,"idx":1}
			print payload
			time.sleep(100)
			res = requests.post('https://www.walmart.com/store/electrode/api/search', data=payload, proxies=random.choice(proxies))
			for results in res.json()["result"]['results']:
				e = {}
				a = flatten(results)
				for key, value in a.items() :
					key = str(str(key)[::-1].partition('_')[0])[::-1]
					e[key] = value
				e['atime'] = str(datetime.now())
				if str(e['upc']) not in ItemsGrabbed:
					sku.append(e)
					ItemsGrabbed.append(e['upc'])
					print(e["WWWItemId"])
					af = 0
				else:
					af = af + 1
		except BaseException as exp:
			print(exp)
			pass
		if af > 1000:
			print('broke thread')
			break

while len(ListOfStores) > 0:
	try:
		ItemsGrabbed = []
		sku = []	
		store = str(GrabStore())
		threads = [threading.Thread(target=Fin, args=(searchterm, store)) for searchterm in lis]
		for thread in threads:
			thread.start()
		for thread in threads:
			thread.join()
		SaveToCSV(store)
	except BaseException as exp:
		print(exp)
		pass


