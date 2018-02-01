#
#
# Builds iBeaconCount graph string 
# filename: detection.py
# Version 1.0 06/19/2014 
#
#


import sys
import time

import utils


sys.path.append('/home/pi/BeaconAir/config')


#global variables

datalist = [];
# if conflocal.py is not found, import default conf.py

# Check for user imports
try:
	import conflocal as conf
except ImportError:
	import conf


def buildGraphString():

	global datalist

	response = ""
	valuecount = ""
        f = open("/home/pi/BeaconAir/state/iBeaconCountGraph.txt", "w")
	for i in range(len(datalist)):
	 	response += str(datalist[i])
		valuecount += str(i)
		if (i < len(datalist)-1):
			response +="^^"
			valuecount +="^^"

	if (len(response) != 0):
		fullresponse = response + "||" + valuecount	
	else:
		fullresponse = ""

        f.write(fullresponse)
        
	f.close() 


def iBeacondetect(RSSIArray):

	global datalist

	count = 0
	for beacon in RSSIArray:
		if (beacon < 0):
			count += 1


	if (len(datalist) == 10):
		if (len(datalist) > 0):
			datalist.pop(0)
	datalist.append(count)	

	buildGraphString()
	f = open("/home/pi/BeaconAir/state/beaconCount.txt", "w") 
	f.write(str(count))
	f.close() 

	return count
