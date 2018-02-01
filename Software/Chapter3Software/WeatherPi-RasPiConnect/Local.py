#!/usr/bin/python 
# Filename: local.py 
# SunAir SwitchDoc Labs
# Version 1.0 01/04/2015
# 
# Local Execute Objects for RasPiConnect  
# to add Execute objects, modify this file 
# 
#
#

# system imports
import sys
import subprocess
import os
import time
# RasPiConnectImports

import Config
import Validate
import BuildResponse 
from time import gmtime, strftime

import MySQLdb as mdb

#
#
# Command to WeatherPiSolarPowerecWeatherStation procdures
#
#
def sendCommandToWeatherPiAndWait(command):
	status = True
	print "Sending Command: ", command

        f = open("/home/pi/WeatherPiSolarPoweredWeather/state/WeatherCommand.txt", "w")
        f.write(command)
        f.close()	
	timeout = 20		
	commandresponse = ""
	while timeout > 0:
		time.sleep(1.0)
		print "Waiting for Response"

        	f = open("/home/pi/WeatherPiSolarPoweredWeather/state/WeatherCommand.txt", "r")
        	commandresponse = f.read()
        	f.close()	
		timeout = timeout-1
		if (commandresponse == "DONE"):
			status = True
			print "Response = DONE"
			timeout = 0
		else:
			status = False
		 
	return status

def sendCommandToWeatherPiAndWaitReturningValue(command):
	status = True
	print "Sending Command For Return Value: ", command

        f = open("/home/pi/WeatherPiSolarPoweredWeather/state/WeatherCommand.txt", "w")
        f.write(command)
        f.close()	
	timeout = 20		
	commandresponse = ""
	while timeout > 0:
		time.sleep(1.0)
		print "Waiting for Response"

        	f = open("/home/pi/WeatherPiSolarPoweredWeather/state/WeatherCommand.txt", "r")
        	commandresponse = f.read()
		value = f.read()
        	f.close()	
		timeout = timeout-1
		if (commandresponse == "DONE"):
			status = value
			print "Response = ", value
			timeout = 0
		else:
			status = "TimeOut"
		 
	return status

def sendCommandToWeatherPiAndReturn(command):

	return

def setupSunAirPlusStats():

        global batteryVoltage, batteryCurrent, solarVoltage, solarCurrent, loadVoltage, loadCurrent
        global batteryPower, solarPower, loadPower, batteryCharge

        f = open("/home/pi/WeatherPiSolarPoweredWeather/state/SunAirPlusStats.txt", "r")
        batteryVoltage = float(f.readline())
	batteryCurrent = float(f.readline())
	solarVoltage = float(f.readline())
	solarCurrent = float(f.readline())
	loadVoltage = float(f.readline())
	loadCurrent = float(f.readline())
        batteryPower = float(f.readline())
	solarPower = float(f.readline())
	loadPower = float(f.readline())
	batteryCharge = float(f.readline())
        f.close()	

def setupWeatherStats():

        global totalRain, as3935LightningCount
        global as3935LastInterrupt, as3935LastDistance, as3935LastStatus
        global currentWindSpeed, currentWindGust, totalRain
        global  bmp180Temperature, bmp180Pressure, bmp180Altitude,  bmp180SeaLevel
        global outsideTemperature, outsideHumidity
        global currentWindDirection, currentWindDirectionVoltage

	global insideTemperature, insideHumidity

        f = open("/home/pi/WeatherPiSolarPoweredWeather/state/WeatherStats.txt", "r")
        totalRain = f.readline()
        as3935LightningCount = float(f.readline())
        as3935LastInterrupt = float(f.readline())
        as3935LastDistance = float(f.readline())
        as3935LastStatus = f.readline()
        currentWindSpeed = float(f.readline())
        currentWindGust = float(f.readline())
        totalRain = float(f.readline())
        bmp180Temperature = float(f.readline())
        bmp180Pressure = float(f.readline())
        bmp180Altitude = float(f.readline())
        bmp180SeaLevel = float(f.readline())
        outsideTemperature = float(f.readline())
        outsideHumidity = float(f.readline())
	currentWindDirection = float(f.readline())
	currentWindDirectionVoltage = float(f.readline())
        insideTemperature = float(f.readline())
        insideHumidity = float(f.readline())
	


        f.close()	


