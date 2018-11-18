import time
import csv
import RandomHeaders
import threading
import os
import glob
import grey_harvest
import requests
import random
import sys
import Networking
reload(sys)
sys.setdefaultencoding('utf-8')

Proxies = [{}]
THREADS = 30
LengthOfProxies = 30

def grabStoreFlyers(store):
	url = 'https://api.flyertown.com/flyerkit/v2.0/publications/walmartusa?access_token=bec50cdf&locale=en-US&store_code={}'.format(store)
	return url

def returnsLiterallyEverything(store):
	url = 'https://search.mobile.walmart.com/search?query=%23&store={}&size=50&mode=setStore&offset=50&searchType=entered'
	return url

def searchDirectlyInApp(key, store):
	url = 'https://search.mobile.walmart.com/search?query={}&store={}&size=20&mode=setStore&offset=0&searchType=entered'.format(key, store)
	return url

def grabAllFreePickupToday(store):
	url = 'https://www.walmart.com/preso/search?prg=mWeb&sort=&page=10&pref_store={}&facet=pickup_and_delivery%3AFREE%20Pickup%20Today'.format(store)
	return url

def getDepartments(store):
	url = 'https://api.mobile.walmart.com/taxonomy/departments'
	return url

def searchByUPC(upc, store):
	url = "http://search.mobile.walmart.com/v1/products-by-code/UPC/{}?storeId={}".format(upc, store)
	return url

def AutocompleteFromAndroid(string):
	url = 'https://maps.googleapis.com/maps/api/place/autocomplete/json?key=AIzaSyAMY5NFtMaQD0Mf4RKLBLakwo1Z6jMCxTw&sensor=true&types=geocode&input=29680&radius=null&components=country%3Aus'
	return url

def returnLatLongStores(string):
	url = 'https://search.mobile.walmart.com/v1/stores/locate?lat=34.7370639&long=-82.2542834&distance=1000&offset=0&count=100'
	return url

def GrabFromSpreadsheet(spreadsheet):
		ListOfStores = []
		with open(spreadsheet, 'r') as f:
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

def GrabByZip(sku, zip):
	url = 'https://www.walmart.com/terra-firma/item/{}/location/{}?selected=true&wl13='.format(sku, zip)
	res = requests.get(url)
	a = res.json()
	OldPrice = (a['payload']['offers'][list(a['payload']['offers'])[0]]['pricesInfo']['priceMap']['WAS']['price'])
	CurrentPrice = (a['payload']['offers'][list(a['payload']['offers'])[0]]['pricesInfo']['priceMap']['CURRENT']['price'])
	offerid = str(result).partition('Offer Id: ')[2].partition(', ')[0]
	return result

def CalculatePrice():
	#Calculates pricing info for all items in newest folder
	Info = []
	def CSVTOSKU():
		SKUs = []
		def DoSomething(store):
			try:
				Database = ConvertStoreToDict(store)
				for key, value in Database.items():
					SKUs.append(key)
			except:
				pass
		threads = [threading.Thread(target=DoSomething, args=(store,)) for store in FindCurrentStores()]
		for thread in threads:
			thread.start()
		for thread in threads:
			thread.join()
		return SKUs
	def remove_duplicates(l):
		return list(set(l))
	SKUs = CSVTOSKU()
	listofSKU = remove_duplicates(SKUs)


	listofSKU = chunks(listofSKU, len(listofSKU)/10)
	def GrabPrice(smalllist):

		for s in smalllist:
			try:
				a = Analytics.OnlinePricingInfo(s)
				b = [s, a['ListPrice'], a['Price']]
				print(b)
				Info.append(b)
			except BaseException as exp:
				print(exp)
				pass
	threads = [threading.Thread(target=GrabPrice, args=(sku,)) for sku in listofSKU]
	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()
	return Info

def ConvertStoreToDict(store):
	lis = {}
	with open('{}/{}.csv'.format('Data/', store), 'rb') as f:
		reader = csv.reader(f)
		your_list = list(reader)
	for lines in your_list:
		try:
			a = {}
			for i in range(len(your_list[0])):
				a[str(your_list[0][i])] = lines[i]
			lis[str(a['productId'])] = a
		except:
			pass
	return lis
