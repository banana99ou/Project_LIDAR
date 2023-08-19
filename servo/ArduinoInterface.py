import serial
import time

dir = 0
res = 1

SerialArduino = serial.Serial('/dev/ttyACM0', 9600, timeout=5) # port is subject to change

InSTR = SerialArduino.readline()
print("Raw Serial input: " + InSTR.decode("UTF-8").strip())

while 1:
    # request to step x degree or step
    SerialArduino.write(b'step' + dir.to_bytes(2, "little") + res.to_bytes(2, "little"))
    print(b'step' + dir.to_bytes(2, "little") + res.to_bytes(2, "little"))

    InSTR = SerialArduino.readline()
    print("Raw Serial input: " + InSTR.decode("UTF-8").strip())

    # receicve acknowledge statement
    if InSTR.decode("utf-8").strip() is True:
        # if request acknloedged pass
        pass
    else: 
        # if request not acknowledged send request again
        pass
    # recive action complete statement