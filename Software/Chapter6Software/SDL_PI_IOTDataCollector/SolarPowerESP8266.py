#
# SolarPowerESP8266
# 
# parsing and storage data
#
# SwitchDoc Labs
# December 2015
#
import time
import datetime

import MySQLdb as mdb

def parseSolarPowerESP8266(data):
	
	type = data["name"]
	deviceid = data["id"]
	timestamp = data["variables"]["RestTimeStamp"]
	dataString = data["variables"]["RestDataString"]
	firmwareversion = data["variables"]["FirmwareVersion"]

	ts = time.time()
	receivedTimeStamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	print "%s: sampling SolarPowerESP8266 data" % receivedTimeStamp


	#print "%s: type= %s deviceid=%s timestamp=%s dataString=%s" % (receivedTimeStamp, type, deviceid, timestamp, dataString)


	con = mdb.connect('localhost', 'root', 'password', 'IOTSolarData');


	# you must create a Cursor object. It will let
	# you execute all the queries you need
	cur = con.cursor()

	# read all data out of JSON
	samples = dataString.split("|") 

	if (len(samples) > 1):
		# we have data

		print "%i sample(s) read" % (len(samples) -1)	
		for i in range(len(samples)):

			values = samples[i].split(',')
			if (i == 0):
				heap_available = int(samples[i])
			else:
				sample_timestamp = int(values[0])	
				battery_load_voltage = float(values[2])	
				battery_current = float(values[3])	
				solarcell_load_voltage = float(values[5])
				solarcell_current = float(values[6])	
				output_load_voltage = float(values[8])	
				output_current = float(values[9])	

				query = 'INSERT INTO SolarPowerData(timestamp,type, deviceid, firmwareversion, heap_available, sample_timestamp, battery_load_voltage, battery_current, solarcell_load_voltage, solarcell_current, output_load_voltage, output_current) VALUES(UTC_TIMESTAMP(), "%s", "%s", "%s", %d, %d, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f)' %( type, deviceid, firmwareversion, heap_available, sample_timestamp, battery_load_voltage, battery_current, solarcell_load_voltage, solarcell_current, output_load_voltage, output_current) 
				#print("query=%s" % query)

				cur.execute(query)
	
	con.commit()	
