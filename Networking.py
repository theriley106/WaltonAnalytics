from __future__ import print_function
import requests
import random
import time
import threading
import grey_harvest
import re
import csv
import os
from datetime import datetime
import glob



def FindNewestCSV():
	return max(glob.iglob('*.[cC][Ss][vV]'), key=os.path.getctime)
def ArchiveOldCSV():
	os.rename(FindNewestCSV(), "Archived/{}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
	with open('ProxyList.csv', "w") as csv_file:
		writer = csv.writer(csv_file, delimiter=',')
		#reader.writerows([['testing'], ['testing2']])

	



"""website to check proxies"""
Proxies = []
def CSVToList(csvs='ProxyList.csv'):
	with open(csvs, 'r') as f:
		reader = csv.reader(f)
		return list(reader)
def AddProxyToList(proxy):
	print('{} added'.format(proxy))
	Proxies.append([proxy])
def chunks(l, n):
    n = max(1, n)
    return (l[i:i+n] for i in xrange(0, len(l), n))

def BreakApartThreads(listname, howmanythreads):
	return chunks(listname, len(listname)/howmanythreads)

def GrabGreyProxy():
	while True:
		harvester = grey_harvest.GreyHarvester()
		Runned = harvester.run()
		for proxy in harvester.run():
			if CheckProxy(proxy) == True and str(proxy) not in CSVToList():
				print('{} added'.format(proxy))
				AddToCSV(proxy)
			else:
				print('Proxy Not Saved')
		print('Started Runned')
def CheckProxy(proxy):
	proxy = {'https': '{}'.format(proxy), 'http': '{}'.format(proxy)}
	try:
		requests.get('http://www.google.com', proxies=proxy)
		return True
	except Exception as exp:
		return False


def ContinueProxies():
	while True:
		for proxy in Proxies:
			if CheckProxy(proxy) == False:
				Proxies.remove(proxy)
	time.sleep(random.choice(0, 60))

def AddToCSV(proxy):
	AllRows = CSVToList()
	AllRows.append([proxy])
	print('added to csv{}'.format(AllRows))
	with open('ProxyList.csv', "w") as csv_file:
		writer = csv.writer(csv_file, delimiter=',')
		#reader.writerows([['testing'], ['testing2']])
		writer.writerows(AllRows)



def WriteListToFile(listname, file):
	print('writing to list')
	print(listname)
	with open(file, "w") as csv_file:
		writer = csv.writer(csv_file, delimiter=',')
		#reader.writerows([['testing'], ['testing2']])
		writer.writerows(listname)



def ReturnProxies(number=1):
	ProxyLocal = []
	with open('ProxyList.csv', 'r') as f:
		reader = csv.reader(f)
		AllRows = list(reader)
	for proxy in AllRows:
		proxy = proxy[0]
		ProxyLocal.append({'https': '{}'.format(proxy), 'http': '{}'.format(proxy)})
	
	ProxyListGen = []
	if number != 1:
		while len(ProxyListGen) < int(number):
			if int(number) > len(ProxyListGen):
				ProxyChoice = random.choice(ProxyLocal)
			if ProxyChoice not in ProxyListGen:
				ProxyListGen.append(ProxyChoice)
	else:
		ProxyListGen = random.choice(ProxyLocal)
	return ProxyListGen




if __name__ == "__main__":
	try:
		ArchiveOldCSV()
	except:
		pass
	print('Starting')
	threading.Thread(target=GrabGreyProxy).start()
	threading.Thread(target=ContinueProxies).start()




