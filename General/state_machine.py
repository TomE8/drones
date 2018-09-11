#!/usr/bin/env python3
from .general_common import Modes
from Control.control_common import ButtonIndex

def getMode(mode,my_joystick):
    # ==============================================================
    if mode == Modes.IDLE:
        if my_joystick.get_button_val(ButtonIndex.SIDE_BUTTON) == 1:
            return Modes.STAND_BY
        elif my_joystick.get_button_val(ButtonIndex.EXIT) == 1:
            return Modes.STOP_BEFORE_EXIT
    # ==============================================================
    elif mode==Modes.STAND_BY:
        if my_joystick.get_button_val(ButtonIndex.TRIGGER) == 1:
            return Modes.MANUAL_CONTROL
        elif my_joystick.get_button_val(ButtonIndex.SIDE_BUTTON) == 1:
            return Modes.STOP
        elif my_joystick.get_button_val(ButtonIndex.EXIT) == 1:
            return Modes.STOP_BEFORE_EXIT
    # ==============================================================
    elif mode==Modes.MANUAL_CONTROL:
        if my_joystick.get_button_val(ButtonIndex.TRIGGER) == 1:
            return Modes.STOP
        if my_joystick.get_button_val(ButtonIndex.EXIT) == 1:
            return Modes.STOP_BEFORE_EXIT
    # ==============================================================
    elif mode==Modes.STOP:
        return Modes.IDLE
    # ==============================================================
    elif mode == Modes.STOP_BEFORE_EXIT:
        return Modes.EXIT
    return mode