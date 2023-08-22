import serial
import time

# all angle in terms of step
# 200 step = 360
# 100 step = 180
# 50 step = 90
# 25 step = 45
# 5 step = 9
angleNow = 0

SerialArduino = serial.Serial('/dev/ttyACM0', 9600, timeout=5)

class StepperError(Exception):
    '''error'''

def step(direction, amount):
    temp1, temp2 = direction, amount
    SerialArduino.write(b'step ' + direction + amount + b'\n')
    response = SerialArduino.read()
    if response == "Ack Step":
        pass
    else:
        step(temp1, temp2)

    
def StepLoop(resolution="fine"): # , ifinit):
    # ties scanning range to certain range
    # emergencystop
    # stop and go back few step
    IsScanEdge = "Nan" 
    # set resolution
    global stepdir
    if resolution == "fine":
        resolution = 1  # == 1,8 degree
    if resolution == "coarse":
        resolution = 5  # == 9 degree
    if stepdir == "cw" and angleNow >= 125: #225 d
        # if lidar scan range right edge (from lidar's perspective)
        print("CW bound")
        stepdir = "ccw"
        IsScanEdge = 1 # "Right"
    elif stepdir == "ccw" and angleNow <= 75: # 135 d
        # if lidar scan range left edge
        print("CCW bound")
        stepdir = "cw"
        IsScanEdge = -1 # "left"
    else:
        IsScanEdge = 0 # "Nan"
    # print("stepdir: ", stepdir)

    if stepdir == "cw":
        stepdir = 1
    elif stepdir == "ccw":
        stepdir = 0

    step(stepdir, resolution)
    return IsScanEdge


def Homing():
    SerialArduino.write(b'Homing')
    response = SerialArduino.read()
    if response == "Ack Homing":
        pass
    else:
        Homing()


def read_serial():
    global angleNow
    while True:
        if SerialArduino.in_waiting > 0:
            message = SerialArduino.readline().decode()
            if message.startswith("AngleNow: "):
                angleNow = int(message.split(":")[1])
            elif message == "LimitSwitchPressed":
                return message


if __name__ == "__main__":
    Homing()
    for i in range(200):
        StepLoop()
        print("stepping")
    print("end")