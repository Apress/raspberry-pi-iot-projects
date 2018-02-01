# utils for BeaconAir
# jcs 6/8/2014


from threading import Thread
import sys
import time
import datetime

import subprocess

sys.path.append('./config')

# if conflocal.py is not found, import default conf.py

# Check for user imports
try:
        import conflocal as conf
except ImportError:
	        import conf



# beacon processing routines

def clearOldValues(seconds, RSSIArray, TimeStampArray, rollingRSSIArray):

	#print "checking old values len(RSSIArray)=", len(RSSIArray)
	for i in range(0, len(RSSIArray)):
		if (int(RSSIArray[i]) < 0):
			#print "beaconnumber=", i, "TSI+secon=", TimeStampArray[i] + seconds, "time.time()=", time.time()
			if (TimeStampArray[i] + seconds < time.time()):
				# clear value - too old
				print "Beacon", i, " purged"
				RSSIArray[i] = 1 # 1 means cleared, 0 is never found	
				rollingRSSIArray[i] = 1 # 1 means cleared, 0 is never found	
			

def checkForMatch(UDID, Major, Minor):

	beaconID = -1
	for beacon in conf.BeaconList:
		if (UDID == beacon[4]):
			# now check major and minor numbers
			if (int(Major) == beacon[5]):
				if (int(Minor) == beacon[6]):
					beaconID = beacon[0]
					break
			
	return beaconID


# read incoming list and update time of last contact and RSSI
def processiBeaconList(incomingBeaconList, RSSIArray, TimeStampArray, rollingRSSIArray):

	# parse the incoming beacon list

	for beaconEntry in incomingBeaconList:
		#print "Beacon=", beaconEntry
		beacon = beaconEntry.split(",");
		UDID = beacon[1]
		Major = beacon[2]
		Minor = beacon[3]
		# strip " " and "-"
		UDID = UDID.replace(" ", "")
		UDID = UDID.replace("-", "")
		UDID = UDID.upper()
		
		beaconnumber = checkForMatch(UDID, Major, Minor)
		if (beaconnumber > -1):  # beacon found
	 		#print "beaconnumberFound = ", beaconnumber	

			if (int(RSSIArray[beaconnumber]) > -1):  # reset rolling average
				rollingRSSIArray[beaconnumber] = float(beacon[5])
			RSSIArray[beaconnumber] = beacon[5]
			TimeStampArray[beaconnumber] = time.time()
			kFilteringFactor = 0.1
			rollingRSSIArray[beaconnumber] = (int(beacon[5]) * kFilteringFactor) + (rollingRSSIArray[beaconnumber] * (1.0 - kFilteringFactor))



# distance and accuracy routines


def XcalculateDistanceWithRSSI(rssi,beaconnumber): 
    #formula adapted from David Young's Radius Networks Android iBeacon Code
    if (rssi == 0): 
        return -1.0; # if we cannot determine accuracy, return -1.
    

    beacon = conf.BeaconList[beaconnumber];  
    txPower = beacon[7] 
    ratio = float(rssi)*1.0/float(txPower);
    if (ratio < 1.0) :
        return pow(ratio,10);
    else:
        accuracy =  (0.89976) * pow(ratio,7.7095) + 0.111;
        return accuracy;


def calculateDistanceWithRSSI(rssi,beaconnumber): 

  	
    	beacon = conf.BeaconList[beaconnumber];  
    	txPower = beacon[7] 
	ratio_db = txPower - rssi;
   	ratio_linear = pow(10, ratio_db / 10);
    	r = pow(ratio_linear, .5);
    	return r


def distanceBetweenTwoPoints(point1, point2):
	
	dist = ( (point2[0] - point1[0])**2 + (point2[1] - point1[1])**2 )**0.5
	return dist


