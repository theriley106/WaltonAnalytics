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


	def returnElectrode(self, SKU):
		headers = {'accept-language': 'en-US', 'x-forwarded-for': '172.0.01', 
				'accept': 'text/html', 'x-crawlera-cookies': 'disable', 'user-agent' : str(RandomHeaders.returnUA())}
		url = ELECTRODE_API.format(SKU)
		electrode_response = requests.get(url, headers=headers, proxies=random.choice(self.proxyList),verify=False, timeout=300, allow_redirects=True)
		if self.saveResponse == True:
			saveToJson(electrode_response.json(), SKU)
		return electrode_response


r = requests.post("http://138.197.123.15:8888/proxies/{}".format(open('./SecretCode.txt').read().strip())).json()

a = walShark(proxyList = r["proxies"], saveResponse=True)
electrode_json = a.returnElectrode('46118613').json()
if electrode_json['product'].get('priceRanges'):
	price_range = electrode_json['product']['priceRanges'].values()[0]
