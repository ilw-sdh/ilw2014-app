from urllib2 import urlopen
from urllib import quote_plus

import json

API_ROOT = 'http://partners.api.skyscanner.net/apiservices'
API_KEY = "ilw02375360823411197864901011420"

def get(path):
	print API_ROOT + path + "?apiKey=" + API_KEY
	raw = urlopen(API_ROOT + path + "?apiKey=" + API_KEY).read()
	return json.loads(raw)

# Returns a list of quotes with attribute:
# QuoteId, MinPrice, Direct, OutboundLeg / InboundLeg { CarrierIds, OriginId, DestinationId, DepartureDate }
def find_cheapest_quotes(origin, destination):
	data = get("/browsequotes/v1.0/GB/GBP/en-GB/%s/%s/anytime/anytime" % (origin, destination))
	quotes = data['Quotes']
	for q in quotes:
		q['OutboundLeg']['Carrier'] = get_carrier_by_id(q['OutboundLeg']['CarrierIds'][0], data['Carriers'])
		q['InboundLeg']['Carrier'] = get_carrier_by_id(q['InboundLeg']['CarrierIds'][0], data['Carriers'])
	return data['Quotes']

def get_carrier_by_id(id, carriers):
	for c in carriers:
		if c['CarrierId'] == id:
			return c['Name']
	return 'Unknown'

def url_for_journey(origin, destination):
	return API_ROOT + "/referral/v1.0/GB/GBP/en-GB/%s/%s/anytime/anytime" % (origin, destination)

	#best_quote = reduce(lambda x, y: x if x['MinPrice'] < y['MinPrice'] else y, data['Quotes'])
	#best_quote['url'] = get_quote_url(best_quote)
