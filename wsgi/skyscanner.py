import xml.etree.ElementTree as ET
from urllib2 import urlopen
from urllib import quote_plus

import json

API_ROOT = 'http://partners.api.skyscanner.net/apiservices'
API_KEY = 'ilw02375360823411197864901011420'

def get(path):
	print API_ROOT + path + "?apiKey=ilw02375360823411197864901011420"
	raw = urlopen(API_ROOT + path + "?apiKey=ilw02375360823411197864901011420").read()
	return json.loads(raw)

def find_best_quote(origin, destination):
	print (str(origin), destination)
	data = get("/browsequotes/v1.0/GB/GBP/en-GB/%s/%s/anytime/anytime" % (origin, destination))
	best_quote = reduce(lambda x, y: x if x['MinPrice'] < y['MinPrice'] else y, data['Quotes'])
	return best_quote

def get_quote_url(quote):
	origin = quote['InboundLeg']['OriginId']
	destination = quote['OutboundLeg']['OriginId']
	inbound_date = quote['InboundLeg']['DepartureDate']
	outbound_date = quote['OutboundLeg']['DepartureDate']
	data = ("/referral/v1.0/GB/GBP/en-GB/%s/%s/%s/%s" % (origin, destination, quote_plus(outbound_date), quote_plus(inbound_date)))
	return data

print get_quote_url(find_best_quote('EDI', 'BRU'))