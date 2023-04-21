import math
import time
from threading import Thread

import matplotlib.pyplot as plt


from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.position_hl_commander import PositionHlCommander

# Import the functions from the model
#from *** import get_image, detect_people

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


# Function to display images only when a person is detected, with detection
def display_camera_images():
    while True:
        img = get_image()
        people = detect_people(img)

        if len(people) > 0:
            # Draw bounding boxes around detected people
            for detection in people:
                x, y, w, h = detection
                plt.gca().add_patch(plt.Rectangle((x, y), w, h, linewidth=2, edgecolor='g', facecolor='none'))

            # Display the image
            plt.imshow(img)
            plt.axis('off')
            plt.title('Camera View')
            plt.show(block=False)
            print("Press 'q' to continue.")
            plt.pause(0.1)

            # Close the image window and clear the plot
            plt.close()
            plt.clf()

        # Press 'q' to exit the display loop
        key = plt.waitforbuttonpress()
        if key == ord('q'):
            plt.close('all')
            break


if __name__ == '__main__':
    main()
