from Analytics import *

class pullData(object):
	#sources = []
	stores = GrabFromSpreadsheet('static/Walmarts.csv')
	#Soruces should contain a list of dictionaries containing
	# yotuube URLS
	def __init__(self):
		for store in self.stores:
			print store

	def rando(self, store=None):
		if store == None:
			store = random.choice(self.stores)
		print ReturnStoreInfo(store)

	def pullStore(self, storenum):
		
