import requests
import threading
import RandomHeaders
import csv
import time
import random
lock = threading.Lock()

r = requests.post("http://138.197.123.15:8888/proxies/{}".format(open('./SecretCode.txt').read().strip())).json()
Proxies = r["proxies"]

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
			'user-agent' : str(RandomHeaders.LoadHeader()),
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

def GrabAllStoreNumbers():
	ListOfStores = []
	with open('Walmarts.csv', 'r') as f:
		reader = csv.reader(f)
		your_list = list(reader)
	for line in your_list:
		if 'Walmart Supercenter' in str(line[1]):
			ListOfStores.append(line[0])
	return ListOfStores

def ReturnLowestPrice(sku, accounttype='Limitedd'):

	Lis = []

	def FNCN(store, SKU):
		for store in store:
			try:
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
						'user-agent' : str(RandomHeaders.LoadHeader()),
						'x-requested-with': 'XMLHttpRequest',
						"searchQuery":"store={}&query={}".format(store, SKU),


						}

				url = "https://www.walmart.com/store/ajax/search"
				loop = 0
				res = None
				while res == None:
					loop = loop + 1
					res = requests.post(url, data=data, timeout=1)
					if loop > 5:
						NoStores.append(' ')
						break
				res = res.json()
				a["Price"] = int((GrabElement(str(res), 'priceInCents'))) * .01
				a["Quantity"] = abs(int(float((GrabElement(str(res), 'quantity')))))
				Lis.append(a)
				try:
					lock.acquire()
					print('{} Scanned'.format(store))
				except:
					pass
				lock.release()
			except Exception as exp:
				pass
	listname = GrabAllStoreNumbers()
	listname = chunks(listname, int(len(listname)/30))
	start = time.time()
	threads = [threading.Thread(target=FNCN, args=(arguments, sku)) for arguments in listname]

	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()
	end = time.time()
	for l in Lis:
		print(l)
	print("Total Time Elapsed: {}".format(end - start))
	return Lis

if __name__ == "__main__":
	#print('{} stores were returned - View {}.csv for product information'.format(str(len(Data)), str(SKU)))
	Data = ReturnLowestPrice("106607294")
	for e in Data:
		print e
	with open('dict.csv', 'wb') as csv_file:
	    writer = csv.writer(csv_file)
	    for key, value in mydict.items():
	       writer.writerow([key, value])
	'''with open("{}.csv".format(SKU), 'w') as csv_file:
		writer = csv.writer(csv_file)
		f = ["Time Scanned", "Quantity Available", "Price", "Store"]
		writer.writerow(f)
		f = []
		writer.writerow(f)

	for Information in Data:
		with open("{}.csv".format(SKU), 'a') as csv_file:
			f = []
			writer = csv.writer(csv_file)
			f.append(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
			for key, value in Information.items():
				f.append(value)
			writer.writerow(f)	'''
	