def CSVTOSKU():
	SKUs = []
	def DoSomething(store):
		Database = ConvertStoreToDict(store)
		for key, value in Database.items():
			SKUs.append(key)
		print(store)
	threads = [threading.Thread(target=DoSomething, args=(store,)) for store in FindCurrentStores()]
	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()
	return SKUs

def remove_duplicates(l):
	return list(set(l))

def Status(zip):
	with open('Economics.csv', 'rb') as f:
		reader = csv.reader(f)
		lis = list(reader)
	for e in lis:
		if str(zip) in str(e):
			return int(float(str(e[1]).replace(",", '')))
def Average(numbers):
	return float(sum(numbers)) / max(len(numbers), 1)
def RareItem(sku):
	a = 0
	for store in Stores:
		quantity = float(int(Database[store][sku]['quantity']))
		if int(quantity) < 0:
			quantity = 0
		if quantity == 0:
			a = a + 1
	if a / len(Stores) < .2:
		return True
	else:
		return False
def ReturnStoreQuantity(store, sku):
	quantity = float(int(Database[store][sku]['quantity']))
	if int(quantity) < 0:
		quantity = 0
	return quantity
def hasNumbers(inputString):
	return any(char.isdigit() for char in inputString)
def FindNewestFolder():
	'''Dir = max(glob.glob(os.path.join(os.getcwd(), '*/')), key=os.path.getmtime).split('/')[-2]


	if 'static' not in str(Dir):
		return Dir
	else:
		raise Exception('static is being reported as the newest folder...')'''
	return "Data"

def FindCurrentStores():
	Stores = []
	for files in os.listdir(FindNewestFolder()):
		Stores.append(files.replace('.csv', ''))
	return Stores


def CSVtoList(csvfile):
	with open('{}/{}'.format(str(FindNewestFolder()), str(csvfile)), 'rb') as f:
		reader = csv.reader(f)
		return list(reader)

def StoretoList(store):
	SKUs = []
	for key, value in Database[store].items():
		SKUs.append(key)
	return SKUs
def LocalPrice(store, sku):
	lis = {}
	with open('{}/{}.csv'.format(str(FindNewestFolder()), store), 'rb') as f:
		reader = csv.reader(f)
		your_list = list(reader)
	for lines in your_list:
		try:
			a = {}
			for i in range(len(your_list[0])):
				a[str(your_list[0][i])] = lines[i]
			if a['productId'] == str(sku):
				return [int(float(a['priceInCents'])) / 100, a['quantity']]
			if a['WWWItemId'] == str(sku):
				return [int(float(a['priceInCents'])) / 100, a['quantity']]
		except BaseException as exp:
			print(exp)
			pass

def ConvertStoreToDict(store):
	lis = {}
	with open('{}/{}.csv'.format(str(FindNewestFolder()), store), 'rb') as f:
		reader = csv.reader(f)
		your_list = list(reader)
	for lines in your_list:
		try:
			a = {}
			for i in range(len(your_list[0])):
				a[str(your_list[0][i])] = lines[i]
			lis[str(a['productId'])] = a
		except:
			pass
	return lis

def GrabStorePrice(store, sku):
	return float(Database[store][sku]['priceInCents'])

def ReturnCategory(store, electronics):
	SKUs = StoretoList(store)
	for sku in SKUs:
		if Database[store][sku]['name'] == 'Cell Phones':
			print('{} - {}'.format(sku, Database[store][sku]['priceInCents']))

def ReturnAllCellPhone(store):
	SKUs = StoretoList(store)
	for sku in SKUs:
		if Database[store][sku]['name'] == 'Cell Phones':
			print('{} - {}'.format(sku, Database[store][sku]['priceInCents']))
def Compare(store, option=4):
	#This algorithm detects if a local store has an item for less than 50% of average
	if option == 1:
		print('\n\nThe following items are 50%+ off of the National Average for the item\n\n')
		for sku in StoretoList(store):
			try:
				if GrabStorePrice(store, sku) / NationalAverage(sku) < .5:
					print(sku)
			except:
				pass
	if option == 2:
		print('\n\nThe following items are 80%+ off of the National Average for the item\n\n')
		for sku in StoretoList(store):
			try:
				if GrabStorePrice(store, sku) / NationalAverage(sku) < .2:
					print(sku)
			except:
				pass
	if option == 3:
		print("\n\nThe following items are considered 'rare' (80%+ out of stock) but in stock at {}\n\n".format(store))
		for sku in StoretoList(store):
			try:
				if RareItem(sku) == True and ReturnStoreQuantity(store, sku) > 0:
					print(sku)
			except:
				pass
	if option == 4:
		print("\n\n(Pricing above $20) The following items are considered 'rare' (80%+ out of stock) but in stock at {}\n\n".format(store))
		for sku in StoretoList(store):
			try:
				if RareItem(sku) == True and ReturnStoreQuantity(store, sku) > 0 and float(GrabStorePrice(store, sku)) / 100 > 20:
					print(sku)
			except:
				pass


