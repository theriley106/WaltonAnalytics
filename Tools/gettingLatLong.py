import csv
import re
from geopy.geocoders import Nominatim
from pyzipcode import ZipCodeDatabase
zcdb = ZipCodeDatabase()
with open('Walmarts.csv', 'rb') as f:
	reader = csv.reader(f)
	your_list = list(reader)
your_list = your_list[1:]
listOfZips = []

for l in your_list:
	try:
		zipCode = re.findall('\d\d\d\d\d', str(l[1]))[0]
	except:
		zipCode = ""
	listOfZips.append(zipCode)
latLong = []
for e in listOfZips:
	try:
		l = zcdb[e]
		a = (l.latitude, l.longitude)
	except:
		a = ""
	print("{}{}".format(e, a))
	latLong.append([a])


with open("latlongs.csv", 'wb') as myfile:
	wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
	wr.writerows(latLong)