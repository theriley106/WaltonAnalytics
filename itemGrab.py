import os
import requests
import random
import threading
import json
import csv
import sys
import bs4
import time
import subprocess
import re
lock = threading.Lock()
STARTTIME = time.time()
TIMEOUT = 10
Proxies = [{}]
THREADS = 30
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

def convertSKUToUPC(sku):
	try:
		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
		res = requests.get('https://brickseek.com/walmart-inventory-checker/?sku={}'.format(sku), headers=headers)
		page = bs4.BeautifulSoup(res.text, 'lxml')
		upc = str(page).partition('upc=')[2].partition('"')[0]
		print("Converted SKU: {} to UPC: {}".format(sku, upc))
		return upc
	except:
		print("Converting to UPC failed.")
		return raw_input("Manually type item UPC: ")

def searchStoreByUPC(store, UPC):
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	try:
		a = {}
		res = requests.get("https://search.mobile.walmart.com/v1/products-by-code/UPC/{}?storeId={}".format(UPC, store), headers=headers).json()
		a['Price'] = res['data']['inStore']['price']['priceInCents']
		a['Quantity'] = res['data']['inStore']['inventory']['quantity']
		a['Store'] = store
		return a
	except Exception as exp:
		return None


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
	print res
	try:
		a["Price"] = int((GrabElement(str(res), 'priceInCents')))
	except:
		pass

	a["Quantity"] = (GrabElement(str(res), 'quantity'))
	return a

def grabTerraFirma(store, SKU):
	headers = {
	    'pragma': 'no-cache',
	    'content-type': 'application/json',
	    'accept': '*/*',
	    'cache-control': 'no-cache',
	    'authority': 'www.walmart.com',
	    'referer': 'https://www.walmart.com/product/{}/sellers'.format(SKU),
	}

	params = (
	    ('rgs', 'OFFER_PRODUCT,OFFER_INVENTORY,OFFER_PRICE,VARIANT_SUMMARY'),
	)

	data = '{{"itemId":"{}","paginationContext":{{"selected":false}},"storeFrontIds":[{{"usStoreId":{},"preferred":false,"semStore":false}}]}}'.format(SKU, store)

	response = requests.post('https://www.walmart.com/terra-firma/fetch', headers=headers, params=params, data=data, timeout=10)
	return returnPricing(response.json())



def returnPricing(terrafirmaDoc):
	for key, value in terrafirmaDoc['payload']['offers'].items():
		try:
			price = terrafirmaDoc['payload']['offers'][key]['pricesInfo']['priceMap']['CURRENT']['price']
			store = terrafirmaDoc['payload']['offers'][key]['fulfillment']['pickupOptions'][0]['storeId']
			quantity = terrafirmaDoc['payload']['offers'][key]['fulfillment']['pickupOptions'][0]['availableQuantity']
			return {"Store": store, "Price": price, "Quantity":quantity}

			#a["Store"] = terrafirmaDoc['payload']['offers'][key]['fulfillment']['pickupOptions']['storeId']
			#a["Quantity"] = terrafirmaDoc['payload']['offers'][key]['fulfillment']['pickupOptions']['availableQuantity']
			#a["Price"] = terrafirmaDoc['payload']['offers'][key]['pricesInfo']['priceMap']['CURRENT']['price']
		except Exception as exp:
			#print exp
			pass

def chunks(l, n):
	for i in xrange(0, len(l), n):
		yield l[i:i + n]

def searchSKU(storeList, UPC):
	for store in storeList:
		if (time.time() - STARTTIME) < (60*TIMEOUT):
			try:
				suggestions_list = random.choice(listOfStores)
				newData = searchStoreByUPC(store, UPC)
				if newData != None:
					newData["Price"]
					lock.acquire()
					print {"Store": store, "Price": newData["Price"], "Quantity": newData["Quantity"]}
					PRIMARYDICT.append({"UPC": UPC, "Store": store, "Price": int(newData["Price"]), "Quantity": newData["Quantity"]})
					lock.release()
			except Exception as exp:
				pass
		else:
			return

def saveToCSV(listVar, UPC):
	with open("{}.csv".format(UPC), "w") as fp:
		wr = csv.writer(fp, dialect='excel')
		list1 = ["Store", "Price", "Quantity"]
		wr.writerow(list1)
		wr.writerow([""])
		for listItem in listVar:
			list1 = [listItem["Store"], '${:,.2f}'.format(int(listItem["Price"] * .01)), listItem["Quantity"]]
			wr.writerow(list1)

if __name__ == '__main__':
	#val = grabTerraFirma('5751', '54594253')
	#returnPricing(val)

	listOfStores = GrabAllStoreNumbers()

	SKU = raw_input("Input SKU: ")
	UPC = convertSKUToUPC(SKU)
	partListOfStores = chunks(listOfStores, int(len(listOfStores)/THREADS))
	threads = [threading.Thread(target=searchSKU, args=(stores, UPC)) for stores in partListOfStores]
	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()
	if len(PRIMARYDICT) > 3:
		PRIMARYDICT = sorted(PRIMARYDICT, key=lambda k: k['Price'])
		print("\n\n\nLowest:\nSTORE: {}\nPRICE: {}\nQUANTITY: {}\n\n\n".format(PRIMARYDICT[0]["Store"], '${:,.2f}'.format(int(PRIMARYDICT[0]["Price"] * .01)), abs(int(PRIMARYDICT[0]["Quantity"]))))
		saveToCSV(PRIMARYDICT, SKU)
		print("Saved Inventory Information to {}.csv\n".format(SKU))
		print("Scan Completed in {} Seconds".format(time.time() - STARTTIME))
		print("UPC: {}".format(UPC))
	else:
		print("Item Stock Too Low")
