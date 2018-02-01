#!/usr/bin/python 
# Filename: local.py 
# MiloCreek BP MiloCreek 
# Version 3.0 6/11/2014 
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

import RPi.GPIO as GPIO ## Import GPIO library
GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
f = open("/home/pi/LightSwarm/state/LS-1.txt", "w")
f.write("0")
f.close()	



#
#
# Command to LightSwarm procdures
#
#
def sendCommandToLightSwarmAndWait(command):
	status = True
	print "Sending Command: ", command

        f = open("/home/pi/LightSwarm/state/LSCommand.txt", "w")
        f.write(command)
        f.close()	
	timeout = 20		
	commandresponse = ""
	while timeout > 0:
		time.sleep(1.0)
		print "Waiting for Response"

        	f = open("/home/pi/LightSwarm/state/LSCommand.txt", "r")
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

def sendCommandToLightSwarmAndWaitReturningValue(command):
	
	print "Sending Command For Return Value: ", command

        f = open("/home/pi/LightSwarm/state/LSCommand.txt", "w")
        f.write(command)
        f.close()	
	timeout = 20		
	commandresponse = ""
	while timeout > 0:
		time.sleep(1.0)
		print "Waiting for Response"

        	f = open("/home/pi/LightSwarm/state/LSCommand.txt", "r")
        	commandresponse = f.read()
		print "commandresponse=|%s|"% commandresponse
        	f.close()	

		timeout = timeout-1
		if (commandresponse == "DONE"):
			timeout = 0
        		f = open("/home/pi/LightSwarm/state/LSResponse.txt", "r")
        		value = f.read()
        		f.close()	
			print "Response = ", value
		else:
			value = "TimeOut"
		 
	return value




