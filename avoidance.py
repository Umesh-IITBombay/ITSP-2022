from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil

import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 21
GPIO_ECHO = 20
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance


print('Connecting to vehicle on: /dev/serial/by-id/usb-ArduPilot_Pixhawk1_3F002C000C51383333353437-if00')
vehicle = connect('/dev/serial/by-id/usb-ArduPilot_Pixhawk1_3F002C000C51383333353437-if00', baud=57600, wait_ready=True)

# Function to arm and then takeoff to a user specified altitude
def arm_and_takeoff(aTargetAltitude):

  print("Basic pre-arm checks")
  # Don't let the user try to arm until autopilot is ready
  #while not vehicle.is_armable:
  #  print " Waiting for vehicle to initialise..."
  #  time.sleep(1)
        
  print("Arming motors")
  # Copter should arm in GUIDED mode
  vehicle.mode    = VehicleMode("STABILIZE")
  vehicle.armed   = True

  #while not vehicle.armed:
  #  print(" Waiting for arming...")
  #  time.sleep(1)
  #  vehicle.armed=True

  print("Taking off!")
  vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

  # Check that vehicle has reached takeoff altitude
  #while True:
  #  print " Altitude: ", vehicle.location.global_relative_frame.alt 
    #Break and return from function just below target altitude.        
  #  if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95: 
  #    print "Reached target altitude"
  #    break
  #  time.sleep(1)

 
if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            print(dist)
            if(dist<20):
              vehicle.close()
              print("can't take_off")
            if(dist>20):
              arm_and_takeoff(20)
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()

