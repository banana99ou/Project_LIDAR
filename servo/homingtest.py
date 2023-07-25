import RPi.GPIO as GPIO
import time

stepPin = 26  # Y.STEP
dirPin = 19  # Y.DIR
enPin = 13
homingPin = 4  # placeholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholder
stepsPerRev = 200
pulseWidthMicros = 100  # microseconds 0.0001 second
millisBtwnSteps = 1000  # 0.001 second
angleNow = 0
stepdir = "cw"

def step(dir, angle):
    # handle stepper motor
    # takes in dirrection and angle in degrees and keep record of current angle
    if dir == "cw":
        GPIO.output(dirPin, GPIO.HIGH)
        anglestep = 1.8 
    if dir == "ccw":
        GPIO.output(dirPin, GPIO.LOW)
        anglestep = -1.8
    for i in range(angle/1.8):
        GPIO.output(stepPin, GPIO.HIGH)
        time.sleep(pulseWidthMicros / 1000000.0)
        GPIO.output(stepPin, GPIO.LOW)
        time.sleep(millisBtwnSteps / 100000.0)
        angleNow += anglestep
    
def StepmotorStep(resolution="fine"):
    # set resolution
    if resolution == "fine":
        resolution = 1  # step == 1.8 degree
    if resolution == "coarse":
        resolution = 3  # == 5.4 degree
    if stepdir == "cw" and angleNow <= 135:
        stepdir = "ccw"
    if stepdir == "ccw" and angleNow >= 225:
        stepdir = "cw"
    # need to add a feature that ties scanning range to certain range
    step(stepdir, resolution)
    return angleNow


def homing():
    while True:
        # if homing switch pressed
        if (GPIO.input(homingPin) == 1):
            angleNow = 45 # 25 step
            # turn 90 clockwise to initialize lidar pos
            # then break
            # find way to use arduino as driver instead
            step("cw", 90)
            break
        # if homing switch not pressed
        else:
            # keep turning ccw until switch pressed
            step("ccw", 1.8)

homing()
for i in range(10):
    StepmotorStep()
    print("stepping")
print("end")