import os
import requests
import main
import random
import threading
import json
import csv
import sys
import time
lock = threading.Lock()
STARTTIME = time.time()
TIMEOUT = 10
Proxies = [{}]
THREADS = 20
PRIMARYDICT = []

def GrabAllStoreNumbers():
	ListOfStores = []
	with open('Walmarts.csv', 'r') as f:
		reader = csv.reader(f)
		your_list = list(reader)
	for line in your_list:
		if 'Walmart Supercenter' in str(line[1]):
			ListOfStores.append(line[0])
	return ListOfStores

def GrabElement(json, element):
	json = json.partition(str(element) + '":')[2]
	json = json.partition(',')[0]
	if '"' in str(json):
		json = json.replace('"', '')
	if '{' in str(json):
		json = json.replace('{', '')
	if '}' in str(json):
		json = json.replace('}', '')
	return json

def SearchStore(store, SKU):
	a = {}
	a['Store'] = str(store)
	data = {
			'authority': 'www.walmart.com',
			'method': 'POST',
			'path': '/store/ajax/search',
			'scheme': 'https',
			'accept' : 'application/json, text/javascript, */*; q=0.01',
			'accept-encoding' : 'gzip, deflate, br',
			'accept-language' : 'en-US,en;q=0.8',
			'content-length' : '55',
			'content-type' : 'application/x-www-form-urlencoded; charset=UTF-8',
			'origin' : 'https://www.walmart.com',
			'referer' : 'https://www.walmart.com/store/{}/search?query={}'.format(store, SKU),
			'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
			'x-requested-with': 'XMLHttpRequest',
			"searchQuery":"store={}&query={}".format(store, SKU),


			}

	url = "https://www.walmart.com/store/ajax/search"
	res = requests.post(url, data=data, proxies=random.choice(Proxies))
	res = res.json()
	try:
		a["Price"] = int((GrabElement(str(res), 'priceInCents')))
	except: 
		pass

	a["Quantity"] = (GrabElement(str(res), 'quantity'))
	return a


def chunks(l, n):
	for i in xrange(0, len(l), n):
		yield l[i:i + n]

def searchSKU(storeList, sku):
	for store in storeList:
		if (time.time() - STARTTIME) < (60*TIMEOUT):
			try:
				suggestions_list = random.choice(listOfStores)
				newData = SearchStore(store, sku)
				newData["Price"]
				lock.acquire()
				print {"Store": store, "Price": newData["Price"], "Quantity": newData["Quantity"]}
				PRIMARYDICT.append({"SKU": sku, "Store": store, "Price": newData["Price"], "Quantity": newData["Quantity"]})
				lock.release()
			except Exception as exp:
				pass
		else:
			return

def saveToCSV(listVar):
	with open("{}.csv".format(listVar[0]["SKU"]), "w") as fp:
		wr = csv.writer(fp, dialect='excel')
		list1 = ["Store", "Price", "Quantity"]
		wr.writerow(list1)
		wr.writerow([""])
		for listItem in listVar:
			list1 = [listItem["Store"], '${:,.2f}'.format(int(listItem["Price"]) * .01), listItem["Quantity"]]
			wr.writerow(list1)

listOfStores = GrabAllStoreNumbers()

SKU = raw_input("Input SKU: ")

partListOfStores = chunks(listOfStores, int(len(listOfStores)/THREADS))
threads = [threading.Thread(target=searchSKU, args=(stores, SKU)) for stores in partListOfStores]
for thread in threads:
	thread.start()
for thread in threads:
	thread.join()
PRIMARYDICT = sorted(PRIMARYDICT, key=lambda k: k['Price']) 
print("\n\n\nLowest:\nSTORE: {}\nPRICE: {}\nQUANTITY: {}".format('${:,.2f}'.format(PRIMARYDICT[0]["Store"], int(PRIMARYDICT[0]["Price"]) * .01, abs(int(PRIMARYDICT[0]["Quantity"])))))
saveToCSV(PRIMARYDICT)
print("Saved Information to {}.csv".format(PRIMARYDICT[0]['SKU']))	
print("Scan Completed in {} Seconds".format(time.time() - STARTTIME))