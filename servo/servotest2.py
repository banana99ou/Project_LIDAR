import RPi.GPIO as GPIO
import time
import sys

input = float(sys.argv[1])

stepYPin = 26  # Y.STEP
dirYPin = 19  # Y.DIR
enPin = 13
stepPin = stepYPin
dirPin = dirYPin
stepsPerRev = 200
pulseWidthMicros = 100  # microseconds 0.0001 second
millisBtwnSteps = 1000  # 0.001 second

GPIO.setmode(GPIO.BCM)
GPIO.setup(enPin, GPIO.OUT)
GPIO.output(enPin, GPIO.LOW)
GPIO.setup(stepPin, GPIO.OUT)
GPIO.setup(dirPin, GPIO.OUT)

print(input)
print(round(input/1.8))

try:
    while True:
        for i in range(round(input/1.8)):
          GPIO.output(dirPin, GPIO.HIGH)  # Enables the motor to move in a particular direction
          
          GPIO.output(stepPin, GPIO.HIGH)
          time.sleep(pulseWidthMicros / 1000000.0)
          GPIO.output(stepPin, GPIO.LOW)
          time.sleep(millisBtwnSteps / 100000.0)
          
          time.sleep(0.001)
          print(i)
        print("break")
        break

except KeyboardInterrupt:
    GPIO.cleanup()
