# Generates graph of all voltages measured on the SolarPowerESP8266 
# filename: SolarPowerESP8266VoltageGraph.py
# Version 1.0 December 2015
# SwitchDoc Labs 
#
#
#


import sys
import time

import gc
import datetime

import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')

from matplotlib import pyplot
from matplotlib import dates

import pylab

import MySQLdb as mdb



def SolarPowerESP8266VoltageGraph(source,days):


    print("SolarPowerESP8266VoltageGraph source:%s days:%s " % (source,days))
    print("SolarPowerESP8266VoltageGraph running now")


    # now we have get the data, stuff it in the graph

    try:
        print("trying database")
        db = mdb.connect('localhost', 'root', 'password', 'IOTSolarData');

        cursor = db.cursor()

        query = "SELECT TimeStamp, sample_timestamp, battery_load_voltage, solarcell_load_voltage, output_load_voltage FROM SolarPowerData where now() - interval %i hour < TimeStamp ORDER BY TimeStamp, sample_timestamp" % (days*24)
        cursor.execute(query)


        result = cursor.fetchall()
        t = []
        s = []
        u = []
        v = []

        for record in result:
            t.append(record[0])
            s.append(record[2])
            u.append(record[3])
            v.append(record[4])

        print ("count of t=",len(t))

        #dts = map(datetime.datetime.fromtimestamp, t)
        #print dts
        fds = dates.date2num(t) # converted
        # matplotlib date format object
        hfmt = dates.DateFormatter('%m/%d-%H')

        fig = pyplot.figure()
        fig.set_facecolor('white')
        ax = fig.add_subplot(111,axisbg = 'white')
        ax.vlines(fds, -200.0, 1000.0,colors='w')

        ax.xaxis.set_major_locator(dates.HourLocator(interval=6))
        ax.xaxis.set_major_formatter(hfmt)
        ax.set_ylim(bottom = -200.0)
        pyplot.xticks(rotation='vertical')
        pyplot.subplots_adjust(bottom=.3)
        pylab.plot(t, s, color='r',label="Battery Voltage",linestyle="-",marker=".")
        pylab.plot(t, u, color='b',label="SolarCell Voltage",linestyle="-",marker=".")
        pylab.plot(t, v, color='g',label="ESP8266 Voltage",linestyle="-",marker=".")
        pylab.xlabel("Hours")
        pylab.ylabel("Voltage")
        pylab.legend(loc='lower left')

        pylab.axis([min(t), max(t), 0, 7])
        pylab.figtext(.5, .05, ("SolarPowerESP8266 Voltages Last %i Days" % days),fontsize=18,ha='center')

        pylab.grid(True)

        pyplot.show()
        pyplot.savefig("static/solarvoltagegraph.png")
        pyplot.savefig("/var/www/solarvoltagegraph.png")

    except mdb.Error, e:

        print "Error %d: %s" % (e.args[0],e.args[1])

    finally:

        cursor.close()
        db.close()

        del cursor
        del db

        fig.clf()
        pyplot.close()
        pylab.close()
        del t, s, u, v
        gc.collect()
        print("SolarPowerESP8266VoltageGraph finished now")
