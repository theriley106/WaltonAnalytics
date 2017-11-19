from urlparse import urlparse
from threading import Thread
import httplib, sys
import requests
from Queue import Queue
import csv
import sys
import time
import random
CONCURRENT = 165
r = requests.post("http://138.197.123.15:8888/proxies/{}".format(open('./SecretCode.txt').read().strip())).json()
PROXIES = r["proxies"]

def doWork():
    while True:
        try:
            url = q.get()
            res = requests.get(url, proxies=random.choice(PROXIES), timeout=3)
            print res.status_code
        except:
            pass
        q.task_done()

def GrabAllStoreNumbers():
    ListOfStores = []
    with open('Walmarts.csv', 'r') as f:
        reader = csv.reader(f)
        your_list = list(reader)
    for line in your_list:
        if 'Walmart Supercenter' in str(line[1]):
            ListOfStores.append(line[0])
    return ListOfStores

def getStatus(ourl):
    try:
        url = urlparse(ourl)
        conn = httplib.HTTPConnection(url.netloc)   
        conn.request("HEAD", url.path)
        res = conn.getresponse()
        return res.status, ourl
    except:
        return "error", ourl

def doSomethingWithResult(status, url):
    print status, url

a = GrabAllStoreNumbers()
q = Queue(CONCURRENT * 2)
for i in range(CONCURRENT):
    t = Thread(target=doWork)
    t.daemon = True
    t.start()
try:
    for store in a:
        url = 'https://search.mobile.walmart.com/search?query={}&store={}&size=20&mode=setStore&offset=0&searchType=entered'.format(SKU, store)
        q.put(url)
    q.join()
except KeyboardInterrupt:
    sys.exit(1)

print("Completed in {} Seconds".format(time.time() - STARTTIME))

if __name__ == '__main__':
    SKU = sys.argv[1]