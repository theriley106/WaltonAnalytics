import csv
import requests
import bs4
import threading
import os
import glob
import Analytics

SKUs = []




def remove_duplicates(l):
    return list(set(l))

def FindNewestFolder():
	Dir = max(glob.glob(os.path.join(os.getcwd(), '*/')), key=os.path.getmtime).split('/')[-2]
	if 'static' not in str(Dir):
		return Dir
	else:
		raise Exception('static is being reported as the newest folder...')
def FindCurrentStores():
	Stores = []
	for files in os.listdir(FindNewestFolder()):
		Stores.append(files.replace('.csv', ''))
	return Stores
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

def CalculatePrice():
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


	def chunks(l, n):
	    """Yield successive n-sized chunks from l."""
	    for i in xrange(0, len(l), n):
	        yield l[i:i + n]
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

SKUs = CalculatePrice()

with open('SKUList.csv','wb') as resultFile:
    wr = csv.writer(resultFile, dialect='excel')
    for SKUs in SKUs:
    	wr.writerow(SKUs)