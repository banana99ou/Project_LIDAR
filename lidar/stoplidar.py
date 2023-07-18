import time
from adafruit_rplidar import RPLidar
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(None, PORT_NAME, timeout=3)
for i in range(1000):
    # lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()
    time.sleep(1)
    print("ran")