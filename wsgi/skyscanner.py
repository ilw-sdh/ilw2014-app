from urllib2 import urlopen
from urllib import quote_plus

import json

API_ROOT = 'http://partners.api.skyscanner.net/apiservices'
API_KEY = 'ilw02375360823411197864901011420'

def get(path):
	print API_ROOT + path + "?apiKey=ilw02375360823411197864901011420"
	raw = urlopen(API_ROOT + path + "?apiKey=ilw02375360823411197864901011420").read()
	return json.loads(raw)

# Returns a list of quotes with attribute:
# QuoteId, MinPrice, Direct, OutboundLeg / InboundLeg { CarrierIds, OriginId, DestinationId, DepartureDate }
def find_cheapest_quotes(origin, destination):
	data = get("/browsequotes/v1.0/GB/GBP/en-GB/%s/%s/anytime/anytime" % (origin, destination))
	return data['Quotes']

def url_for_journey(origin, destination):
	return API_ROOT + "/referral/v1.0/GB/GBP/en-GB/%s/%s/anytime/anytime" % (origin, destination)

	#best_quote = reduce(lambda x, y: x if x['MinPrice'] < y['MinPrice'] else y, data['Quotes'])
	#best_quote['url'] = get_quote_url(best_quote)