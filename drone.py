import math
import time
from threading import Thread

import numpy as np
import cv2

from crazyflie import Crazyflie
from cflib.crazyflie import PositionHlCommander
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.position_hl_commander import PositionHlCommander

# Import your custom functions from the other file
from your_image_processing_file import get_image, detect_people

# Change this URI to your Crazyflie's radio address
URI = 'radio://0/80/2M/E7E7E7E7E7'

# Function for the spiral path
def spiral_path(cf):
    with PositionHlCommander(
            cf,
            x=0.0, y=0.0, z=0.0,
            default_velocity=0.2,
            default_height=1.0,
            controller=PositionHlCommander.CONTROLLER_PID) as pc:

        base_height = 1.0
        radius = 0.5
        velocity = 0.2
        num_points = 50
        z_step = 0.1

        for i in range(num_points):
            angle = 2 * math.pi * i / num_points
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            z = base_height + z_step * i
            pc.go_to(x, y, z, velocity)

            time.sleep(0.1)

# Main function
def main():
    cf = Crazyflie(rw_cache='./cache')

    camera_thread = Thread(target=display_camera_images)
    camera_thread.start()

    with SyncCrazyflie(URI, cf=cf) as scf:
        spiral_path(scf)

    camera_thread.join()

# Function to display images with detected people
def display_camera_images():
    while True:
        img = get_image()
        people = detect_people(img)
        
        # Draw bounding boxes around detected people
        for detection in people:
            x, y, w, h = detection
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow('Camera View', img)
        key = cv2.waitKey(1) & 0xFF

        # Press 'q' to exit the display loop
        if key == ord('q'):
            cv2.destroyAllWindows()
            break

if __name__ == '__main__':
    main()
