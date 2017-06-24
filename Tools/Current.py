import time
import requests
import bs4
import csv
import random
import Networking

def ConvertCSV(spreadsheet, column=None, Keyword=None, IgnoreWords=None):
	with open(spreadsheet, 'r') as f:
		reader = csv.reader(f)
		AllRows = list(reader)
	if column != None:
		ReturningList = []
		for rows in AllRows:
			if IgnoreWords == None:
				if Keyword == None:
					ReturningList.append(rows[int(column)])
				else:
					if str(Keyword).lower() in str(rows).lower():
						ReturningList.append(rows[int(column)])
			else:
				if Keyword == None and str(IgnoreWords).lower() not in str(rows).lower():
					ReturningList.append(rows[int(column)])
				else:
					if str(Keyword).lower() in str(rows).lower() and str(IgnoreWords).lower() not in str(rows).lower():
						ReturningList.append(rows[int(column)])

		return ReturningList
	else:
		return AllRows

def ModdedRequest(url):
	res = requests.get(url, headers=RandomHeaders.Loadheader(), proxies=Networking.Proxies())


"""If a search returns only a single item, that means that the model number is correct"""

'''Create a program to determine which proxies are currently working"""




ListOfStores = ConvertCSV('Walmarts.csv', 0, Keyword="supercenter", IgnoreWords="Simpsonville")

print(len(ListOfStores))



#def Lowest(skin):
