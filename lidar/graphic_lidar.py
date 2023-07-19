#import os
import pygame
from math import cos, sin, pi, floor
from adafruit_rplidar import RPLidar
import RPi.GPIO as GPIO
import time

stepYPin = 26  # Y.STEP
dirYPin = 19  # Y.DIR
enPin = 13
stepPin = stepYPin
dirPin = dirYPin
homingPin = 4 # placeholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholder
stepsPerRev = 200
pulseWidthMicros = 100  # microseconds 0.0001 second
millisBtwnSteps = 1000  # 0.001 second

GPIO.setmode(GPIO.BCM)
GPIO.setup(enPin, GPIO.OUT)
GPIO.output(enPin, GPIO.LOW)
GPIO.setup(stepPin, GPIO.OUT)
GPIO.setup(dirPin, GPIO.OUT)

W = 600
H = 600

SCAN_BYTE = b'\x20'
SCAN_TYPE = 129

def StepmotorStep(resolution="fine"):
    # set resolution
    if(resolution == "fine"):
      resolution = 1 # step == 1.8 degree
    if(resolution == "coarse"):
       resolution = 3 # == 5.4 degree
    # need to add a feature that ties scanning range to certain range
    GPIO.output(dirPin, GPIO.LOW)
    for i in range(resolution):
      GPIO.output(stepPin, GPIO.HIGH)
      time.sleep(pulseWidthMicros / 1000000.0)
      GPIO.output(stepPin, GPIO.LOW)
      time.sleep(millisBtwnSteps / 100000.0)
def homing():
  while True:
    # if homing switch pressed
    if(GPIO.input(homingPin) == 1):
      # turn 90 clockwise to initialize lidar pos
      # then break
      # find way to use arduino as driver instead
      GPIO.output(dirPin, GPIO.HIGH)
      for i in range(90/1.8):
        GPIO.output(stepPin, GPIO.HIGH)
        time.sleep(pulseWidthMicros / 1000000.0)
        GPIO.output(stepPin, GPIO.LOW)
       / 100000.0)
      break
    # if homing switch not pressed
    else:
      # keep turning ccw until switch pressed
      GPIO.output(dirPin, GPIO.LOW)
      GPIO.output(stepPin, GPIO.HIGH)
      time.sleep(pulseWidthMicros / 1000000.0)
      GPIO.output(stepPin, GPIO.LOW)
      time.sleep(millisBtwnSteps / 100000.0)

# Setup pygame
pygame.display.init()
lcd = pygame.display.set_mode((H,H))
pygame.mouse.set_visible(False)
lcd.fill((200,0,0))
pygame.display.update()


# Setup the RPLidar
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(None, PORT_NAME, timeout=3)

# used to scale data to fit on the screen
max_distance = 0


def process_data(data):
    global max_distance
    lcd.fill((0,0,0))
    point = ( int(W / 2) , int(H / 2) )
    
    pygame.draw.circle(lcd,pygame.Color(255, 255, 255),point,10 )
    pygame.draw.circle(lcd,pygame.Color(100, 100, 100),point,100 , 1 )
    pygame.draw.line( lcd,pygame.Color(100, 100, 100) , ( 0, int(H/2)),( W , int(H/2) ) )
    pygame.draw.line( lcd,pygame.Color(100, 100, 100) , ( int(W/2),0),( int(W/2) , H ) )

    for angle in range(360):
        distance = data[angle]
        if distance > 0:                  # ignore initially ungathered data points
            max_distance = 100 # scale maxdistance value to biggest value among current datamax([min([5000, distance]), max_distance]) check unit of distance val
            radians = angle * pi / 180.0
            x = distance * cos(radians)
            y = distance * sin(radians)
            point = ( int(W / 2) + int(x / max_distance * (W/2)), int(H/2) + int(y / max_distance * (H/2) ))
            pygame.draw.circle(lcd,pygame.Color(255, 0, 0),point,2 )
    pygame.display.update()

scan_data = [0] * 360

try:
    for scan in lidar.iter_scans():
        for (_, angle, distance) in scan:
            scan_data[min([359, floor(angle)])] = distance
            StepmotorStep("coarse")
        process_data(scan_data)

except KeyboardInterrupt:
    print('Stopping.')
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()


      
# issues:
# .stop() sends stop byte to lidar so chekc what stop byte should be in doc
# and discriptor length
# intergrate stepper motor
# edit cad to have homing switch
# lidar resolution seems to be bit low check it and find way to increase resolution.
# it could be done by limiting max distance value from lidar
# check if mountplate is blocking los to lower angle of lidar 
# move this line to github issue page or readme.md file

# milestone
# get lidar working (done)
# get mount printed (done)
# get stepper motor working
# ㄴneed to fix vibration issue
# ㄴneed to find a way to removed sleep function
#  ㄴuse arduino as driver
#  ㄴsepeate program(big issue) or routine
#  ㄴsome other way
# get stepper and lidar working together
# data processing

# idea:
# find milestone management program/website
