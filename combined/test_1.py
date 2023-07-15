import os
import pygame
from math import cos, sin, pi, floor
from adafruit_rplidar import RPLidar
import RPi.GPIO as GPIO
from time import sleep


# Setup pygame
pygame.display.init()
lcd = pygame.display.set_mode((480, 640))
pygame.mouse.set_visible(False)
lcd.fill((200, 0, 0))
pygame.display.update()

# Setup the RPLidar
PORT_NAME = "/dev/ttyUSB0"
lidar = RPLidar(None, PORT_NAME, timeout=3)

# Initialize the servo motor
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
pwm = GPIO.PWM(11, 50)
pwm.start(0)
servo_angle = 0

# Used to scale data to fit on the screen
max_distance = 0


def process_data(data):
    global max_distance, servo_angle
    lcd.fill((0, 0, 0))
    x_center, y_center, z_center = 240, 320, 0

    # Draw the lidar scanning plane
    pygame.draw.circle(lcd, pygame.Color(255, 255, 255), (x_center, y_center), 10)
    pygame.draw.circle(lcd, pygame.Color(100, 100, 100), (x_center, y_center), 100, 1)
    pygame.draw.line(lcd, pygame.Color(100, 100, 100), (0, y_center), (480, y_center))
    pygame.draw.line(lcd, pygame.Color(100, 100, 100), (x_center, 0), (x_center, 640))

    # Draw the lidar data in 3D
    for angle in range(360):
        distance = data[angle]
        if distance > 0:
            max_distance = max([min([5000, distance]), max_distance])
            radians = angle * pi / 180.0
            x = distance * cos(radians)
            y = distance * sin(radians)
            z = servo_angle  # Use the servo angle as the z-coordinate
            point = (int(x_center + x / max_distance * 100), int(y_center + y / max_distance * 100), int(z_center + z))
            pygame.draw.circle(lcd, pygame.Color(255, 0, 0), point, 2)

    pygame.display.update()


scan_data = [0] * 360

try:
    for scan in lidar.iter_scans():
        # Process the lidar data for the current scanning plane
        for (_, angle, distance) in scan:
            scan_data[min([359, floor(angle)])] = distance
        process_data(scan_data)

        # Rotate the servo motor by 90 degrees after the first plane is scanned
        if servo_angle == 0:
            SetAngle(90)
        elif servo_angle == 90:
            SetAngle(180)
        elif servo_angle == 180:
            SetAngle(270)
        else:
            SetAngle(0)

        # Reset the lidar data for the next scanning plane
except:
    print("error")