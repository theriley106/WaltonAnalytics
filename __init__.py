from flask import Flask, render_template, request, url_for, redirect, Markup, jsonify, make_response, send_from_directory, session
import csv
import gpxpy.geo
import bs4
#import PullData
import Analytics
import random
import requests
import os
import time
from operator import itemgetter
import threading

proxies = {}
app = Flask(__name__)
Timeout = 60



@app.route('/download/<file>')  
def download_csv(file):
	return send_from_directory(directory='static', filename=file)

def Status(zip):
	with open('Data/Economics.csv', 'rb') as f:
		reader = csv.reader(f)
		lis = list(reader)
	for e in lis:
		if str(zip) in str(e):
			return int(float(str(e[1]).replace(",", '')))

def MarkupIgnore(markup):
	markup = str(markup.getText())
	return markup

def LatLong(address):
	address = address.replace(" ", "+")
	response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={}'.format(address))
	resp_json_payload = response.json()
	return (resp_json_payload['results'][0]['geometry']['location'])

def diffLatLong(lat1, long1, lat2, long2):
	return gpxpy.geo.haversine_distance(lat1, lon1, lat2, lon2)

def EditGoogleMaps(iframe, width, height):
	try:
		iframe = str(iframe).replace('width="250"', 'width="{}"'.format(width))
		iframe = str(iframe).replace('height="250"', 'height="{}"'.format(height))
	except:
		print(iframe)
	return iframe

def ReturnStoreInfo(store):
	try:
		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
		Store = {}
		url = 'https://www.walmart.com/store/{}'.format(store)
		res = requests.get(url, headers=headers, proxies=proxies)
		page = bs4.BeautifulSoup(res.text, "lxml")
		Store['Number'] = store
		Google = EditGoogleMaps(page.select('#store-side-bar > div.StoreSideBar > div.GoogleMapsIframe > iframe')[0], 400, 400)
		Store['GoogleMaps'] = Markup(Google)
		if len(page.select('.open-24-hours')) == 0:
			Store['StoreHours'] = 'Not 24 Hours'
		else:
			Store['StoreHours'] = '24 Hours'
		Store['Phone'] = MarkupIgnore(page.select('.phone')[0])
		Store['Address2'] = MarkupIgnore(page.select('.address2')[0])
		Store['Address1'] = MarkupIgnore(page.select('.address1')[0])
		Store['Name'] = MarkupIgnore(page.select('.heading-d')[0])
		Store['ItemCount'] = len(Analytics.ConvertStoreToDict(store))
		Store['Econ'] = str("{:,.2f}".format(Status(Store['Address2'][-5:])))[:-3]
		Store.update(Analytics.ReturnStoreInfo(store))
		return Store
	except Exception as exp:
		print(exp)


def GrabFromSpreadsheet(spreadsheet):
	ListOfStores = []

	with open(spreadsheet, 'r') as f:
		reader = csv.reader(f)
		your_list = list(reader)
	for line in your_list:
		a = {}
		if 'Walmart Supercenter' in str(line[1]):
			a['number'] = line[0]
			ListOfStores.append(a)
	return ListOfStores




def CheckUser(username):
	ListOfUsernames = ["Matt", "Christopher"]
	if username != None and str(username) in ListOfUsernames:
		return True
	else:
		return False



@app.route('/')
def Home(username=None):
	return render_template('Home.html', database=GrabFromSpreadsheet("{}/static/Walmarts.csv".format(os.getcwd())))

###############################

@app.route('/Login', methods=['POST'])
def LogIn():
	#Loading Page
	print(session.get('my_var', None))

	session['Username'] = request.form['username']
	session['Password'] = request.form['password']
	if Username == 'admin' and Password == 'password':
		return "True"
	#store = ReturnStoreInfo(store)
	else:
		return 'False'
	#return redirect(url_for('ItemPage', storenum=store))
	#return render_template('testing.html', store=store)

###############################################################################################################################


@app.route('/Item/')
def SearchItem(username=None):
	return render_template('ItemSearch.html', database=GrabFromSpreadsheet("{}/static/Walmarts.csv".format(os.getcwd())))
	

@app.route('/Item/', methods=['POST'])
def SearchItemByNumber(username=None, SKU=None, store=None):
	#Loading Page
	ZIP = request.form['zip']
	SKU = request.form['item']
	#store = ReturnStoreInfo(store)
	return redirect(url_for('ItemPage', storenum=store))
	#return render_template('testing.html', store=store)

@app.route('/Item/<sku>/')
def ItemPage(sku):
	Info = ReturnSKUInfo(sku)
	StockList = MultiStoreSearch(sku)
	#Stock == StockList
	return render_template('ItemPage.html', info=Info)

#########################################################################################

###################SINGLE ITEM SEARCH


@app.route('/LowestPrice/')
def SearchLow(username=None):
	Stock = [{'Store': '', 'Price': '', 'Quantity': '', 'Aisle': ''}]
	BasicItem = {'name': '', 'Title': '', 'OnlinePrice': '', 'ListPrice': '', 'PercentQuantity': '', 'ReviewCount': '', 'AverageReview': ''}

	return render_template('LowSearch.html', Stock=Stock, BasicItem=BasicItem)

@app.route('/LowestPrice/<sku>')
def GrabLowPrice(sku):
	Stock = [{'Store': '', 'Price': '', 'Quantity': '', 'Aisle': ''}]
	BasicItem = {'name': '', 'Title': '', 'OnlinePrice': '', 'ListPrice': '', 'PercentQuantity': '', 'ReviewCount': '', 'AverageReview': ''}

	return render_template('LowestPriceItem.html', Stock=Stock, BasicItem=BasicItem)

@app.route('/LowestPrice/', methods=['POST'])
def SearchItemByLow(username=None, SKU=None, store=None):
	#Loading Page
	SKU = request.form['yourname']
	#store = ReturnStoreInfo(store)
	return redirect(url_for('ItemPage', storenum=store))
	#return render_template('testing.html', store=store)

##################################################################3

@app.route('/Store/')
def SearchStore(username=None):
	return render_template('StoreSearch.html', database=GrabFromSpreadsheet("{}/static/Walmarts.csv".format(os.getcwd())))

@app.route('/Store/', methods=['POST'])
def Search(username=None, SKU=None, store=None):
	#Loading Page
	store = request.form['yourname']
	#store = ReturnStoreInfo(store)
	return redirect(url_for('StorePage', storenum=store))
	#return render_template('testing.html', store=store)






@app.route('/Store/<csvs>/html/')
def ToHTMLDoc(csvs):
	csvs = 'static/' + str(csvs) + '.csv'
	with open(csvs, 'rb') as f:
		reader = csv.reader(f)
		your_list = list(reader)
	print(len(your_list))
	return render_template('ToHTML.html', Stock=your_list)





@app.route('/Store/<storenum>', methods=['GET'])
def StorePage(storenum):
	print('blah')
	store = ReturnStoreInfo(str(int(storenum)))
	if store != None:
		return render_template('testing.html', store=store)
	else:
		return 'error'


#################################################################################################3


@app.route('/_add_numbers')
def add_numbers():
	a = request.args.get('a', 0, type=str)
	store = request.args.get('b', 0, type=str)
	# a is the SKIN or search Query
	a = Analytics.LocalPrice(store, str(a))
	a = '{} - {} In Stock'.format('${:,.2f}'.format(a[0]), a[1])
	if a != None:
		return jsonify(result=str(a))
	else:
		return jsonify(result='Item Not Available')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000, debug=True)






