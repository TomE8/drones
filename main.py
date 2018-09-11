#!/usr/bin/env python3
import time
import os
import cv2

from General.state_machine import getMode
from General.general_common import States
from General.gui import Screen

from Control.joystick import Joystick
from Control.drone_communication import CommandCenter

from Vision.camera import Camera

my_joystick=Joystick(0.1,0.1,0.2,0.1) # TODO: read these values from the config file
my_camera = Camera()
my_command_center = CommandCenter()
my_screen = Screen()
mode=States.IDLE

while mode != States.EXIT:
    my_joystick.refresh()

    mode=getMode(mode,my_joystick)
    my_command_center.send_command(mode, my_joystick)

    image = my_camera.get_image()
    if image is not None:
        cv2.imshow('Video', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(0.02)

    my_screen.update_mode(mode)
    my_joystick.update_vales()

cv2.destroyAllWindows()
os.system('cls' if os.name == 'nt' else 'clear')
