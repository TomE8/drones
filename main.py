#!/usr/bin/env python3
import cv2
import time
from gi.repository import Gst, GObject

from General.state_machine import getState
from General.general_common import States
from General.gui import Screen

from Control.joystick import Joystick
from Control.command_center import CommandCenter

from Camera.create_gstreamer_pipe import create_gstreamer_pipe
from Camera.YUV_to_RGB import YUV_to_RGB


my_joystick=Joystick(0.1,0.1,0.2,0.1) # TODO: read these values from the config file
my_command_center = CommandCenter()
my_screen = Screen()
state=States.IDLE

pipeline, sink= create_gstreamer_pipe()
ret = pipeline.set_state(Gst.State.PLAYING) #TODO: print this value to the LOG file

while state != States.EXIT:
    my_joystick.refresh()
    state = getState(state, my_joystick)
    my_command_center.perform_action(state, my_joystick=my_joystick)

    sample = sink.emit("pull-sample")
    if sample:
        buff=sample.get_buffer()
        buffer = buff.extract_dup(0, buff.get_size())
        image= YUV_to_RGB(bytearray(buffer))
        cv2.imshow("video", image)
        cv2.waitKey(1)
        time.sleep(0.01)

    my_screen.update_state(state)
    my_joystick.update_values()

cv2.destroyAllWindows()
