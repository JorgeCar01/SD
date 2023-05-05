import time

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.position_hl_commander import PositionHlCommander
from cflib.utils import uri_helper

URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')
HOVER_HEIGHT = 1.0
HOVER_DURATION = 8

def hover_and_land(cf):
    with PositionHlCommander(
            cf,
            x=0.0, y=0.0, z=0.0,
            default_velocity=0.2,
            default_height=HOVER_HEIGHT,
            controller=PositionHlCommander.CONTROLLER_PID) as pc:

        print("Taking off...")
        pc.go_to(0, 0, HOVER_HEIGHT, 0.2)
        time.sleep(1)

        print(f"Hovering at {HOVER_HEIGHT} meters for {HOVER_DURATION} seconds...")
        time.sleep(HOVER_DURATION)

        print("Landing...")
        pc.land(0.2)
        time.sleep(1)

def main():
    cflib.crtp.init_drivers()

    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
        hover_and_land(scf.cf)

if __name__ == '__main__':
    main()
