#light control
#
# JCS 06/09/14
#

# controls the lights from Hue

import sys
from phue import Bridge

import bubblelog

# set up the hue variable
hue = None

sys.path.append('./config')


def initializeHue(address):
	global hue
	hue = Bridge(address) 

def setInitialLightState(currentLightState):
	global hue
	return

	
# if conflocal.py is not found, import default conf.py

# Check for user imports
try:
        import conflocal as conf
except ImportError:
	        import conf

import utils

def checkForLightTrigger (myPosition, currentDistanceSensitivity, currentBrightnessSensitivity, lightStateArray):
	global hue	

	for light in conf.LightList:
		
		# check for light match
		lightDistance = utils.distanceBetweenTwoPoints([light[2], light[3]], myPosition)
		brightness = getTheBrightness(lightDistance, currentBrightnessSensitivity)
		if (lightDistance < currentDistanceSensitivity):
			print "Brightness set to: %3.2f" % brightness	
			if (lightStateArray[light[0]] == 1):
				print "Light %i:%s is already ON" % (light[0], light[1])
			else:
				print "Turn Light %i:%s ON" % (light[0], light[1])
				lightStateArray[light[0]] = 1
				hue.set_light(light[7],'on', True)
				bubblelog.writeToBubbleLog("Light#%i (%s) turned ON " % (light[0], light[1]) )
				#hue.set_light(light[7],'bri', (brightness *256))

		elif (lightDistance > currentDistanceSensitivity):
			if (lightStateArray[light[0]] == 0):
				print "Light %i:%s is already OFF" % (light[0], light[1])
			else:
				print "Turn Light %i:%s OFF" % (light[0], light[1])
				lightStateArray[light[0]] = 0
				hue.set_light(light[7],'on', False)
				bubblelog.writeToBubbleLog("Light#%i (%s) turned OFF " % (light[0], light[1]) )
	
	

def getTheBrightness(lightDistance, currentBrightnessSensitivity):

	global hue 
	newBrightness = (1.0 - lightDistance/currentBrightnessSensitivity)
	if (newBrightness > 1.0):
		newBrightness = 1.0 
	elif (newBrightness < 0.0):
		newBrightness = 0.0
		

	return newBrightness
	

def allLights(ON_OFF, lightStateArray):
	global hue
	
	for light in conf.LightList:
		print "Setting light:", light[0]
		if (ON_OFF == True):
			lightStateArray[light[0]] = 1
		else:
			lightStateArray[light[0]] = 0


		hue.set_light(light[7],'on', ON_OFF)
		
	
	
