import time
import serial
import adafruit_rplidar

# Set up the RPLIDAR A1
uart = serial.Serial("/dev/ttyUSB0", baudrate=115200, timeout=1)
lidar = adafruit_rplidar.RPLidar(uart)

# Start scanning
for measurement in lidar.iter_measurments():
    # Extract the distance and angle from the measurement
    distance, angle = measurement[:2]
    print(f"Distance: {distance} cm, Angle: {angle} degrees")

    # Wait for a short time before taking the next measurement
    time.sleep(0.01)

# Stop the RPLIDAR A1
lidar.stop()
lidar.disconnect()

# File "/home/pi/Desktop/code/Project_LIDAR/lidar/adafruit_sample1.py", line 7, in <module>
#     lidar = adafruit_rplidar.RPLidar(uart)
# TypeError: __init__() missing 1 required positional argument: 'port'