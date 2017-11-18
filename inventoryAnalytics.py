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


class walShark(object):
	def __init__(self, proxyList=[], randomizeHeaders=True, randomizeProxies=True, primaryStore=None, confirmProxy=False):
		self.proxyList = proxyList
		self.randomizeHeaders = randomizeHeaders
		self.randomizeProxies = randomizeProxies
		self.primaryStore = primaryStore


	def returnElectrode(self, SKU):
		headers = {'accept-language': 'en-US', 'x-forwarded-for': '172.0.01', 
				'accept': 'text/html', 'x-crawlera-cookies': 'disable', 'user-agent' : str(RandomHeaders.returnUA())}
		url = ELECTRODE_API.format(SKU)       
		return requests.get(url, headers=headers, proxies=random.choice(self.proxyList),verify=False, timeout=300, allow_redirects=True).json()


r = requests.post("http://138.197.123.15:8888/proxies/{}".format(open('./SecretCode.txt').read().strip())).json()

a = walShark(proxyList = r["proxies"])
print a.returnElectrode('46118613')
