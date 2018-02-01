# bubblelog.py
# logs system information to RasPiConnect Bubble Control
#
# jcs 6/10/14
#

from time import gmtime, strftime
def writeToBubbleLog(message):

       f = open("/home/pi/BeaconAir/state/bubblelog.txt", "a")
       time = strftime("%H:%M:%S", gmtime())
       f.write(time+":"+message+"\n")
       f.close()