def NationalAverage(sku):
	Prices = []
	for store in Stores:
		try:
			Prices.append(int(Database[store][sku]['priceInCents']))
		except:
			pass
	return Average(Prices)


def CompareStores(sku, listofstores):
	Pricing = {}
	for store in listofstores:
		try:
			Pricing[store] = int(Database[store][sku]['priceInCents'])
		except:
			pass
	return Pricing

def PullListPrice(sku):
	url = 'https://www.walmart.com/search/?query={}'.format(sku)
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	res = requests.get(url, headers=headers, proxies=proxies)
	price = float(str(str(res.text).partition('"offerPrice":'.format(sku))[2]).split(',')[0])
	try:
		listprice = float(str(str(res.text).partition('"listPrice":'.format(sku))[2]).split(',')[0])
	except:
		listprice = price
	return float(listprice)

def OnlinePricingInfo(sku):
	url = 'https://www.walmart.com/search/?query={}'.format(sku)
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	res = requests.get(url, headers=headers, proxies=proxies)
	price = float(str(str(res.text).partition('"offerPrice":'.format(sku))[2]).split(',')[0])
	try:
		listprice = float(str(str(res.text).partition('"listPrice":'.format(sku))[2]).split(',')[0])
	except:
		listprice = price
	return {'ListPrice': float(listprice), "Price": float(price)}

def CurrentOnlinePrice(sku):
	url = 'https://www.walmart.com/search/?query={}'.format(sku)
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	res = requests.get(url, headers=headers, proxies=proxies)
	price = float(str(str(res.text).partition('"offerPrice":'.format(sku))[2]).split(',')[0])
	return float(price)


def ReturnStoreInfo(store):
	#this is the problem with the FindNewestFolder()
	Information = {}
	lis = []
	with open('./{}.csv'.format(store), 'rb') as f:
		reader = csv.reader(f)
		your_list = list(reader)
	for lines in your_list:
		try:
			a = {}
			for i in range(len(your_list[0])):
				a[str(your_list[0][i])] = lines[i]
			lis.append(a)
		except:
			pass
	arb = []
	Electronics = 0
	quant = 0
	lim = 0
	he = 0
	vg = 0
	cellphones = 0
	for a in lis:
		try:
			if str(a['status']) == 'Limited Stock' and float(a['quantity']) > 0 and str(a['name']) == 'Electronics' and len(arb) < 5:
				arb.append('https://www.walmart.com/store/{}/search?query={}'.format(store, a['WWWItemId']))

			if str(a['status']) == 'Limited Stock' and float(a['quantity']) > 0:
				lim = lim + 1
			if str(a['status']) == 'Limited Stock' and float(a['quantity']) > 0:
				lim = lim + 1
			if str(a['name']) == 'Electronics':
				Electronics = Electronics + 1
			if str(a['name']) == 'Household Essentials' and float(a['quantity']) > 0:
				he = he + 1
			if str(a['name']) == 'Video Games' and float(a['quantity']) > 0:
				vg = vg + 1
			if str(a['name']) == 'Cell Phones' and float(a['quantity']) > 0:
				cellphones = cellphones + 1

			if float(a['quantity']) > 0:
				quant = quant + 1
		except:
			pass
	Information['Electronics'] = Electronics
	Information['Item Count'] = len(your_list)
	Information['InStock'] = round(((float(quant) / float(len(your_list))) * 100), 2)
	Information['LimitedStock'] = lim
	Information["CellPhones"] = cellphones
	Information["HomeEssentials"] = he
	Information['VideoGames'] = vg
	Information['Arbitrage'] = arb
	return Information

