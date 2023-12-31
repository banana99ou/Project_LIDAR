import RPi.GPIO as GPIO
import time

# all angle in terms of step
# 200 step = 360
# 100 step = 180
# 50 step = 90
# 25 step = 45
# 5 step = 9

class StepperError(Exception):
    '''error'''

stepPin = 26  # Y.STEP
dirPin = 19  # Y.DIR
enPin = 13
HomingPin = 20
HomingCommon = 21
stepsPerRev = 200
pulseWidthMicros = 100  # microseconds 0.0001 second
millisBtwnSteps = 1000  # 0.001 second
angleNow = 0
stepdir = "cw"
StepToAngle = 360/200

GPIO.setmode(GPIO.BCM)
GPIO.setup(enPin, GPIO.OUT)
GPIO.output(enPin, GPIO.LOW)
GPIO.setup(stepPin, GPIO.OUT)
GPIO.setup(dirPin, GPIO.OUT)
GPIO.setup(HomingPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(HomingCommon, GPIO.OUT)
GPIO.output(HomingCommon, GPIO.HIGH)

def step(dir, angle):
    # handle stepper motor
    # takes in dirrection and angle in degrees and keep record of current angle
    if dir == "cw":
        global angleNow
        GPIO.output(dirPin, GPIO.HIGH)
        anglestep = 1 
    if dir == "ccw":
        GPIO.output(dirPin, GPIO.LOW)
        anglestep = -1
    for i in range(int(angle)):
        GPIO.output(stepPin, GPIO.HIGH)
        time.sleep(pulseWidthMicros / 1000000.0)
        GPIO.output(stepPin, GPIO.LOW)
        time.sleep(millisBtwnSteps / 100000.0)
        angleNow += anglestep
        # print(angleNow * StepToAngle)
        # time.sleep(0.1)
    
def StepmotorStep(resolution="fine"): # , ifinit):
    # emergencystop
    # stop and go back few step
    IsScanEdge = "Nan" 
    if GPIO.input(HomingPin):
        raise StepperError('Angle Error')
    # set resolution
    global stepdir
    if resolution == "fine":
        resolution = 1  # == 1,8 degree
    if resolution == "coarse":
        resolution = 5  # == 9 degree
    if stepdir == "cw" and angleNow >= -25: #225 d
        # if lidar scan range right edge (from lidar's perspective)
        print("CW bound")
        stepdir = "ccw"
        IsScanEdge = 1 # "Right"
    elif stepdir == "ccw" and angleNow <= 25: # 135 d
        # if lidar scan range left edge
        print("CCW bound")
        stepdir = "cw"
        IsScanEdge = -1 # "left"
    else:
        IsScanEdge = 0 # "Nan"
    # need to add a feature that ties scanning range to certain range
    # print("stepdir: ", stepdir)
    step(stepdir, resolution)
    return IsScanEdge

def homing():
    while True:
        # if homing switch pressed
        if GPIO.input(HomingPin):
            global angleNow 
            angleNow = 75 # 45 degree
            print("reset")
            # print(angleNow * StepToAngle)
            time.sleep(0.5)
            # turn 180 clockwise to initialize lidar pos
            # then break
            # find way to use arduino as driver instead
            step("cw", 50)
            time.sleep(1)
            break
        # if homing switch not pressed
        else:
            # keep turning ccw until switch pressed
            step("ccw", 1)

if __name__ == "__main__":
    homing()
    for i in range(200):
        StepmotorStep()
        print("stepping")
    print("end")