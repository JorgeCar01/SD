import time
#test
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.position_hl_commander import PositionHlCommander
from cflib.positioning.motion_commander import MotionCommander
from cflib.utils import uri_helper

URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')
DEFAULT_HEIGHT = 0.5
BOX_LIMIT = 0.5
def spiral_path(cf):
    with PositionHlCommander(
            cf,
            x=0.0, y=0.0, z=0.0,
            default_velocity=0.2,
            default_height=1.0,
            controller=PositionHlCommander.CONTROLLER_PID) as pc:

        base_height = 100
        # radius = 0.5
        velocity = 0.2
        # num_points = 50
        # z_step = 0.1

        for i in range(base_height):
            # angle = 2 * math.pi * i / num_points
            # x = radius * math.cos(angle)
            # y = radius * math.sin(angle)
            z = base_height / 100  
            pc.go_to(0, 0, 0, velocity)

            time.sleep(0.1)

        for i in range(base_height, 0, -1):
            # angle = 2 * math.pi * i / num_points
            # x = radius * math.cos(angle)
            # y = radius * math.sin(angle)
            z = base_height / 100  
            pc.go_to(0, 0, 0, velocity)

            time.sleep(0.1)

def simple_connect():

    print("Yeah, I'm connected! :D")
    time.sleep(3)
    print("Now I will disconnect :'(")

def take_off_simple(scf):
    with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
        time.sleep(8)
        mc.stop()


def main():
    cflib.crtp.init_drivers()

    # camera_thread = Thread(target=display_camera_images)
    # camera_thread.start()

    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
        take_off_simple(scf)
        # simple_connect()

    # camera_thread.join()



if __name__ == '__main__':
    main()