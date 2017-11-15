import os
import requests
import main
import random
import threading
import json
import sys
import time
lock = threading.Lock()
STARTTIME = time.time()
TIMEOUT = 10
if "debug" in str(sys.argv).lower():
	DEBUG = True
else:
	DEBUG = False
if "timeout" in str(sys.argv).lower():
	TIMEOUT = sys.argv[sys.argv.index("TIMEOUT") + 1]

THREADS = int(sys.argv[1])
print(THREADS)
SKU = sku = sys.argv[2]

if THREADS > 500:
	sys.exit()

listOfStores = main.GrabAllStoreNumbers()

PRIMARYDICT = {}

def chunks(l, n):
	for i in xrange(0, len(l), n):
		yield l[i:i + n]

def searchSKU(storeList, sku):
	for store in storeList:
		if (time.time() - STARTTIME) < (60*TIMEOUT):
			try:
				suggestions_list = random.choice(listOfStores)
				newData = main.SearchStore(store, sku)
				newData["Price"]
				lock.acquire()
				PRIMARYDICT[store] = {"Price": newData["Price"], "Quantity": newData["Quantity"]}
				lock.release()
				

			except Exception as exp:
				if DEBUG == True:
					print exp
				pass
		else:
			return


def updateDict():
	while (time.time() - STARTTIME) < (60*TIMEOUT):
		lock.acquire()
		with open('{}.json'.format(SKU), 'w') as f:
			json.dump(PRIMARYDICT, f)
		lock.release()
		e = 0
		while TIMEOUT > 0 and e < 5:
			e += 1
			time.sleep(1)
	lock.acquire()
	with open('{}.json'.format(SKU), 'w') as f:
		json.dump(PRIMARYDICT, f)
	lock.release()
	return

		
partListOfStores = chunks(listOfStores, int(len(listOfStores)/THREADS))

threading.Thread(target=updateDict).start()

threads = [threading.Thread(target=searchSKU, args=(stores, sku)) for stores in partListOfStores]
for thread in threads:
	thread.start()
for thread in threads:
	thread.join()
TIMEOUT = 0
time.sleep(1.5)
print("Completed in {} Seconds".format(time.time() - STARTTIME))