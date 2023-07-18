import RPi.GPIO as GPIO
import time

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

print(pulseWidthMicros / 1000000.0)
print(millisBtwnSteps / 1000.0)

print("CNC Shield Initialized")

try:
    while True:
        print("Running clockwise")
        GPIO.output(dirPin, GPIO.HIGH)  # Enables the motor to move in a particular direction

        # Makes 200 pulses for making one full cycle rotation
        for i in range(stepsPerRev):
            GPIO.output(stepPin, GPIO.HIGH)
            time.sleep(pulseWidthMicros / 1000000.0)
            GPIO.output(stepPin, GPIO.LOW)
            time.sleep(millisBtwnSteps / 100000.0)
            print(i)

        time.sleep(1)  # One second delay

        print("Running counter-clockwise")
        GPIO.output(dirPin, GPIO.LOW)  # Changes the rotation's direction

        # Makes 400 pulses for making two full cycle rotation
        for i in range(2 * stepsPerRev):
            GPIO.output(stepPin, GPIO.HIGH)
            time.sleep(pulseWidthMicros / 1000000.0)
            GPIO.output(stepPin, GPIO.LOW)
            time.sleep(millisBtwnSteps / 100000.0)

        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