def getXYFrom3Beacons(beaconnumbera, beaconnumberb, beaconnumberc, rollingRSSIArray):

	beacona = conf.BeaconList[beaconnumbera];
	beaconb = conf.BeaconList[beaconnumberb];
	beaconc = conf.BeaconList[beaconnumberc];
	xa = float(beacona[2])
	ya = float(beacona[3])
	xb = float(beaconb[2])
	yb = float(beaconb[3])
	xc = float(beaconc[2])
	yc = float(beaconc[3])

	ra = float(calculateDistanceWithRSSI(rollingRSSIArray[beaconnumbera], beaconnumbera ))
	rb = float(calculateDistanceWithRSSI(rollingRSSIArray[beaconnumberb], beaconnumberb ))
	rc = float(calculateDistanceWithRSSI(rollingRSSIArray[beaconnumberc], beaconnumberc ))

	#print "xa,ya:", xa,ya, "xb,yb", xb,yb, "xc,yc", xc,yc, "ra, rb, rc", ra, rb, rc
	S = (pow(xc, 2.) - pow(xb, 2.) + pow(yc, 2.) - pow(yb, 2.) + pow(rb, 2.) - pow(rc, 2.)) / 2.0
	T = (pow(xa, 2.) - pow(xb, 2.) + pow(ya, 2.) - pow(yb, 2.) + pow(rb, 2.) - pow(ra, 2.)) / 2.0

	#print "S,T=", S, T
	#print "((ya - yb) * (xb - xc)) ", ((ya - yb) * (xb - xc)) 
	#print "((yc - yb) * (xb - xa)) ", ((yc - yb) * (xb - xa)) 
	#print "denominator=", (((ya - yb) * (xb - xc)) - ((yc - yb) * (xb - xa)))

	try:
		y = ((T * (xb - xc)) - (S * (xb - xa))) / (((ya - yb) * (xb - xc)) - ((yc - yb) * (xb - xa)))
		x = ((y * (ya - yb)) - T) / (xb - xa)

	except ZeroDivisionError as detail:
		print 'Handling run-time error:', detail
		return [-1,-1]
	
	point = [x, y] 
	
	return point

def AlternativeGetXYFrom3Beacons(beaconnumbera, beaconnumberb, beaconnumberc, rollingRSSIArray):

	beacona = conf.BeaconList[beaconnumbera];
	beaconb = conf.BeaconList[beaconnumberb];
	beaconc = conf.BeaconList[beaconnumberc];
	ax = float(beacona[2])
	ay = float(beacona[3])
	bx = float(beaconb[2])
	by = float(beaconb[3])
	cx = float(beaconc[2])
	cy = float(beaconc[3])

	dA = float(calculateDistanceWithRSSI(rollingRSSIArray[beaconnumbera], beaconnumbera ))
	dB = float(calculateDistanceWithRSSI(rollingRSSIArray[beaconnumberb], beaconnumberb ))
	dC = float(calculateDistanceWithRSSI(rollingRSSIArray[beaconnumberc], beaconnumberc ))

	x = ( ( (pow(dA,2)-pow(dB,2)) + (pow(cx,2)-pow(ax,2)) + (pow(by,2)-pow(ay,2)) ) * (2*cy-2*by) - ( (pow(dB,2)-pow(dC,2)) + (pow(cx,2)-pow(cx,2)) + (pow(cy,2)-pow(by,2)) ) *(2*by-2*ay) ) / ( (2*bx-2*cx)*(2*by-2*ay)-(2*ax-2*bx)*(2*cy-2*by) );

	y = ( (pow(dA,2)-pow(dB,2)) + (pow(cx,2)-pow(ax,2)) + (pow(by,2)-pow(ay,2)) + x*(2*ax-2*bx)) / (2*by-2*ay);


	point = [x, y] 
	
	return point


def haveThreeGoodBeacons(rollingRSSIArray):

	goodbeacons = 0
	for i in range(0, len(rollingRSSIArray)):
		if (rollingRSSIArray[i] < 0):
			goodbeacons += 1
	print "goodbeacons=", goodbeacons
	return goodbeacons	


def get_item(item):
	return item[1]

def get3ClosestBeacons(rollingRSSIArray):

	#print ("len=", len(rollingRSSIArray))
	sortedBeacons = []
	for i in range(0, len(rollingRSSIArray)):
		sortedBeacons.append([i, rollingRSSIArray[i]])
	
	#print("beaconlist=", sortedBeacons)

	mySorted = sorted(sortedBeacons, key=get_item)

	#print("as beaconlist=", mySorted)

	return [mySorted[0][0], mySorted[1][0], mySorted[2][0]]


# debugging routines


def printBeaconStatus(beacon, RSSIArray, TimeStampArray, rollingRSSIArray):

	print "----------"
	print "BeaconNumber: ", beacon[0]	
	print "BeaconName: ", beacon[1]	
	print "x,y: ", beacon[2], beacon[3]	
	print "UDID: ", beacon[4]	
	print "Major: ", beacon[5]	
	print "Minor: ", beacon[6]	
	print "Last RSSI: ", RSSIArray[beacon[0]]	
	print "Rolling RSSI: ", rollingRSSIArray[beacon[0]]	
	print "TimeStamp: ", datetime.datetime.fromtimestamp(TimeStampArray[beacon[0]])	
	print "----------"

def printBeaconDistance(beacon, RSSIArray, TimeStampArray,rollingRSSIArray):

	print "BN: ", beacon[0],"x,y: ", beacon[2], beacon[3],"RSSI:", RSSIArray[beacon[0]], "rollingRSSI: %3.2f" % rollingRSSIArray[beacon[0]] , "Distance: %3.2f" % calculateDistanceWithRSSI(rollingRSSIArray[beacon[0]], beacon[0])	
		


