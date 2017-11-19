import requests
import bs4
import random
import time
import threading
import json
import RandomHeaders
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

ELECTRODE_API = "https://www.walmart.com/product/electrode/api/state/content/{0}"
TERRA_FIRMA_API = "https://www.walmart.com/terra-firma/item/{0}"
SEARCH_API = "http://search.mobile.walmart.com/search?query={0}&store={1}&size=20&offset={2}"
TERRA_FIRMA_ZIP = 'https://www.walmart.com/terra-firma/item/{0}/location/{1}?selected=true&wl13='

def saveToJson(jsonDict, fileName):
	with open('{}.json'.format(fileName.replace('.json', '')), 'w') as outfile:
		json.dump(jsonDict, outfile) 

class walShark(object):
	def __init__(self, proxyList=[], saveResponse=False, randomizeHeaders=True, randomizeProxies=True, primaryStore=None, confirmProxy=False):
		self.proxyList = proxyList
		self.randomizeHeaders = randomizeHeaders
		self.randomizeProxies = randomizeProxies
		self.primaryStore = primaryStore
		self.saveResponse = saveResponse

	def returnHeaders(self):
		headers = {'accept-language': 'en-US', 'x-forwarded-for': '172.0.01', 
				'accept': 'text/html', 'x-crawlera-cookies': 'disable', 'user-agent' : str(RandomHeaders.returnUA())}
		return headers

	def returnElectrode(self, SKU):
		url = ELECTRODE_API.format(SKU)
		electrode_response = requests.get(url, headers=self.returnHeaders(), proxies=random.choice(self.proxyList),verify=False, timeout=300, allow_redirects=True)
		if self.saveResponse == True:
			saveToJson(electrode_response.json(), SKU)
		return electrode_response

	def returnTerraFirma(self, SKU):
		url = TERRA_FIRMA_API.format(SKU)
		terra_firma_response = requests.get(url, headers=self.returnHeaders(), proxies=random.choice(self.proxyList),verify=False, timeout=300, allow_redirects=True)
		if self.saveResponse == True:
			saveToJson(terra_firma_response.json(), SKU)
		return terra_firma_response

	#def returnMobileInfo(self, SKU, store, allResults=False):
		#if allResults = False:

	def returnTerraFirmaZIP(self, SKU, zipCode=None):
		url = TERRA_FIRMA_ZIP.format(SKU, zipCode)
		terra_firma_zip_response = requests.get(url, headers=self.returnHeaders(), proxies=random.choice(self.proxyList), allow_redirects=True)
		if self.saveResponse == True:
			saveToJson(terra_firma_zip_response.json(), SKU)
		return terra_firma_zip_response


r = requests.post("http://138.197.123.15:8888/proxies/{}".format(open('./SecretCode.txt').read().strip())).json()

a = walShark(proxyList = r["proxies"], saveResponse=True)
electrode_json = a.returnTerraFirmaZIP('46118613', '29680').json()
