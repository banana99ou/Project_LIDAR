import serial
import time

# all angle in terms of step
# 200 step = 360
# 100 step = 180
# 50 step = 90
# 25 step = 45
# 5 step = 9

prev_angle = 0
angleNow = 0
stringComplete = False
stepdir = 0

def init_serial():
    '''start serial com'''
    global SerialArduino
    SerialArduino = serial.Serial('/dev/ttyACM0', 9600, timeout=2)

class StepperError(Exception):
    '''error'''

def step(amount: int, direction: int=1):
    '''run motor dir 1=cw 0=ccw amount (in step)'''
    temp1 = amount
    temp2 = direction
    SerialArduino.write(b'Step ' + str(amount).encode() +b'\n')#+ str(direction).encode() + b'\n')
    print(b'Step ' + str(amount).encode() + b'\n')
    
    response = ''
    for i in range(3):
        response += SerialArduino.readline().decode('utf-8')
    print('response: ' + str(response))
    if "Ack: Step" in response:
        print("Ack Received")
        return
    else:
        print("Ack not Received")
        step(temp1, temp2)
    
def step_loop(resolution="fine"): # , ifinit):
    '''ties scanning range to certain range 
        emergencystop 
        stop and go back few step'''
    
    if resolution == "fine":
        resolution = 1  # == 1,8 degree
    if resolution == "coarse":
        resolution = 5  # == 9 degree
    global prev_angle
    global angleNow
    if(((angleNow - prev_angle) > 0) and (angleNow <= 125)):
        step(angleNow + resolution)
    if(angleNow >= 125):
        step(angleNow - resolution)
    if(((angleNow + prev_angle) > 0) and (angleNow >= 75)):
        step(angleNow - resolution)
    if(angleNow <= 75):
        step(angleNow + resolution)
    prev_angle = angleNow
    response = ''
    for i in range(3):
        response += SerialArduino.readline().decode('utf-8')
    print('response: ' + str(response))
    prefix = "AngleNow: "
    if prefix in response:
        lines = response.split('\n')
        for line in lines:
            if "AngleNow: " in line:
                angleNow = int(line[len("AngleNow: "):])
                print("angleNow saved" + str(angleNow))
    return angleNow

    # IsScanEdge = "Nan" 
    # # set resolution
    # global stepdir
    # global angleNow
    
    # if stepdir == "cw" and angleNow >= 125: #225 d
    #     # if lidar scan range right edge (from lidar's perspective)
    #     print("CW bound")
    #     stepdir = "ccw"
    #     IsScanEdge = 1 # "Right"
    # elif stepdir == "ccw" and angleNow <= 75: # 135 d
    #     # if lidar scan range left edge
    #     print("CCW bound")
    #     stepdir = "cw"
    #     IsScanEdge = -1 # "left"
    # else:
    #     IsScanEdge = 0 # "Nan"
    # # print("stepdir: ", stepdir)

    # if stepdir == "cw":
    #     stepdir = 1
    # elif stepdir == "ccw":
    #     stepdir = 0

    # step(resolution)
  
def homing():
    '''Homes stepper motor'''
    SerialArduino.write(b'Homing' + b'\n')
    print(b'Homing')
    response = ''
    for i in range(3):
        response += SerialArduino.readline().decode('utf-8')
    print('response: ' + str(response))
    # read Ack statement from arduino and try again if ack not recieved
    if "Ack: Homing" in response:
        print("Ack Recieved")
        # wait until homing complete messege
        while True:
            response = SerialArduino.readline().decode('utf-8')
            print('response: ' + str(response))
            if "HomgComp" in response:
                print("homing comp")
                break
    else:
        print("Ack not Recieved")
        homing()


def serial_event():
    '''deprected'''
    global stringComplete
    response = " "
    while SerialArduino.available():
        in_char = chr(SerialArduino.read())
        response += in_char
        if in_char == '\n':
            stringComplete = True
            break
    return response


def read_serial():
    '''read serial from arduino'''
    global angleNow
    while True:
        if SerialArduino.in_waiting > 0:
            message = SerialArduino.readline().decode()
            if message.startswith("AngleNow: "):
                angleNow = int(message.split(":")[1])
            elif "LimitSwitchPressed" in message:
                return message


if __name__ == "__main__":
    homing()
    for i in range(200):
        step_loop()
        print("stepping")
    print("end")