def GrabAllStoreNumbers():
	ListOfStores = []
	with open('Walmarts.csv', 'r') as f:
		reader = csv.reader(f)
		your_list = list(reader)
	for line in your_list:
		if 'Walmart Supercenter' in str(line[1]):
			ListOfStores.append(line[0])
	return ListOfStores
def chunks(l, n):
	for i in xrange(0, len(l), n):
		yield l[i:i + n]


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
			'cookie' : 'spid=E5669BFD-B28F-486F-B4E3-54B125AB6AE2; s=undefined; prefper=PREFSTORE~1641~2PREFCITY~1Greenville~2PREFFULLSTREET~16134%20White%20Horse%20Rd~2PREFSTATE~1SC~2PREFZIP~129601~2PREFSTORE~1641~2PREFCITY~1Greenville~2PREFFULLSTREET~16134%20White%20Horse%20Rd~2PREFSTATE~1SC~2PREFZIP~129601; TBV=a0zyf; WMR=p1-1|p2-1|p3-1|p4-0; akavpau_p3=1491489649~id=9dde41a09f2cbb9ae5cdeeeac7e57280; akavpau_p5=1491489662~id=4efbe67fefa3314c47cc13b7f11e36b9; sps=i%2454310056%3B48183904%3B; athrvi=RVI~h33cb4a8-h2df3a60; akavpau_p4=1491508840~id=328602308bf193a1352503323b59cc06; x-csrf-jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiY29va2llIiwidXVpZCI6Ijg4NjU4YTkwLTFiMDItMTFlNy04ZmI1LWVkODA2YmE2N2JiZiIsImlhdCI6MTQ5MTUwODMzNSwiZXhwIjoxNDkxNTA5NTM1fQ.1YZyxD3V_4LWPtHwG-jIyvultQ8w0am1GzCp8ToTfP4; AID=wmlspartner%3DhQHSnYPFcGw%3Areflectorid%3D09007855021638109532%3Alastupd%3D1491508335032; search.perf.metric=timerPromiseAll=143ms|timerHeaderAction=71ms|timerSearchAction=143ms|timerFooterAction=41ms|timerPreso=139ms; DL=67052%2C37.751007080078125%2C-97.8219985961914%2Cip%2C67052%2CUSA%2CKS; NSID=3103.1-5855.6-3283.7-1221.8-5991.12-5990.12-1099.13-4321.14-592.17-1507.19-3155.20-3492.20-2428.28-370.28-346.32-794.33-186.38-369.43-978.48-993.49; akavpau_p7=1491508935~id=e3e677b43522fee0b70a0b183b3c3f06; VSID=2265%2C2266; SSLB=2; akavpau_p0=1491513602~id=fe0e46157f671ff7fcddc52eadcaafd8; AID=wmlspartner%3DhQHSnYPFcGw%3Areflectorid%3D09007855021638109532%3Alastupd%3D1491513085492; com.wm.reflector="reflectorid:09007855021638109532@lastupd:1491513085492@firstcreate:1491486835583"; vtc=Sa7mas539Zo9I10IU9BNk8; bstc=SaXTFjNaJobs1VjUAj7sZc; exp=1%2B1491512606%2BSa7mas539Zo9I10IU9BNk8%2B0%2BCcvJB.uH-Lt|bCt4O.KMTvF; exp-ck=uH-LtKMTvF; akavpau_p9=1491513731~id=a7eec29316d45708d714d4629324b12e',
			'origin' : 'https://www.walmart.com',
			'referer' : 'https://www.walmart.com/store/{}/search?query={}'.format(store, SKU),
			'user-agent' : 'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; GTB7.4; InfoPath.2; SV1; .NET CLR 3.3.69573; WOW64; en-US)',
			'x-requested-with': 'XMLHttpRequest',
			"searchQuery":"store={}&query={}".format(store, SKU),


			}

	url = "https://www.walmart.com/store/ajax/search"
	res = requests.post(url, data=data, proxies=proxies)
	res = res.json()
	try:
		a["Price"] = int((GrabElement(str(res), 'priceInCents'))) * .01
	except:
		pass

	a["Quantity"] = (GrabElement(str(res), 'quantity'))
	return a
def GenerateHundred():
	Results = random.sample(GrabAllStoreNumbers(), 100)
	return Results


