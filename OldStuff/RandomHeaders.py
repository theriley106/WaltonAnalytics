import random
import csv


UserAgentCSV = open('Data/UserAgent.csv', 'r')
UserAgentList = csv.reader(UserAgentCSV)
UserAgentList = [row for row in UserAgentList]
UserAgentList = [l[0] for l in UserAgentList]
random.shuffle(UserAgentList)

def LoadHeader():
	#This is bad code style but it's reffered to somewhat frequently in analytics.py
	return {'User-Agent': random.choice(UserAgentList)}

def returnUA():
	return random.choice(UserAgentList)

def loadHeader():
	return {'User-Agent': random.choice(UserAgentList)}