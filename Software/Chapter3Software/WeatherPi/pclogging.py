#
#
# logging system from Project Curacao 
# filename: pclogger.py
# Version 1.0 10/04/13
#
# contains logging data 
#


CRITICAL=50
ERROR=40
WARNING=30
INFO=20
DEBUG=10
NOTSET=0


import sys
import time
import MySQLdb as mdb

DATABASEPASSWORD = "rmysqlpassword"

def log(level, source, message):

   LOWESTDEBUG = 0
	# open mysql database

	# write log


	# commit


	# close

   if (level >= LOWESTDEBUG):
        try:
	
                #print("trying database")
                con = mdb.connect('localhost', 'root', DATABASEPASSWORD, 'WeatherPi');

                cur = con.cursor()
                #print "before query"

                query = "INSERT INTO systemlog(TimeStamp, Level, Source, Message) VALUES(UTC_TIMESTAMP(), %i, '%s', '%s')" % (level, source, message)
	        #print("query=%s" % query)

                cur.execute(query)

                con.commit()


        except mdb.Error, e:

                print "Error %d: %s" % (e.args[0],e.args[1])
                con.rollback()
                #sys.exit(1)

        finally:
                cur.close()
                con.close()

                del cur
                del con

