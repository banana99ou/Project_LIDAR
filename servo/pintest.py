import RPi.GPIO as GPIO
import time

servoPIN = 17
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

try:
  while True:
    GPIO.output(17, GPIO.HIGH)
except KeyboardInterrupt:
  GPIO.cleanup()
