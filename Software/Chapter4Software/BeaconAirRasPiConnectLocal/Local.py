#!/usr/bin/python
# Filename: local.py 
# SwitchDoc Labs 
# Version 1.8 6/19/2014 
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

sys.path.append('../BeaconAir/config')

# if conflocal.py is not found, import default conf.py

# Check for user imports
try:
        import conflocal as conf
except ImportError:
        import conf

#
#
# Command to Beacon Air procdures
#
#
def sendCommandToBeaconAirAndWait(command):
	status = True
	print "Sending Command: ", command

        f = open("/home/pi/BeaconAir/state/BeaconAirCommand.txt", "w")
        f.write(command)
        f.close()	
	timeout = 20		
	commandresponse = ""
	while timeout > 0:
		time.sleep(1.0)
		print "Waiting for Response"

        	f = open("/home/pi/BeaconAir/state/BeaconAirCommand.txt", "r")
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

def sendCommandToBeaconAirAndReturn(command):

	return



def ExecuteUserObjects(objectType, element):

	# Example Objects

	# fetch information from XML for use in user elements

	#objectServerID is the RasPiConnect ID from the RasPiConnect App

        objectServerID = element.find("./OBJECTSERVERID").text
        objectID = element.find("./OBJECTID").text
        objectAction = element.find("./OBJECTACTION").text
        objectName = element.find("./OBJECTNAME").text

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

	#
	# W-10 Main plan  Web page screen 
	if (objectServerID == "W-10"):	

               	#check for validate request
		# validate allows RasPiConnect to verify this object is here 

               	if (validate == "YES"):
                       	outgoingXMLData += Validate.buildValidateResponse("YES")
                       	outgoingXMLData += BuildResponse.buildFooter()
                       	return outgoingXMLData

		# not validate request, so execute

		# note that python is in the main directory for this call, not the local directory

		# read an HTML template into aw string

		
		responseData = "<html><head>"
              	responseData += "<title></title><style>body,html,iframe{margin:0;padding:0;}"
		tempString = ""
		try:
       			f = open("/home/pi/RasPiConnectServer/Templates/W-1b.txt", "r")
              		tempString = f.read()
               		f.close()
		except IOError as e:
			tempString = ""	

		responseData += tempString
 		responseData += "</style>"

		#responseData += "<META HTTP-EQUIV='CACHE-CONTROL' CONTENT='NO-CACHE'>"
             	responseData += "</head>"
		# read in the rest of the css definitions 

              	responseData += "<body>"

         	responseData += "<div style='position: relative; left: 0; top: 0;'>\n"
               	responseData += "<img src='http://rfw.wardner.com:9600/static/mainplanfull.png' style='position: relative; top: 0; left: 0;'/>\n"

		# read in the rest of the objects
		tempString = ""
		try:
       			f = open("/home/pi/RasPiConnectServer/Templates/W-1a.txt", "r")
              		tempString = f.read()
               		f.close()
		except IOError as e:
			tempString = ""	

		responseData += tempString


               	responseData += "</div>"


               	responseData +="</body>"

              	responseData += "</html>"

		print "responseData =", responseData

               	outgoingXMLData += BuildResponse.buildResponse(responseData)
      		outgoingXMLData += BuildResponse.buildFooter()
               	return outgoingXMLData
		

	#
	# BTL-1 Bubble Log
	if (objectServerID == "BTL-1"):	

               	#check for validate request
		# validate allows RasPiConnect to verify this object is here 

               	if (validate == "YES"):
                       	outgoingXMLData += Validate.buildValidateResponse("YES")
                       	outgoingXMLData += BuildResponse.buildFooter()
                       	return outgoingXMLData

		responseData =""
		# not validate request, so execute

		# note that python is in the main directory for this call, not the local directory
		try:
       			f = open("/home/pi/BeaconAir/state/bubblelog.txt", "r")
              		tempString = f.read()
              		f.close()
			os.remove("/home/pi/BeaconAir/state/bubblelog.txt")
		except IOError as e:
			tempString = ""	

		responseData = tempString


		print "responseData =", responseData

               	outgoingXMLData += BuildResponse.buildResponse(responseData)
      		outgoingXMLData += BuildResponse.buildFooter()
               	return outgoingXMLData
		


	# DSPL-1 Dynamic Spark Line event driven 
	if (objectServerID == "DSPL-1"):	

               	#check for validate request
		# validate allows RasPiConnect to verify this object is here 

               	if (validate == "YES"):
                       	outgoingXMLData += Validate.buildValidateResponse("YES")
                       	outgoingXMLData += BuildResponse.buildFooter()
                       	return outgoingXMLData

		responseData =""
		# not validate request, so execute

		# note that python is in the main directory for this call, not the local directory
		try:
       			f = open("/home/pi/BeaconAir/state/distancejitter.txt", "r")
              		tempString = f.read()
              		f.close()
			os.remove("/home/pi/BeaconAir/state/distancejitter.txt")
		except IOError as e:
			tempString = ""	

		responseData = tempString


		print "responseData =", responseData

               	outgoingXMLData += BuildResponse.buildResponse(responseData)
      		outgoingXMLData += BuildResponse.buildFooter()
               	return outgoingXMLData
		
	# SLGL-1 - Beacon count
	if (objectServerID == "SLGL-1"):	

               	#check for validate request
		# validate allows RasPiConnect to verify this object is here 
                if (validate == "YES"):
                        outgoingXMLData += Validate.buildValidateResponse("YES")
                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData

                # normal response requested
		try:
        		f = open("/home/pi/BeaconAir/state/iBeaconCountGraph.txt", "r")
        		commandresponse = f.read()
        		f.close()	
		except IOError as e:
			commandresponse = "0^^0||No Data from BeaconAir^^"			

                outgoingXMLData += BuildResponse.buildResponse(commandresponse)


                outgoingXMLData += BuildResponse.buildFooter()
                return outgoingXMLData	

	# SL-1 - Sensitivity in meters 
	if (objectServerID == "SL-1"):	

               	#check for validate request
		# validate allows RasPiConnect to verify this object is here 
                if (validate == "YES"):
                        outgoingXMLData += Validate.buildValidateResponse("YES")
                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData

                # normal response requested
		commandresponse = objectAction	
	
		if (float(commandresponse) < 0.15):
                	try:
       	                 	f = open("/home/pi/BeaconAir/state/distanceSensitivity.txt", "r")
       	                 	commandresponse = f.read()
       	                 	f.close()
       	         	except:
                        	commandresponse = "2.0"
	
    		f = open("/home/pi/BeaconAir/state/distanceSensitivity.txt", "w")
        	f.write(commandresponse)
        	f.close()
		status = sendCommandToBeaconAirAndWait("UPDATESENSITIVITIES")
		# Not LIVE values, just send "" back
		
		commandresponse = ""
		
                outgoingXMLData += BuildResponse.buildResponse(commandresponse)


                outgoingXMLData += BuildResponse.buildFooter()
                return outgoingXMLData	

	# SL-2 - Brightness Sensitivity in meters 
	if (objectServerID == "SL-2"):	

               	#check for validate request
		# validate allows RasPiConnect to verify this object is here 
                if (validate == "YES"):
                        outgoingXMLData += Validate.buildValidateResponse("YES")
                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData

                # normal response requested
		commandresponse = objectAction	
		if (float(commandresponse) < 0.15):
                	try:
                        	f = open("/home/pi/BeaconAir/state/brightnessSensitivity.txt", "r")
                        	commandresponse = f.read()
                        	f.close()
                	except:
                        	commandresponse = "2.0" 

    		f = open("/home/pi/BeaconAir/state/brightnessSensitivity.txt", "w")
        	f.write(commandresponse)
        	f.close()
		status = sendCommandToBeaconAirAndWait("UPDATESENSITIVITIES")
		# Not LIVE values, just send "" back
		
		commandresponse = ""
		
                outgoingXMLData += BuildResponse.buildResponse(commandresponse)


                outgoingXMLData += BuildResponse.buildFooter()
                return outgoingXMLData	

	# LT-1 - display beacon count 
	if (objectServerID == "LT-1"):	

               	#check for validate request
		# validate allows RasPiConnect to verify this object is here 
                if (validate == "YES"):
                        outgoingXMLData += Validate.buildValidateResponse("YES")
                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData

                # normal response requested
		
		try:
       			f = open("/home/pi/BeaconAir/state/beaconCount.txt", "r")
              		tempString = f.read()
               		f.close()
		except IOError as e:
			tempString = "no count"	
		
		commandresponse = tempString + ", "+ tempString + ", iBeacon Count "

 
		
                outgoingXMLData += BuildResponse.buildResponse(commandresponse)


                outgoingXMLData += BuildResponse.buildFooter()
                return outgoingXMLData	


	# FB-5 -  turn beacon reception on / off 
	if (objectServerID == "FB-5"):	

               	#check for validate request
		# validate allows RasPiConnect to verify this object is here 
               	if (validate == "YES"):
                        outgoingXMLData += Validate.buildValidateResponse("YES")
                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData

		# not validate request, so execute

                responseData = "XXX"
 

                if (objectName is None):
                        objectName = "XXX"

               	lowername = objectName.lower()


               	if (lowername == "enable beacons"):

			status = sendCommandToBeaconAirAndWait("BEACONON") 
                       	responseData = "disable beacons" 
                       	responseData = responseData.title()


               	elif (lowername == "disable beacons"):

			status = sendCommandToBeaconAirAndWait("BEACONOFF")
                       	responseData = "enable beacons" 
                       	responseData = responseData.title()


		 # defaults to on 
               	else:
			status = sendCommandToBeaconAirAndWait("BEACONON") 
                       	lowername = "disable beacons" 
                       	responseData = lowername.title()


               	outgoingXMLData += BuildResponse.buildResponse(responseData)
      		outgoingXMLData += BuildResponse.buildFooter()
               	return outgoingXMLData





	# FB-1 -  turns display beacons on or off
	if (objectServerID == "FB-1"):	

               	#check for validate request
		# validate allows RasPiConnect to verify this object is here 
               	if (validate == "YES"):
                        outgoingXMLData += Validate.buildValidateResponse("YES")
                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData

		# not validate request, so execute

                responseData = "XXX"
 

                if (objectName is None):
                        objectName = "XXX"

               	lowername = objectName.lower()


               	if (lowername == "display beacons on"):

			status = sendCommandToBeaconAirAndWait("DISPLAYBEACONON") 
                       	responseData = "display beacons off" 
                       	responseData = responseData.title()


               	elif (lowername == "display beacons off"):

			status = sendCommandToBeaconAirAndWait("DISPLAYBEACONOFF")
                       	responseData = "display beacons on" 
                       	responseData = responseData.title()


		 # defaults to on 
               	else:
			status = sendCommandToBeaconAirAndWait("DISPLAYBEACONON") 
                       	lowername = "display beacons off" 
                       	responseData = lowername.title()


               	outgoingXMLData += BuildResponse.buildResponse(responseData)
      		outgoingXMLData += BuildResponse.buildFooter()
               	return outgoingXMLData


	# FB-4 -  turns display beacons on or off
	if (objectServerID == "FB-4"):	

               	#check for validate request
		# validate allows RasPiConnect to verify this object is here 
               	if (validate == "YES"):
                        outgoingXMLData += Validate.buildValidateResponse("YES")
                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData

		# not validate request, so execute

                responseData = "XXX"
 

                if (objectName is None):
                        objectName = "XXX"

               	lowername = objectName.lower()


               	if (lowername == "display lights on"):

			status = sendCommandToBeaconAirAndWait("DISPLAYLIGHTSON") 
                       	responseData = "display beacons off" 
                       	responseData = responseData.title()


               	elif (lowername == "display lights off"):

			status = sendCommandToBeaconAirAndWait("DISPLAYLIGHTSOFF")
                       	responseData = "display beacons on" 
                       	responseData = responseData.title()


		 # defaults to on 
               	else:
			status = sendCommandToBeaconAirAndWait("DISPLAYLIGHTSON") 
                       	lowername = "display lights off" 
                       	responseData = lowername.title()


               	outgoingXMLData += BuildResponse.buildResponse(responseData)
      		outgoingXMLData += BuildResponse.buildFooter()
               	return outgoingXMLData


	# FB-2 -  turns display beacons on or off
	if (objectServerID == "FB-2"):	

               	#check for validate request
		# validate allows RasPiConnect to verify this object is here 
               	if (validate == "YES"):
                        outgoingXMLData += Validate.buildValidateResponse("YES")
                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData

		# not validate request, so execute

                responseData = "XXX"
 

                if (objectName is None):
                        objectName = "XXX"

               	lowername = objectName.lower()


               	if (lowername == "all lights on"):

			status = sendCommandToBeaconAirAndWait("ALLLIGHTSON") 
                       	responseData = "all lights off" 
                       	responseData = responseData.title()


               	elif (lowername == "all lights off"):

			status = sendCommandToBeaconAirAndWait("ALLLIGHTSOFF")
                       	responseData = "all lights on" 
                       	responseData = responseData.title()


		 # defaults to on 
               	else:
			status = sendCommandToBeaconAirAndWait("ALLLIGHTSON") 
                       	lowername = "all lights off" 
                       	responseData = lowername.title()


               	outgoingXMLData += BuildResponse.buildResponse(responseData)
      		outgoingXMLData += BuildResponse.buildFooter()
               	return outgoingXMLData



	else:
		return ""
	# returning a zero length string tells the server that you have not matched 
	# the object and server 
	return ""

