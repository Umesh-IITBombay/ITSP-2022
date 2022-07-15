from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time

import argparse  
parser = argparse.ArgumentParser()
parser.add_argument('--connect', default='127.0.0.1:14550')
args = parser.parse_args()

# Connect to the Vehicle
print('Connecting to vehicle on: %s')
vehicle = connect('/dev/serial/by-id/usb-ArduPilot_Pixhawk1_3F002C000C51383333353437-if00', baud=57600, wait_ready=True)

# Function to arm and then takeoff to a user specified altitude
def arm_and_takeoff(aTargetAltitude):

  print("Basic pre-arm checks")
  # Don't let the user try to arm until autopilot is ready
  #while not vehicle.is_armable:
  #  print(" Waiting for vehicle to initialise...")
  #  time.sleep(1)
        
  print("Arming motors")
  # Copter should arm in GUIDED mode
  vehicle.mode    = VehicleMode("GUIDED")
  vehicle.armed   = True

  while not vehicle.armed:
    print(" Waiting for arming...")
    time.sleep(1)

  print("Taking off!")
  vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude
  time.sleep(20)
  # Check that vehicle has reached takeoff altitude
  #while True:
  #  print(" Altitude: ") vehicle.location.global_relative_frame.alt 
    #Break and return from function just below target altitude.        
  #  if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95: 
  #    print "Reached target altitude"
  #    break
  #  time.sleep(1)

# Initialize the takeoff sequence to 20m
arm_and_takeoff(20)

print("Take off complete")

# Hover for 10 seconds
time.sleep(30)

print("Now let's land")
vehicle.mode = VehicleMode("LAND")

# Close vehicle object
vehicle.close()
