#
#
# IOT Data Collector
#
# SwitchDoc Labs
# December 2015
#

import httplib2 as http
import json

import time

import SolarPowerESP8266


try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

# fetch the JSON data from the IOT device
def fetchJSONData(uri, path):
	target = urlparse(uri+path)
	method = 'GET'
	body = ''

	h = http.Http()
	
	# If you need authentication some example:
	#if auth:
	#    h.add_credentials(auth.user, auth.password)

	response, content = h.request(
        	target.geturl(),
        	method,
        	body,
        	headers)

	# assume that content is a json reply
	# parse content with the json module
	data = json.loads(content)

	return data

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json; charset=UTF-8'
}

# main program
uri = 'http://192.168.1.129'
path = '/'



while True:

	data = fetchJSONData(uri, path)

	if (data['name'] == "SolarPowerESP8266"):
		SolarPowerESP8266.parseSolarPowerESP8266(data)

	#print( data['id'], data['name'])

	time.sleep(60.0)