def GrabNearbyStores(zip):
	res = requests.get('https://www.walmart.com/search/api/location?location={}'.format(zip), headers=RandomHeaders.LoadHeader(), proxies=proxies)
	print(res.json())

def SearchResultsLocalStores(sku, storenum):
	url = 'https://www.walmart.com/search/api/preso?prg=desktop&query={}&stores={}'.format(sku, storenum)
	res = requests.get(url,  headers=RandomHeaders.LoadHeader(), proxies=proxies)
	print(res.json())

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
						'cookie' : 'spid=E5669BFD-B28F-486F-B4E3-54B125AB6AE2; s=undefined; prefper=PREFSTORE~1641~2PREFCITY~1Greenville~2PREFFULLSTREET~16134%20White%20Horse%20Rd~2PREFSTATE~1SC~2PREFZIP~129601~2PREFSTORE~1641~2PREFCITY~1Greenville~2PREFFULLSTREET~16134%20White%20Horse%20Rd~2PREFSTATE~1SC~2PREFZIP~129601; TBV=a0zyf; WMR=p1-1|p2-1|p3-1|p4-0; akavpau_p3=1491489649~id=9dde41a09f2cbb9ae5cdeeeac7e57280; akavpau_p5=1491489662~id=4efbe67fefa3314c47cc13b7f11e36b9; sps=i%2454310056%3B48183904%3B; athrvi=RVI~h33cb4a8-h2df3a60; akavpau_p4=1491508840~id=328602308bf193a1352503323b59cc06; x-csrf-jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiY29va2llIiwidXVpZCI6Ijg4NjU4YTkwLTFiMDItMTFlNy04ZmI1LWVkODA2YmE2N2JiZiIsImlhdCI6MTQ5MTUwODMzNSwiZXhwIjoxNDkxNTA5NTM1fQ.1YZyxD3V_4LWPtHwG-jIyvultQ8w0am1GzCp8ToTfP4; AID=wmlspartner%3DhQHSnYPFcGw%3Areflectorid%3D09007855021638109532%3Alastupd%3D1491508335032; search.perf.metric=timerPromiseAll=143ms|timerHeaderAction=71ms|timerSearchAction=143ms|timerFooterAction=41ms|timerPreso=139ms; DL=67052%2C37.751007080078125%2C-97.8219985961914%2Cip%2C67052%2CUSA%2CKS; NSID=3103.1-5855.6-3283.7-1221.8-5991.12-5990.12-1099.13-4321.14-592.17-1507.19-3155.20-3492.20-2428.28-370.28-346.32-794.33-186.38-369.43-978.48-993.49; akavpau_p7=1491508935~id=e3e677b43522fee0b70a0b183b3c3f06; VSID=2265%2C2266; SSLB=2; akavpau_p0=1491513602~id=fe0e46157f671ff7fcddc52eadcaafd8; AID=wmlspartner%3DhQHSnYPFcGw%3Areflectorid%3D09007855021638109532%3Alastupd%3D1491513085492; com.wm.reflector="reflectorid:09007855021638109532@lastupd:1491513085492@firstcreate:1491486835583"; vtc=Sa7mas539Zo9I10IU9BNk8; bstc=SaXTFjNaJobs1VjUAj7sZc; exp=1%2B1491512606%2BSa7mas539Zo9I10IU9BNk8%2B0%2BCcvJB.uH-Lt|bCt4O.KMTvF; exp-ck=uH-LtKMTvF; akavpau_p9=1491513731~id=a7eec29316d45708d714d4629324b12e',
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
					res = requests.post(url, data=data, proxies=random.choice(Proxies), timeout=10)
					if loop > 5:
						NoStores.append(' ')
						break
				res = res.json()
				print res
				a["Price"] = int((GrabElement(str(res), 'priceInCents'))) * .01
				a["Quantity"] = abs(int(float((GrabElement(str(res), 'quantity')))))
				Lis.append(a)
				print('-')
			except Exception as exp:
				print(exp)
				pass
	if accounttype != "Limited":
		listname = GrabAllStoreNumbers()
	else:
		listname = GenerateHundred()
	listname = chunks(listname, int(len(listname)/int(LengthOfProxies)))
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
	#print('\n\n\nTotal Time Elapsed: {} Seconds\n{} Did not work'.format(end - start, len(NoStores)))

