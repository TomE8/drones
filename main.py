#!/usr/bin/env python3
import cv2
import time

from General.state_machine import getState
from General.general_common import States
from General.gui import Screen

from Control.joystick import Joystick
from Control.command_center import CommandCenter

from Camera.camera import Camera

my_joystick = Joystick(0.1,0.1,0.2,0.1) # TODO: read these values from the config file
my_camera = Camera()
my_command_center = CommandCenter()
my_screen = Screen()
state=States.IDLE

fourcc = cv2.VideoWriter_fourcc(*'XVID')
video = cv2.VideoWriter('flight.avi', fourcc, 20.0, (1280, 720))

while state != States.EXIT:
    my_joystick.refresh()
    state = getState(state, my_joystick)
    my_command_center.perform_action(state, my_joystick=my_joystick)

    image = my_camera.get_RGB_image()
    cv2.imshow("video", image)
    cv2.waitKey(1)
    video.write(image)

    my_camera.update_RGB_image()
    my_screen.update_state(state)
    my_joystick.update_values()

video.release()
cv2.destroyAllWindows()
