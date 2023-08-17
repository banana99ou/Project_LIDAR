import serial
import time

dir = 0
res = 0

SerialArduino = serial.Serial('/dev/ttyUSB1', 9600, timeout=5) # port is subject to change

InSTR = SerialArduino.readline()
print("Raw Serial input: " + InSTR.decode("UTF-8").strip())


while 1:
    # request to step x degree or step
    SerialArduino.write(b'step' + str(dir) + str(res))

    InSTR = SerialArduino.readline()

    # receicve acknowledge statement
    if InSTR.decode("utf-8").strip() is True:
        # if request acknloedged pass
        pass
    else:
        # if request not acknowledged send request again

    # recive action complete statement