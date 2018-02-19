#!/usr/bin/env python

import rospy
from std_msgs.msg import Int16MultiArray
from std_msgs.msg import String
from rosserial_python import SerialClient, RosSerialServer
from serial import SerialException
import os.path
from time import sleep
import multiprocessing
import couchdb
from pyswip import Prolog, registerForeign

import sys

prolog = Prolog()
prolog.assertz("sensorup(1)")

# DB connection

couchServer = couchdb.Server('http://192.168.1.10:5984/')
user = "admin"
password = "mysecretpassword"
couchserver = couchdb.Server("http://%s:%s@192.168.1.10:5984/" % (user, password))

dbname = "robotics_mazesolver"
if dbname in couchserver:
    db = couchserver[dbname]
else:
    db = couchserver.create(dbname)

doc_id, doc_rev = db.save({'sensorsHIT': {'s1': 0, 's2': 0, 's3': 0} })
sensors = [0, 0, 0]

def think(data):
        #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
        #print(data.data)
        if data.data[1]==1:
                pub = rospy.Publisher('leftlogic',String,queue_size=10)
        elif data.data[2]==1:
                pub = rospy.Publisher('forwardlogic',String,queue_size=10)
        elif data.data[3]==1:
                pub = rospy.Publisher('rightlogic',String,queue_size=10)
        elif data.data[4]==0:
                pub = rospy.Publisher('leftfinal',String,queue_size=10)
        elif data.data[4]==2:
                pub = rospy.Publisher('rightfinal',String,queue_size=10)
        if data.data[3]==1:
                pub = rospy.Publisher('right',String,queue_size=10)
        else:
                pub = rospy.Publisher('arriving',String,queue_size=10)
        
        for i in range(1, 4):
            s = data.data[i]
            if prolog.query("sensorup(%d)" % s):
                sensors[i-1] += s
                doc_id, doc_rev = db.save({'sensorsHIT': {'s1': sensors[0], 's2': sensors[1], 's3': sensors[2]} })

        pub.publish("yes");

if __name__=="__main__":

        rospy.init_node("serial_node")
        rospy.loginfo("ROS Serial Python Node")
        

        port_name = rospy.get_param('~port','/dev/arduino')
        baud = int(rospy.get_param('~baud','57600'))

        # for systems where pyserial yields errors in the fcntl.ioctl(self.fd, TIOCMBIS, \
        # TIOCM_DTR_str) line, which causes an IOError, when using simulated port
        fix_pyserial_for_test = rospy.get_param('~fix_pyserial_for_test', False)

        while not rospy.is_shutdown():
                rospy.loginfo("Connecting to %s at %d baud" % (port_name,baud) )
                rospy.Subscriber("sensors", Int16MultiArray, think)
                try:
                        if os.path.exists('/dev/arduino'):
                                client = SerialClient(port_name, baud)
                                client.run()
                        else:
                                sleep(1.0)
                                continue
                except KeyboardInterrupt:
                        break
                except SerialException:
                        sleep(1.0)
                        continue
                except OSError:
                        sleep(1.0)
                        continue
                except Exception as e:
                        print e
                        sleep(1.0)
                        continue