def ExecuteUserObjects(objectType, element):

	# Example Objects

	# fetch information from XML for use in user elements

	#objectServerID is the RasPiConnect ID from the RasPiConnect App


        objectServerID = element.find("./OBJECTSERVERID").text
        objectID = element.find("./OBJECTID").text
	objectAction = element.find("./OBJECTACTION").text	
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
       
	# blink selected light button 

	if (objectServerID == "B-2"):

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
			print "In local B-2"
			print("answ = %s" % answ)

        	try:
			f = open("/home/pi/LightSwarm/state/LS-1.txt", "r")
        		lightSelected = f.read()
        		f.close()	
			print "lightSelected = ",lightSelected
			lightSelected = int(float(lightSelected))
		except:
			lightSelected = 0

		print "sampling weather"
		sendCommandToLightSwarmAndWait("BLINKLIGHT,"+str(lightSelected))

		responseData = "OK"

                outgoingXMLData += BuildResponse.buildResponse(responseData)
                outgoingXMLData += BuildResponse.buildFooter()
                return outgoingXMLData

	# reset selected
	if (objectServerID == "B-3"):

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
			print "In local B-2"
			print("answ = %s" % answ)

        	try:
			f = open("/home/pi/LightSwarm/state/LS-1.txt", "r")
        		lightSelected = f.read()
        		f.close()	
			print "lightSelected = ",lightSelected
			lightSelected = int(float(lightSelected))
		except:
			lightSelected = 0

		print "sampling weather"
		sendCommandToLightSwarmAndWait("RESETSELECTED,"+str(lightSelected))

		responseData = "OK"

                outgoingXMLData += BuildResponse.buildResponse(responseData)
                outgoingXMLData += BuildResponse.buildFooter()
                return outgoingXMLData

	#  Reset Swarm

	if (objectServerID == "B-4"):

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
			print "In local B-4"
			print("answ = %s" % answ)

		sendCommandToLightSwarmAndWait("RESETSWARM")

		responseData = "OK"

                outgoingXMLData += BuildResponse.buildResponse(responseData)
                outgoingXMLData += BuildResponse.buildFooter()
                return outgoingXMLData
		
	# send Server to Swarm
	if (objectServerID == "B-5"):

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
			print "In local B-5"
			print("answ = %s" % answ)

		sendCommandToLightSwarmAndWait("SENDSERVER")

		responseData = "OK"

                outgoingXMLData += BuildResponse.buildResponse(responseData)
                outgoingXMLData += BuildResponse.buildFooter()
                return outgoingXMLData
		

	# Webview for device status

	if (objectServerID == "W-10"):	

		if (Config.debug()):
			print "In local W-10"


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

              	responseData += "<body style='font-family:Verdana'>"
         	responseData += "<div style='position: relative; left: 0; top: 0;'>\n"
               	#responseData += "<img src='http://rfw.wardner.com:9600/static/mainplanfull.png' style='position: relative; top: 0; left: 0;'/>\n"

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
		

	if (objectServerID == "M-1"):	

       	        #check for validate request
               	if (validate == "YES"):
                       	outgoingXMLData += Validate.buildValidateResponse("YES")
                       	outgoingXMLData += BuildResponse.buildFooter()

                       	return outgoingXMLData
        
		try:	
        		f = open("/home/pi/LightSwarm/state/LSStatus.txt", "r")
        		logString = f.read()
        		f.close()	
		except:
			logString = ""

		responseData = "%3.2f" % logString.count("PR")
		print "%s = %s" % (objectServerID, responseData)

               	outgoingXMLData += BuildResponse.buildResponse(responseData)
 		outgoingXMLData += BuildResponse.buildFooter()
               	return outgoingXMLData

	if (objectServerID == "M-2"):	

       	        #check for validate request
               	if (validate == "YES"):
                       	outgoingXMLData += Validate.buildValidateResponse("YES")
                       	outgoingXMLData += BuildResponse.buildFooter()

                       	return outgoingXMLData
        
		try:	
        		f = open("/home/pi/LightSwarm/state/LSStatus.txt", "r")
        		logString = f.read()
        		f.close()	
		except:
			logString = ""

		responseData = "%3.2f" % logString.count("TO")
		print "%s = %s" % (objectServerID, responseData)

               	outgoingXMLData += BuildResponse.buildResponse(responseData)
 		outgoingXMLData += BuildResponse.buildFooter()
               	return outgoingXMLData


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

		# now setup internal variables


                outgoingXMLData += BuildResponse.buildResponse(responseData)
                outgoingXMLData += BuildResponse.buildFooter()
                return outgoingXMLData
		

	#
	if (objectServerID == "BTL-1"):	

               	#check for validate request
		# validate allows RasPiConnect to verify this object is here 

               	if (validate == "YES"):
                       	outgoingXMLData += Validate.buildValidateResponse("YES")
                       	outgoingXMLData += BuildResponse.buildFooter()
                       	return outgoingXMLData

		# not validate request, so execute
		#
		
		#
		#
		# Execute your code
		#
		#

        	if (Config.debug()):
        		print("BTL-1 # %s: Status" % objectServerID)
		
		responseData = sendCommandToLightSwarmAndWaitReturningValue("STATUS")
		
		f = open("/home/pi/LightSwarm/state/LSStatus.txt", "w")
        	f.write(responseData)
        	f.close()	



		print "responseData =", responseData

		#
		#
		# Done with your code
		#
		#

               	outgoingXMLData += BuildResponse.buildResponse(responseData)
      		outgoingXMLData += BuildResponse.buildFooter()
               	return outgoingXMLData
		
	#
	if (objectServerID == "SL-1"):	

               	#check for validate request
		# validate allows RasPiConnect to verify this object is here 

               	if (validate == "YES"):
                       	outgoingXMLData += Validate.buildValidateResponse("YES")
                       	outgoingXMLData += BuildResponse.buildFooter()
                       	return outgoingXMLData

		# not validate request, so execute
		#
		
		#
		#
		# Execute your code
		#
		#

        	if (Config.debug()):
        		print("SL-1 # %s: Status" % objectServerID)
		
		responseData = ""

		
        	f = open("/home/pi/LightSwarm/state/LS-1.txt", "w")
        	f.write(objectAction)
        	f.close()	

		print "responseData =", responseData

		#
		#
		# Done with your code
		#
		#

               	outgoingXMLData += BuildResponse.buildResponse(responseData)
      		outgoingXMLData += BuildResponse.buildFooter()
               	return outgoingXMLData
		


	else:
		# returning a zero length string tells the server that you have not matched 
		# the object and server 
		return ""


	
