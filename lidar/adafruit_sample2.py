from math import floor
from adafruit_rplidar import RPLidar, RPLidarException
import time
import random

PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(None, PORT_NAME, timeout=3)

max_distance = 0

def process_data(data):
    print(data)

scan_data = [0]*360

while True:
    try:
        for scan in lidar.iter_scans():
            for (_, angle, distance) in scan:
                scan_data[min([359, floor(angle)])] = distance
            process_data(scan_data)


    except RPLidarException as e:
        print(f"RPLidar Exception: {e}")
        lidar.stop_motor()
        lidar.disconnect()
        time.sleep(random.randrange(0,1)/100)
        lidar.connect()
        lidar.start_motor()

    except KeyboardInterrupt:
        print('Stopping.')
        break
lidar.stop()
lidar.stop_motor()
lidar.disconnect()

#currentl data format [dis,dis,dis,dis,dis] order each dis value defines angle value ex) 0 , 1 , 2, 
#but there should be 360 dis value in each line but at least 1000 dis value is found
#consult refer to get angle from lidar or try iter_measurements method instead

