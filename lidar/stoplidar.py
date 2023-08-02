import time
from adafruit_rplidar import RPLidar
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(None, PORT_NAME, timeout=3)
try:
    for i in range(10):
        lidar.stop_motor()
        time.sleep(5)
        print("ran")
finally:
    lidar.stop_motor()
    lidar.disconnect()