import RPi.GPIO as GPIO

somePin1 = 26
somePin2 = 19
angle = "fine"

GPIO.setmode(GPIO.BCM)
GPIO.setup(somePin1, GPIO.OUT)
GPIO.setup(somePin2, GPIO.OUT)

if angle == "fine":
    GPIO.output(somePin1, GPIO.HIGH)
if angle == "coarse":
    GPIO.output(somePin2, GPIO.HIGH)