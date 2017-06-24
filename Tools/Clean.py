import requests


def GrabByZip(sku='27653029', zip='29680'):
	Information = {}
	url = 'https://www.walmart.com/terra-firma/item/{}/location/{}?selected=true&wl13='.format(sku, zip)
	res = requests.get(url).json()
	
	Information["OfferNumber"] = len(res['payload']['offers'])
	for itemnumbers in list(res['payload']['offers']):
		#itemnumbers is the name of each result
		InStock = res['payload']['offers']['D8800B11F7074BB9B2D60B61421B52A6']['productAvailability']['availabilityStatus']
		Discount = res['payload']['offers'][itemnumbers]['pricesInfo']['savings']['savingsAmount']['price']
		CurrentPrice = res['payload']['offers'][itemnumbers]['pricesInfo']['priceMap']['CURRENT']['price']
		ListPrice = res['payload']['offers'][itemnumbers]['pricesInfo']['priceMap']['LIST']['price']
		Rank = res['payload']['offers'][itemnumbers]['pricesInfo']['priceFlags'][0]['rank']
		ShipPass = res['payload']['offers'][itemnumbers]['offerInfo']['shippingPassEligible']
		Min = res['payload']['offers'][itemnumbers]['offerInfo']['quantityOptions']['orderMinLimit']
		Limit = res['payload']['offers'][itemnumbers]['offerInfo']['quantityOptions']['orderLimit']


	#Information["Results"]
	return res

