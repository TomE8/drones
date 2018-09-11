#!/usr/bin/env python3
import time
import os
import cv2

from General.state_machine import getMode
from General.general_common import Modes

from Control.joystick import Joystick
from Control.drone_communication import command_center

from Vision.camera import Camera

my_joystick=Joystick(0.1,0.1,0.2,0.1) # TODO: read these values from the config file
my_camera = Camera()
mode=Modes.IDLE

while mode != Modes.EXIT:
    my_joystick.refresh()

    mode=getMode(mode,my_joystick)
    command_center(mode, my_joystick)

    image = my_camera.get_image()
    if image is not None:
        cv2.imshow('Video', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(0.02)

    print("mode changed: {}".format(mode))
    os.system('cls' if os.name == 'nt' else 'clear')

    my_joystick.update_vales()

cv2.destroyAllWindows()
os.system('cls' if os.name == 'nt' else 'clear')
