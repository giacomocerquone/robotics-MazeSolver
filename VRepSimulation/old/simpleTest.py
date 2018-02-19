# Copyright 2006-2017 Coppelia Robotics GmbH. All rights reserved. 
# marc@coppeliarobotics.com
# www.coppeliarobotics.com
# 
# -------------------------------------------------------------------
# THIS FILE IS DISTRIBUTED "AS IS", WITHOUT ANY EXPRESS OR IMPLIED
# WARRANTY. THE USER WILL USE IT AT HIS/HER OWN RISK. THE ORIGINAL
# AUTHORS AND COPPELIA ROBOTICS GMBH WILL NOT BE LIABLE FOR DATA LOSS,
# DAMAGES, LOSS OF PROFITS OR ANY OTHER KIND OF LOSS WHILE USING OR
# MISUSING THIS SOFTWARE.
# 
# You are free to use/modify/distribute this file for whatever purpose!
# -------------------------------------------------------------------
#
# This file was automatically created for V-REP release V3.4.0 rev. 1 on April 5th 2017

# Make sure to have the server side running in V-REP: 
# in a child script of a V-REP scene, add following command
# to be executed just once, at simulation start:
#
# simExtRemoteApiStart(19999)
#
# then start simulation, and run this program.
#
# IMPORTANT: for each successful call to simxStart, there
# should be a corresponding call to simxFinish at the end!

try:
	import vrep
except:
	print ('--------------------------------------------------------------')
	print ('"vrep.py" could not be imported. This means very probably that')
	print ('either "vrep.py" or the remoteApi library could not be found.')
	print ('Make sure both are in the same folder as this file,')
	print ('or appropriately adjust the file "vrep.py"')
	print ('--------------------------------------------------------------')
	print ('')

import time
sim_boolparam_vision_sensor_handling_enabled = 10


print ('Program started')
vrep.simxFinish(-1) # just in case, close all opened connections
clientID=vrep.simxStart('127.0.0.1',20001,True,True,5000,5) # Connect to V-REP
if clientID!=-1:
	print ('Connected to remote API server')

	# Now try to retrieve data in a blocking fashion (i.e. a service call):
	res,objs=vrep.simxGetObjects(clientID,vrep.sim_handle_all,vrep.simx_opmode_blocking)
	if res==vrep.simx_return_ok:
		print ('Number of objects in the scene: ',len(objs))
	else:
		print ('Remote API function call returned with error code: ',res)

	time.sleep(2)
	
	LASTSENSOR = 0

	# Initializate
	r,LeftSensor_handle=vrep.simxGetObjectHandle(clientID,"LeftSensor#",vrep.simx_opmode_blocking)	
	r,MiddleSensor_handle=vrep.simxGetObjectHandle(clientID,"MiddleSensor#",vrep.simx_opmode_blocking)	
	r,RightSensor_handle=vrep.simxGetObjectHandle(clientID,"RightSensor#",vrep.simx_opmode_blocking)	
	r,LeftJoint_handle=vrep.simxGetObjectHandle(clientID,"DynamicLeftJoint#",vrep.simx_opmode_blocking)	
	r,RightJoint_handle=vrep.simxGetObjectHandle(clientID,"DynamicRightJoint#",vrep.simx_opmode_blocking)

	# Read all sensors and joints
	vrep.simxReadVisionSensor(clientID,LeftSensor_handle,vrep.simx_opmode_streaming)
	vrep.simxReadVisionSensor(clientID,MiddleSensor_handle,vrep.simx_opmode_streaming)
	vrep.simxReadVisionSensor(clientID,RightSensor_handle,vrep.simx_opmode_streaming)
	vrep.simxGetJointPosition(clientID,LeftJoint_handle,vrep.simx_opmode_streaming)
	vrep.simxGetJointPosition(clientID,RightJoint_handle,vrep.simx_opmode_streaming)
	

	
	# Now retrieve streaming data (i.e. in a non-blocking fashion):
	startTime=time.time()
	while True:
			
		# Sense
		r,left,auxPackets=vrep.simxReadVisionSensor(clientID,LeftSensor_handle,vrep.simx_opmode_buffer)
		r,mid,auxPackets=vrep.simxReadVisionSensor(clientID,MiddleSensor_handle,vrep.simx_opmode_buffer)
		r,right,auxPackets=vrep.simxReadVisionSensor(clientID,RightSensor_handle,vrep.simx_opmode_buffer)
		
		left = not left
		mid = not mid
		right = not right
		print ('LeftSensor: %s\tMiddleSensor: %s\tRightSensor: %s' % (left, mid, right))
		
		# Think
		if left:
			errorCode=vrep.simxSetJointTargetVelocity(clientID, LeftJoint_handle, -2, vrep.simx_opmode_streaming)
			errorCode=vrep.simxSetJointTargetVelocity(clientID, RightJoint_handle, 2, vrep.simx_opmode_streaming)
			LASTSENSOR = 0
			startTime=time.time()
			#while (left and mid and right):
                         #       pass
                        if(time.time() - startTime > 1):
                                break
		elif mid:
			errorCode=vrep.simxSetJointTargetVelocity(clientID, LeftJoint_handle, 5, vrep.simx_opmode_streaming)
			errorCode=vrep.simxSetJointTargetVelocity(clientID, RightJoint_handle, 5, vrep.simx_opmode_streaming)
			if right:
				LASTSENSOR = 2
		elif right:
			errorCode=vrep.simxSetJointTargetVelocity(clientID, LeftJoint_handle, 2, vrep.simx_opmode_streaming)
			errorCode=vrep.simxSetJointTargetVelocity(clientID, RightJoint_handle, -2, vrep.simx_opmode_streaming)
			LASTSENSOR = 2
		elif LASTSENSOR == 0:
			errorCode=vrep.simxSetJointTargetVelocity(clientID, LeftJoint_handle, -2, vrep.simx_opmode_streaming)
			errorCode=vrep.simxSetJointTargetVelocity(clientID, RightJoint_handle, 2, vrep.simx_opmode_streaming)
		elif LASTSENSOR == 2:
			errorCode=vrep.simxSetJointTargetVelocity(clientID, LeftJoint_handle, 2, vrep.simx_opmode_streaming)
			errorCode=vrep.simxSetJointTargetVelocity(clientID, RightJoint_handle, -2, vrep.simx_opmode_streaming)
			
		time.sleep(0.005)

        
	print ('FINISHED')
	# Now send some data to V-REP in a non-blocking fashion:
	vrep.simxAddStatusbarMessage(clientID,'Hello V-REP!',vrep.simx_opmode_oneshot)

	# Before closing the connection to V-REP, make sure that the last command sent out had time to arrive. You can guarantee this with (for example):
	vrep.simxGetPingTime(clientID)

	# Now close the connection to V-REP:
	vrep.simxFinish(clientID)
else:
	print ('Failed connecting to remote API server')
print ('Program ended')
