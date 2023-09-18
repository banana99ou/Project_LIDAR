# import os
# from math import cos, sin, pi, floor
import math
from adafruit_rplidar import RPLidar,RPLidarException
# import RPi.GPIO as GPIO
# import pygame
import time
import StepModule as StepModule
import random
# import threading

stepPin = 26  # Y.STEP
dirPin = 19  # Y.DIR
enPin = 13
homingPin = 4  # placeholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholder
stepsPerRev = 200
pulseWidthMicros = 100  # microseconds 0.0001 second
millisBtwnSteps = 1000  # 0.001 second
angleNow = 125
prev_angle = 0
stepdir = "cw"

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(enPin, GPIO.OUT)
# GPIO.output(enPin, GPIO.LOW)
# GPIO.setup(stepPin, GPIO.OUT)
# GPIO.setup(dirPin, GPIO.OUT)

# W = 600
# H = 600

SCAN_BYTE = b'\x20'
SCAN_TYPE = 129

# Setup pygame
# pygame.display.init()
# lcd = pygame.display.set_mode((H, H))
# pygame.mouse.set_visible(False)
# lcd.fill((200, 0, 0))
# pygame.display.update()

# Setup the RPLidar
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(None, PORT_NAME, timeout=3)

# used to scale data to fit on the screen
max_distance = 0


def process_data(data):
    '''process data'''
    # global max_distance
    # lcd.fill((0, 0, 0))
    # point = (int(W / 2), int(H / 2))

    # pygame.draw.circle(lcd, pygame.Color(255, 255, 255), point, 10)
    # pygame.draw.circle(lcd, pygame.Color(100, 100, 100), point, 100, 1)
    # pygame.draw.line(lcd, pygame.Color(100, 100, 100), (0, int(H/2)), (W, int(H/2)))
    # pygame.draw.line(lcd, pygame.Color(100, 100, 100), (int(W/2), 0), (int(W/2), H))

    # for angle in range(360):
    #     distance = data[angle]
    #     if distance > 0:                  # ignore initially ungathered data points
    #         # scale maxdistance value to biggest value among current datamax([min([5000, distance]), max_distance]) check unit of distance val
    #         max_distance = 100
    #         radians = angle * pi / 180.0
    #         x = distance * cos(radians)
    #         y = distance * sin(radians)
    #         point = (int(W / 2) + int(x / max_distance * (W/2)),
    #                  int(H/2) + int(y / max_distance * (H/2)))
    #         pygame.draw.circle(lcd, pygame.Color(255, 0, 0), point, 2)
    # pygame.display.update()
    print(data)

# def read_serial_from_module():
#     message = StepModule.read_serial()
#     print("Received from module:", message)
#     if message == "LimitSwitchPressed":
#         raise StepModule.StepperError("Limit switch pressed on Arduino")
#
# serial_thread = threading.Thread(target=read_serial_from_module)
# serial_thread.start()

StepModule.init_serial()
StepModule.homing()

scan_data = [0] * 360
Single_Scan = [0] * 360

while True:
    try:
        for scan in lidar.iter_scans():
            for (_, angle, distance) in scan:
                Single_Scan[min([359, math.floor(angle)])] = distance
            angleNow, prev_angle = StepModule.step_loop(resolution="fine", angleNow=angleNow, prev_angle=prev_angle)
            scan_data.insert(angleNow, Single_Scan)
        process_data(scan_data)

    except RPLidarException as e:
        print(f"RPLidar Exception: {e}")
        lidar.stop_motor()
        lidar.disconnect()
        time.sleep(0.07)  # Add a small delay before reconnecting to the sensor
        lidar.connect()
        lidar.start_motor()

    except StepModule.StepperError as e:
        print(f"Stepper Error: {e}")
        StepModule.step(1, 20)
        print("recallibrating")
        StepModule.homing()

    except KeyboardInterrupt:
        print('Stopping.')
        break

lidar.stop()
lidar.stop_motor()
lidar.disconnect()


# def step(dir, angle):
#     # handle stepper motor
#     # takes in dirrection and angle in degrees and keep record of current angle
#     if dir == "cw":
#         GPIO.output(dirPin, GPIO.HIGH)
#         anglestep = 1.8 
#     if dir == "ccw":
#         GPIO.output(dirPin, GPIO.LOW)
#         anglestep = -1.8
#     for i in range(angle/1.8):
#         GPIO.output(stepPin, GPIO.HIGH)
#         time.sleep(pulseWidthMicros / 1000000.0)
#         GPIO.output(stepPin, GPIO.LOW)
#         time.sleep(millisBtwnSteps / 100000.0)
#         angleNow += anglestep
    
# def StepmotorStep(resolution="fine"):
#     # set resolution
#     if resolution == "fine":
#         resolution = 1  # step == 1.8 degree
#     if resolution == "coarse":
#         resolution = 3  # == 5.4 degree
#     if stepdir == "cw" and angleNow <= 135:
#         stepdir = "ccw"
#     if stepdir == "ccw" and angleNow >= 225:
#         stepdir = "cw"
#     # need to add a feature that ties scanning range to certain range
#     step(stepdir, resolution)
#     return angleNow


# def homing()
#:
#     while True:
#         # if homing switch pressed
#         if (GPIO.input(homingPin) == 1):
#             angleNow = 45 # 25 step
#             # turn 90 clockwise to initialize lidar pos
#             # then break
#             # find way to use arduino as driver instead
#             step("cw", 90)
#             break
#         # if homing switch not pressed
#         else:
#             # keep turning ccw until switch pressed
#             step("ccw", 1.8)
