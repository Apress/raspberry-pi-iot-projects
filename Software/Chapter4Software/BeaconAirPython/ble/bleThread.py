# bleThread - background thread reading BLE adverts
# jcs 6/8/2014
#

import sys
import time


import bluetooth._bluetooth as bluez


sys.path.append('/home/pi/BeaconAir/config')
sys.path.append('/home/pi/BeaconAir/ble')


import blescan
import utils




def bleDetect(source, repeatcount, queue):




	dev_id = 0
	try:
    		sock = bluez.hci_open_dev(dev_id)
	except:
    		print "error accessing bluetooth device..."
    		sys.exit(1)
	blescan.hci_le_set_scan_parameters(sock)
	blescan.hci_enable_le_scan(sock)


        while True:
		returnedList = blescan.parse_events(sock, repeatcount)
		#print "result put in queue"
		#print "returnList = ", returnedList
                queue.put(returnedList)
		





