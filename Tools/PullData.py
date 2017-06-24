import csv
import requests
import random
import bs4
import os.path
import os
import threading
import time

Threads = 10
proxies = {}

Walmart = '/var/www/FlaskApp/FlaskApp/statics/Walmarts.csv'

def GrabPricingInfo(SKU, timeout, Save=False):
	if Save != False:
		with open(str(Save), 'w') as fp:
			b = csv.writer(fp)
			data = ["Title","Price", "Address"]
			b.writerow(data)
	stores = {}
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
	def GrabFromSpreadsheet(spreadsheet):
		ListOfStores = []
		with open(spreadsheet, 'r') as f:
			reader = csv.reader(f)
			your_list = list(reader)
		for line in your_list:
			if 'Walmart Supercenter' in str(line[1]):
				stores[line[0]] = line[1]
				ListOfStores.append(line[0])
		return ListOfStores
	try:
		Stores = GrabFromSpreadsheet(Walmart)
	except:
		Stores = GrabFromSpreadsheet('/home/administrator/Python_Arbitrage/Walmarts.csv')
	Information = []
	def ReturnStore():
		a = []
		for i in range(len(Stores) / Threads):
			e = random.choice(Stores)
			Stores.remove(e)
			a.append(e)
		return a
	def SaveData(a, Save):
		Information.append(a)

		with open(str(Save), 'a') as fp:
			b = csv.writer(fp)
			data = [a["Title"], a["Price"], a["Quantity"], a["Address"], a["Image"]]
			b.writerow(data)
	def GrabPrice(SKU=SKU, timout=timeout):
		MultipleStores = ReturnStore()
		#print(MultipleStores)
		def PickStore(MultipleStores=MultipleStores):

			if time.time() < timeout:
				a = random.choice(MultipleStores)
				MultipleStores.remove(a)
				return a
			else:
				MultipleStores = []
				return None

		while time.time() < timeout:
			try:
				store = PickStore()
				#print("store={}&query={}".format(store, SKU))
				if store != None:
					a = {}
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
					print(res)
					a["Address"] = stores[str(store)]
					try:
						a["Price"] = int((GrabElement(str(res), 'priceInCents'))) * .01
					except:
						continue
					a["Quantity"] = (GrabElement(str(res), 'quantity'))
					a["Title"] = (GrabElement(str(res), 'name'))
					a["Image"] = (GrabElement(str(res), "largeUrl"))
					if a["Quantity"] == None:
						a["Quantity"] = 0
					if a["Quantity"] < 0:
						a["Quantity"] = 0
					if a["Price"] == None:
						a = None
					if Save != False:
						SaveData(a, Save)
			except IOError:
			    Error = type, value, traceback = sys.exc_info()
			    if 'base 10' not in str(Error):
			    	pass
			    	#print('Error opening %s: %s' % (value.filename, value.strerror))
	threads = [threading.Thread(target=GrabPrice) for i in range(10)]
	for thread in threads:
		thread.start()


