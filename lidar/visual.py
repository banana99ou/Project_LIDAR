import pygame

W = 640
H = 480

# Set up pygame
pygame.display.init()
lcd = pygame.display.set_mode((H, H))
pygame.mouse.set_visible(False)
lcd.fill((200, 0, 0))
pygame.display.update()

# Set up the lidar data file
filename = "lidar_data.txt"
file = open(filename, "r")

# Used to scale data to fit on the screen
max_distance = 0

for line in file:
    data = line.strip().split(" ")
    angle = int(data[0])
    distance = int(data[1])
    if distance > 0:  # Ignore initially ungathered data points
        max_distance = max([min([5000, distance]), max_distance])
        radians = angle * pi / 180.0
        x = distance * cos(radians)
        y = distance * sin(radians)
        point = (int(W / 2) + int(x / max_distance * (W / 2)), int(H / 2) + int(y / max_distance * (H / 2)))
        pygame.draw.circle(lcd, pygame.Color(255, 0, 0), point, 2)

pygame.display.update()

# Clean up
file.close()