def returnStoreItemCount(store, searchterm, dic=None):
	Quantity = None
	retry = 0
	while Quantity == None and retry < 5:
		try:
			payload = {"storeId":store,"searchTerm":searchterm,"size":49,"dept":1000,"newIndex":1, 'offset': 0, "query":searchterm,"idx":1}
			res = requests.post('https://www.walmart.com/store/electrode/api/search', data=payload, proxies=random.choice(Proxies))
			a = res.json()['result']['totalCount']
			Quantity = a
			if dic != None:
				dic[searchterm] = Quantity
			return Quantity
		except:
			retry += 1
	raise Exception("return Item Count Failed...")


def wmGrabData(store, searchterm, offset, storeDict=None, threadCount=10):
	totalPages = genPageVar(offset)
	def genData(store, searchTerm, listPage, storeDict):
		for offset in listPage:
			payload = {"storeId":store,"searchTerm":searchterm,"size":49,"dept":1000,"newIndex":1, 'offset': offset, "query":searchterm,"idx":1}
			res = requests.post('https://www.walmart.com/store/electrode/api/search', data=payload, proxies=random.choice(Proxies))
			if storeDict == None:
				return res.json()["result"]['results']
			else:
				for e in res.json()["result"]['results']:
					try:
						rating = e['ratings']['rating']
						e['ratings'] = rating
						inventoryStatus = e['inventory']['status']
						inventoryQuantity = e['inventory']['quantity']
						e['quantity'] = inventoryQuantity
						e['inStock'] = inventoryStatus
						del e['inventory']
						try:
							price = float(e['price']['priceInCents']) * .01
							e['price'] = price
						except:
							e['price'] = "UNAVAILABLE"
						review = e['reviews']['reviewCount']
						e['reviews'] = review
						image = e['images']['largeUrl']
						e['images'] = image
						del e['location']
						dept = e['department']['name']
						e['department'] = dept
						e['www'] = e['productId']['WWWItemId']
						e['upc'] = e['productId']['upc']
						e['pID'] = e['productId']['productId']
						del e['productId']
						if e['upc'] not in str(storeDict[store]['results']):
							storeDict[store]['results'].append(e)
					except:
						pass
	threads = [threading.Thread(target=genData, args=(store, searchterm, listPage, storeDict)) for listPage in chunks(totalPages, len(totalPages)/threadCount)]
	for thread in threads: thread.start()
	for thread in threads: thread.join()
def genPageVar(categorizedInventoryCount):
	a = []
	for i in range(0, int(categorizedInventoryCount), 49):
		a.append(i)
	return a

def printInventory(store, results):
	while True:
		time.sleep(2)
		try:
			print len(results[store]['results'])
		except Exception as exp:
			print exp

def saveInventory(store, my_dict):
	while True:
		time.sleep(15)
		with open('{}.csv'.format(store), 'wb') as f:  # Just use 'w' mode in 3.x
			w = csv.DictWriter(f, my_dict[store]['results'][0].keys())
			w.writeheader()
			w.writerows(my_dict[store]['results'])

class storeAnalytics(object):
	def __init__(self, store, searchTerms=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '*']):
		self.store = store
		self.inventoryCount = 0
		results = {}
		threads = [threading.Thread(target=returnStoreItemCount, args=(store, char, results)) for char in searchTerms]
		for thread in threads: thread.start()
		for thread in threads: thread.join()
		self.categorizedInventory = results.copy()
		for char in searchTerms:
			self.inventoryCount += results[char]
		self.inventory = {self.store: {'results': []}}

	#def findAllSKU(self):

	def searchStore(self):
		threads = [threading.Thread(target=wmGrabData, args=(self.store, searchterm, resultcount, self.inventory)) for searchterm, resultcount in self.categorizedInventory.iteritems()]
		for thread in threads: thread.start()
		threading.Thread(target = printInventory, args = (self.store, self.inventory)).start()
		threading.Thread(target = saveInventory, args = (self.store, self.inventory)).start()
		for thread in threads: thread.join()




if __name__ == "__main__":
	#ReturnLowestPrice("106607294")
	#ReturnStoreInfo('5871')
	a = storeAnalytics('3563')
	'''for e in wmGrabData("2265", "1", 0):
		print e["name"]'''
	a.searchStore()
	#print('opened')


