from dronekit import connect, VehicleMode, LocationGlobalRelative, APIException
import time
import socket
#import exceptions
import math
import argparse

def connectMyCopter():
	parser=argparse.ArgumentParser(description = "commands")
	parser.add_argument("--connect")
	args = parser.parse_args()
	connection_string = args.connect
	baud_rate = 92100
	vehicle = connect('/dev/serial/by-id/usb-ArduPilot_Pixhawk1_3F002C000C51383333353437-if00',wait_ready=True,baud=baud_rate)
	return vehicle

def arm():
	#while vehicle.is_armable==False:
	#	print("waiting for vehicle to become armable...")
	#	time.sleep(1)
	print("yooooo vehicle is now armable")
	print("")

	vehicle.armed = True
	while vehicle.armed==False:
		print("waiting for drone to become armed")
		time.sleep(1)
		vehicle.armed=True

	print("vehicle is now armed")
	print("OMG prope are sppinning. LOCK OUT......")
	return None


vehicle = connectMyCopter()
arm()
print("end of script") 