def ExecuteUserObjects(objectType, element):


	# Example Objects

	# fetch information from XML for use in user elements

        objectServerID = element.find("./OBJECTSERVERID").text
        objectID = element.find("./OBJECTID").text
	objectAction = element.find(".OBJECTACTION").text	
	objectName = element.find("./OBJECTNAME").text
        objectFlags = element.find("./OBJECTFLAGS").text


        if (Config.debug()):
        	print("objectServerID = %s" % objectServerID)
	# 
	# check to see if this is a Validate request
	#
        validate = Validate.checkForValidate(element)

        if (Config.debug()):
        	print "VALIDATE=%s" % validate

        
	# Build the header for the response

	outgoingXMLData = BuildResponse.buildHeader(element)

	# SS-1 - Server Present 
        if (objectServerID == "SS-1"):

                #check for validate request
                # validate allows RasPiConnect to verify this object is here
                if (validate == "YES"):
                        outgoingXMLData += Validate.buildValidateResponse("YES")
                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData

                # normal response requested
		answ = "2"
		#answ = ""
		if (Config.debug()):
			print "In local SS-1"
			print("answ = %s" % answ)
		responseData = answ
		print "sampling weather"
		sendCommandToWeatherPiAndWait("SAMPLEBOTH")

		# now setup internal variables

		setupWeatherStats()
		setupSunAirPlusStats()

                outgoingXMLData += BuildResponse.buildResponse(responseData)
                outgoingXMLData += BuildResponse.buildFooter()
                return outgoingXMLData
		


	# B-1 - Sample Both and Do All Graphs 
        if (objectServerID == "B-1"):

                #check for validate request
                # validate allows RasPiConnect to verify this object is here
                if (validate == "YES"):
                        outgoingXMLData += Validate.buildValidateResponse("YES")
                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData

                # normal response requested
		answ = "OK"
		#answ = ""
		if (Config.debug()):
			print "In local B-1"
			print("answ = %s" % answ)

		print "sampling weather"
		sendCommandToWeatherPiAndWait("SAMPLEBOTHGRAPHS")

		# now setup internal variables

		setupWeatherStats()
		setupSunAirPlusStats()

		responseData = "OK"

                outgoingXMLData += BuildResponse.buildResponse(responseData)
                outgoingXMLData += BuildResponse.buildFooter()
                return outgoingXMLData
		
	# FB-2 - Graph Selection Feedback
        if (objectServerID == "FB-2"):

                #check for validate request
                # validate allows RasPiConnect to verify this object is here
                if (validate == "YES"):
                        outgoingXMLData += Validate.buildValidateResponse("YES")
                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData

                # normal response requested
		responseData = "XXX"
		if (objectName is None):
			objectName = "XXX"
		
		lowername = objectName.lower()
		
		if (lowername == "wind graph"):

			responseData = "temp / hum graph"
			responseData = responseData.title()	
               		f = open("./local/GraphSelect.txt", "w")
               		f.write(lowername)
               		f.close()

		elif (lowername == "temp / hum graph"):

			responseData = "baro graph"
			responseData = responseData.title()	
               		f = open("./local/GraphSelect.txt", "w")
               		f.write(lowername)
               		f.close()

		elif (lowername == "baro graph"):

			responseData = "voltage graph"
			responseData = responseData.title()	
               		f = open("./local/GraphSelect.txt", "w")
               		f.write(lowername)
               		f.close()

		elif (lowername == "voltage graph"):

			responseData = "system logs"
			responseData = responseData.title()	
               		f = open("./local/GraphSelect.txt", "w")
               		f.write(lowername)
               		f.close()
		
		elif (lowername == "system logs"):

			responseData = "current graph"
			responseData = responseData.title()	
               		f = open("./local/GraphSelect.txt", "w")
               		f.write(lowername)
               		f.close()

		elif (lowername == "current graphs"):

			responseData = "wind graph"
			responseData = responseData.title()	
               		f = open("./local/GraphSelect.txt", "w")
               		f.write(lowername)
               		f.close()

		else: 
			# default value
			responseData = "temp / hum graph"
			responseData = responseData.title()	
               		f = open("./local/GraphSelect.txt", "w")
               		f.write(lowername)
               		f.close()




		if (Config.debug()):
			print "In local FB-2"
			print("responseData = %s" % responseData)

                outgoingXMLData += BuildResponse.buildResponse(responseData)
                outgoingXMLData += BuildResponse.buildFooter()
                return outgoingXMLData
		
	# W-1 - Graph View 
        if (objectServerID == "W-1"):

                #check for validate request
                # validate allows RasPiConnect to verify this object is here
                if (validate == "YES"):
                        outgoingXMLData += Validate.buildValidateResponse("YES")
                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData

                # normal response requested
		#answ = ""
		if (Config.debug()):
			print "In local W-1"


		lowername = "voltage graph"

		try:
              		f = open("./local/GraphSelect.txt", "r")
               		tempString = f.read()
               		f.close()
			lowername = tempString 		

		except IOError as e:
			print "I/O error({0}): {1}".format(e.errno, e.strerror)

                
		print "lowername=", lowername	
		if (lowername == "voltage graph"):

			imageName = "PowerVoltageGraph.png"

		elif (lowername == "current graph"):

			imageName = "PowerCurrentGraph.png"
		
		elif (lowername == "baro graph"):

			imageName = "BarometerLightningGraph.png"

		elif (lowername == "temp / hum graph"):

			imageName = "TemperatureHumidityGraph.png"
		
		elif (lowername == "system logs"):

				# grab the system logs
				with open ("./Templates/W-16-SL.html", "r") as myfile:
					import time
					responseData = "System Time: "
					responseData +=  time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
					responseData += "<BR>\n"
    					responseData += myfile.read().replace('\n', '')
		
		        	try:
                			print("trying database")
					DATABASEPASSWORD = "rmysqlpassword"
                			db = mdb.connect('localhost', 'root', DATABASEPASSWORD, 'WeatherPi');
		
                			cursor = db.cursor()


					query = "SELECT TimeStamp, Level, Source, Message FROM systemlog ORDER BY ID DESC LIMIT 30"
                			cursor.execute(query)

					rows = cursor.fetchall()
					CRITICAL=50
					ERROR=40
					WARNING=30
					INFO=20
					DEBUG=10
					NOTSET=0

					for row in rows:
						level = row[1]	
						levelName = "NONE"
						if (level == DEBUG):
							levelName = "DEBUG"
						if (level == INFO):
							levelName = "INFO"
						if (level == WARNING):
							levelName = "WARNING"
						if (level == ERROR):
							levelName = "ERROR"
						if (level == CRITICAL):
							levelName = "CRITICAL"

						logline = "%s:%s:%s:%s" % (row[0], levelName, row[2], row[3] )
						line = logline+"<BR>\n<!--INSERTLOGS-->"	

						responseData = responseData.replace("<!--INSERTLOGS-->", line)	



        			except mdb.Error, e:
		
                			print "Error %d: %s" % (e.args[0],e.args[1])

        			finally:
		
                			cursor.close()
                			db.close()
			
                			del cursor
                			del db
		
                		outgoingXMLData += BuildResponse.buildResponse(responseData)
                		outgoingXMLData += BuildResponse.buildFooter()
                		return outgoingXMLData



		else:
			imageName = "PowerVoltageGraph.png"



              	responseData = "<html><head>"
                responseData += "<title></title><style>body,html,iframe{margin:0;padding:0;}</style>"
		responseData += "<META HTTP-EQUIV='CACHE-CONTROL' CONTENT='NO-CACHE, MUST-REVALIDATE'>"
		responseData += "<META HTTP-EQUIV='PRAGMA' CONTENT='NO-CACHE'>"
                responseData += "</head>"
               	responseData += "<body><img src=\""
               	responseData += Config.localURL()
               	responseData += "static/"
		import random
		answer = random.randrange(0,100,1)

               	responseData += imageName + "?x" + str(answer )
               	responseData += "\" type=\"jpg\" width=\"730\" height=\"300\">"

               	responseData +="</body>"
	
               	responseData += "</html>"


                outgoingXMLData += BuildResponse.buildResponse(responseData)
                outgoingXMLData += BuildResponse.buildFooter()
                return outgoingXMLData
		
	# AIL-1 - Activity Indicator - LIVE
        if (objectServerID == "AIL-1"):

                #check for validate request
                # validate allows RasPiConnect to verify this object is here
                if (validate == "YES"):
                        outgoingXMLData += Validate.buildValidateResponse("YES")
                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData

                # normal response requested
		#answ = "NO"
		answ = "YES"
		#answ = ""
		if (Config.debug()):
			print "In local AIL-1"
			print("answ = %s" % answ)
		responseData = answ

                outgoingXMLData += BuildResponse.buildResponse(responseData)
                outgoingXMLData += BuildResponse.buildFooter()
                return outgoingXMLData
		
	# BTL-1 Bubble Table 
	if (objectServerID == "BTL-1"):	

               	#check for validate request
		# validate allows RasPiConnect to verify this object is here 

               	if (validate == "YES"):
                       	outgoingXMLData += Validate.buildValidateResponse("YES")
                       	outgoingXMLData += BuildResponse.buildFooter()
                       	return outgoingXMLData

		#
		#
		# Execute your code
		#
		#

		#
        	if (Config.debug()):
        		print "In Local BTL-1"
		
       		time = strftime("%H:%M:%S", gmtime())
		responseData =  time+as3935LastStatus+"\n"+"Lighting Count="+str(int(as3935LightningCount))
        	if (Config.debug()):
			print "responseData =", responseData

		#
		#
		# Done with your code
		#
		#

               	outgoingXMLData += BuildResponse.buildResponse(responseData)
      		outgoingXMLData += BuildResponse.buildFooter()
               	return outgoingXMLData
	

	# BR-1 - Power Left in Battery 
        if (objectServerID == "BR-1"):

                #check for validate request
                # validate allows RasPiConnect to verify this object is here
                if (validate == "YES"):
                        outgoingXMLData += Validate.buildValidateResponse("YES")
                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData

                # normal response requested
		answ = str(batteryCharge)
		#answ = ""
		if (Config.debug()):
			print "In local BR-1"
			print("answ = %s" % answ)
		responseData = answ

                outgoingXMLData += BuildResponse.buildResponse(responseData)
                outgoingXMLData += BuildResponse.buildFooter()
                return outgoingXMLData
	
	# LT-5 - Sample Count

        if (objectServerID == "LT-5"):

                #check for validate request
                # validate allows RasPiConnect to verify this object is here
                if (validate == "YES"):
                        outgoingXMLData += Validate.buildValidateResponse("YES")
                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData

                # normal response requested
		answ = "0"
		#answ = ""
		if (Config.debug()):
			print "In local LT-5"
			print("answ = %s" % answ)
		responseData = answ

                outgoingXMLData += BuildResponse.buildResponse(responseData)
                outgoingXMLData += BuildResponse.buildFooter()
                return outgoingXMLData
		
	
	# LT-4 - Server Present - Power From Battery
        if (objectServerID == "LT-4"):

                #check for validate request
                # validate allows RasPiConnect to verify this object is here
                if (validate == "YES"):
                        outgoingXMLData += Validate.buildValidateResponse("YES")
                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData

                # normal response requested
		answ = "%0.0f mA/%0.2f W" % (batteryCurrent, batteryPower)
		#answ = ""
		if (Config.debug()):
			print "In local LT-4"
			print("answ = %s" % answ)
		responseData = answ

                outgoingXMLData += BuildResponse.buildResponse(responseData)
                outgoingXMLData += BuildResponse.buildFooter()
                return outgoingXMLData
		
	
	# LT-2 - Server Present - Power From Solar Cells 
        if (objectServerID == "LT-2"):

                #check for validate request
                # validate allows RasPiConnect to verify this object is here
                if (validate == "YES"):
                        outgoingXMLData += Validate.buildValidateResponse("YES")
                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData

                # normal response requested
		answ = "%0.0f mA/%0.2f W" % (solarCurrent, solarPower)
		#answ = ""
		if (Config.debug()):
			print "In local LT-2"
			print("answ = %s" % answ)
		responseData = answ

                outgoingXMLData += BuildResponse.buildResponse(responseData)
                outgoingXMLData += BuildResponse.buildFooter()
                return outgoingXMLData
		
	# LT-3 - Server Present - Power Into Pi
        if (objectServerID == "LT-3"):

                #check for validate request
                # validate allows RasPiConnect to verify this object is here
                if (validate == "YES"):
                        outgoingXMLData += Validate.buildValidateResponse("YES")
                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData

                # normal response requested
		answ = "%0.0f mA/%0.2f W" % (loadCurrent, loadPower)
		#answ = ""
		if (Config.debug()):
			print "In local LT-3"
			print("answ = %s" % answ)
		responseData = answ

                outgoingXMLData += BuildResponse.buildResponse(responseData)
                outgoingXMLData += BuildResponse.buildFooter()
                return outgoingXMLData
		
	
	# DLU-3 - Wind Speed Text 
        if (objectServerID == "DLU-3"):

                #check for validate request
                # validate allows RasPiConnect to verify this object is here
                if (validate == "YES"):
                        outgoingXMLData += Validate.buildValidateResponse("YES")
                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData
		
		

                # normal response requested
		answ = "Wind Speed: %0.2f MPH" % currentWindSpeed 
		#answ = ""
		if (Config.debug()):
			print "In local DLU-3"
			print("answ = %s" % answ)
		responseData = answ

                outgoingXMLData += BuildResponse.buildResponse(responseData)
                outgoingXMLData += BuildResponse.buildFooter()
                return outgoingXMLData

	# DLU-4 - Wind Gust 
        if (objectServerID == "DLU-4"):

                #check for validate request
                # validate allows RasPiConnect to verify this object is here
                if (validate == "YES"):
                        outgoingXMLData += Validate.buildValidateResponse("YES")
                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData

                # normal response requested
		answ = "Wind Gust: %0.2f MPH" % currentWindGust
		#answ = ""
		if (Config.debug()):
			print "In local DLU-4"
			print("answ = %s" % answ)
		responseData = answ

                outgoingXMLData += BuildResponse.buildResponse(responseData)
                outgoingXMLData += BuildResponse.buildFooter()
                return outgoingXMLData



	# DLU-5 - Outside Temperature 
        if (objectServerID == "DLU-5"):

                #check for validate request
                # validate allows RasPiConnect to verify this object is here
                if (validate == "YES"):
                        outgoingXMLData += Validate.buildValidateResponse("YES")
                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData

                # normal response requested
		answ = "Outside Temperature: %0.2f C" % outsideTemperature
		#answ = ""
		if (Config.debug()):
			print "In local DLU-5"
			print("answ = %s" % answ)
		responseData = answ

                outgoingXMLData += BuildResponse.buildResponse(responseData)
                outgoingXMLData += BuildResponse.buildFooter()
                return outgoingXMLData



	# DLU-6 - Outside Humidity 
        if (objectServerID == "DLU-6"):

                #check for validate request
                # validate allows RasPiConnect to verify this object is here
                if (validate == "YES"):
                        outgoingXMLData += Validate.buildValidateResponse("YES")
                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData

                # normal response requested
		answ = "Outside Humidity: %0.2f %%" % outsideHumidity
		#answ = ""
		if (Config.debug()):
			print "In local DLU-6"
			print("answ = %s" % answ)
		responseData = answ

                outgoingXMLData += BuildResponse.buildResponse(responseData)
                outgoingXMLData += BuildResponse.buildFooter()
                return outgoingXMLData



	# DLU-7 - Barometric Pressure 
        if (objectServerID == "DLU-7"):

                #check for validate request
                # validate allows RasPiConnect to verify this object is here
                if (validate == "YES"):
                        outgoingXMLData += Validate.buildValidateResponse("YES")
                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData

                # normal response requested
		answ = "Barometric Pressure: %0.2f mbar" % (bmp180SeaLevel * 10)
		#answ = ""
		if (Config.debug()):
			print "In local DLU-7"
			print("answ = %s" % answ)
		responseData = answ

                outgoingXMLData += BuildResponse.buildResponse(responseData)
                outgoingXMLData += BuildResponse.buildFooter()
                return outgoingXMLData



	# DLU-8 - Inside Temperature 
        if (objectServerID == "DLU-8"):

                #check for validate request
                # validate allows RasPiConnect to verify this object is here
                if (validate == "YES"):
                        outgoingXMLData += Validate.buildValidateResponse("YES")
                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData

                # normal response requested


		
		if (Config.debug()):
			print "In local DLU-8"

		responseData = "Inside Temperature: %0.2f C" % bmp180Temperature
		

                outgoingXMLData += BuildResponse.buildResponse(responseData)
                outgoingXMLData += BuildResponse.buildFooter()
                return outgoingXMLData


	# DLU-9 - Rain Total 
        if (objectServerID == "DLU-9"):

                #check for validate request
                # validate allows RasPiConnect to verify this object is here
                if (validate == "YES"):
                        outgoingXMLData += Validate.buildValidateResponse("YES")
                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData

                # normal response requested


		
		if (Config.debug()):
			print "In local DLU-9"

		responseData = "Rain Total: %0.2f In" % totalRain
		

                outgoingXMLData += BuildResponse.buildResponse(responseData)
                outgoingXMLData += BuildResponse.buildFooter()
                return outgoingXMLData


	# DLU-10 - Wind Direction 
        if (objectServerID == "DLU-10"):

                #check for validate request
                # validate allows RasPiConnect to verify this object is here
                if (validate == "YES"):
                        outgoingXMLData += Validate.buildValidateResponse("YES")
                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData

                # normal response requested


		
		if (Config.debug()):
			print "In local DLU-10"

		responseData = "Wind Direction: %0.2f deg" % currentWindDirection
		

                outgoingXMLData += BuildResponse.buildResponse(responseData)
                outgoingXMLData += BuildResponse.buildFooter()
                return outgoingXMLData

	# DLU-11 - Inside Humidity 
        if (objectServerID == "DLU-11"):

                #check for validate request
                # validate allows RasPiConnect to verify this object is here
                if (validate == "YES"):
                        outgoingXMLData += Validate.buildValidateResponse("YES")
                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData

                # normal response requested


		
		if (Config.debug()):
			print "In local DLU-11"

		responseData = "Inside Humidity: %0.2f %%" % insideHumidity
		

                outgoingXMLData += BuildResponse.buildResponse(responseData)
                outgoingXMLData += BuildResponse.buildFooter()
                return outgoingXMLData



	# M-4 - Wind Speed 
        if (objectServerID == "M-4"):

                #check for validate request
                # validate allows RasPiConnect to verify this object is here
                if (validate == "YES"):
                        outgoingXMLData += Validate.buildValidateResponse("YES")
                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData

                # normal response requested
		answ = "%0.2f" % currentWindSpeed
		#answ = ""
		if (Config.debug()):
			print "In local M-4"
			print("answ = %s" % answ)
		responseData = answ

                outgoingXMLData += BuildResponse.buildResponse(responseData)
                outgoingXMLData += BuildResponse.buildFooter()
                return outgoingXMLData
		

	# M-2 - Solar Voltage 
        if (objectServerID == "M-2"):

                #check for validate request
                # validate allows RasPiConnect to verify this object is here
                if (validate == "YES"):
                        outgoingXMLData += Validate.buildValidateResponse("YES")
                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData

                # normal response requested
		answ = str(solarVoltage) 
		#answ = ""
		if (Config.debug()):
			print "In local M-2"
			print("answ = %s" % answ)
		responseData = answ

                outgoingXMLData += BuildResponse.buildResponse(responseData)
                outgoingXMLData += BuildResponse.buildFooter()
                return outgoingXMLData
		
	# M-3 - Battery Voltage 
        if (objectServerID == "M-3"):

                #check for validate request
                # validate allows RasPiConnect to verify this object is here
                if (validate == "YES"):
                        outgoingXMLData += Validate.buildValidateResponse("YES")
                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData

                # normal response requested
		answ = str(batteryVoltage) 
		#answ = ""
		if (Config.debug()):
			print "In local M-3"
			print("answ = %s" % answ)
		responseData = answ

                outgoingXMLData += BuildResponse.buildResponse(responseData)
                outgoingXMLData += BuildResponse.buildFooter()
                return outgoingXMLData
		
	# SLGL-1 Simple Line Graph - LIVE
	if (objectServerID == "SLGL-1"):	

               	#check for validate request
		# validate allows RasPiConnect to verify this object is here 

               	if (validate == "YES"):
                       	outgoingXMLData += Validate.buildValidateResponse("YES")
                       	outgoingXMLData += BuildResponse.buildFooter()
                       	return outgoingXMLData

		#
		#
		# Execute your code
		#
		#

		#
        	if (Config.debug()):
        		print "In Local SLGL-1"

		import random
		#answer = random.randrange(0,100,1)
		answer = "68672.000000^^17457.000000^^16954.000000^^723.000000^^10874.000000^^10367.000000^^59561.000000^^56276.000000^^6379.000000^^40763.000000||"
		responseData = answer 
		
        	if (Config.debug()):
			print "responseData =", responseData

		#
		#
		# Done with your code
		#
		#

               	outgoingXMLData += BuildResponse.buildResponse(responseData)
      		outgoingXMLData += BuildResponse.buildFooter()
               	return outgoingXMLData

	# SLGL-2 Simple Line Graph - LIVE
	if (objectServerID == "SLGL-2"):	

               	#check for validate request
		# validate allows RasPiConnect to verify this object is here 

               	if (validate == "YES"):
                       	outgoingXMLData += Validate.buildValidateResponse("YES")
                       	outgoingXMLData += BuildResponse.buildFooter()
                       	return outgoingXMLData

		#
		#
		# Execute your code
		#
		#

		#
        	if (Config.debug()):
        		print "In Local SLGL-2"

		import random
		#answer = random.randrange(0,100,1)
		answer = "68672.000000^^17457.000000^^16954.000000^^723.000000^^10874.000000^^10367.000000^^59561.000000^^56276.000000^^6379.000000^^40763.000000||"
		responseData = answer 
		
        	if (Config.debug()):
			print "responseData =", responseData

		#
		#
		# Done with your code
		#
		#

               	outgoingXMLData += BuildResponse.buildResponse(responseData)
      		outgoingXMLData += BuildResponse.buildFooter()
               	return outgoingXMLData
	


	# returning a zero length string tells the server that you have not matched 
	# the object and server 
	return ""

