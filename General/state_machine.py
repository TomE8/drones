#!/usr/bin/env python3
from .general_common import States
from Control.control_common import ButtonIndex

def getMode(mode,my_joystick):
    # ==============================================================
    if mode == States.IDLE:
        if my_joystick.get_button_val(ButtonIndex.SIDE_BUTTON) == 1:
            return States.STAND_BY
        elif my_joystick.get_button_val(ButtonIndex.EXIT) == 1:
            return States.STOP_BEFORE_EXIT
    # ==============================================================
    elif mode==States.STAND_BY:
        if my_joystick.get_button_val(ButtonIndex.TRIGGER) == 1:
            return States.MANUAL_CONTROL
        elif my_joystick.get_button_val(ButtonIndex.SIDE_BUTTON) == 1:
            return States.STOP
        elif my_joystick.get_button_val(ButtonIndex.EXIT) == 1:
            return States.STOP_BEFORE_EXIT
    # ==============================================================
    elif mode==States.MANUAL_CONTROL:
        if my_joystick.get_button_val(ButtonIndex.TRIGGER) == 1:
            return States.STOP
        if my_joystick.get_button_val(ButtonIndex.EXIT) == 1:
            return States.STOP_BEFORE_EXIT
    # ==============================================================
    elif mode==States.STOP:
        return States.IDLE
    # ==============================================================
    elif mode == States.STOP_BEFORE_EXIT:
        return States.EXIT
    return mode