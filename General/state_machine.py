#!/usr/bin/env python3
from .general_common import States
from Control.control_common import ButtonIndex

def getState(state, my_joystick):
    # ==============================================================
    if state == States.IDLE:
        if my_joystick.get_button_val(ButtonIndex.SIDE_BUTTON) == 1:
            return States.STAND_BY
        elif my_joystick.get_button_val(ButtonIndex.EXIT) == 1:
            return States.STOP_BEFORE_EXIT
    # ==============================================================
    elif state==States.STAND_BY:
        if my_joystick.get_button_val(ButtonIndex.TRIGGER) == 1:
            return States.MANUAL_CONTROL
        elif my_joystick.get_button_val(ButtonIndex.SIDE_BUTTON) == 1:
            return States.STOP
        elif my_joystick.get_button_val(ButtonIndex.EXIT) == 1:
            return States.STOP_BEFORE_EXIT
    # ==============================================================
    elif state==States.MANUAL_CONTROL:
        if my_joystick.get_button_val(ButtonIndex.HOVERING) == 1:
            return States.HOVERING
        if my_joystick.get_button_val(ButtonIndex.TRIGGER) == 1:
            return States.STOP
        if my_joystick.get_button_val(ButtonIndex.EXIT) == 1:
            return States.STOP_BEFORE_EXIT
    elif state==States.HOVERING:
        if my_joystick.get_button_val(ButtonIndex.HOVERING) == 1:
            return States.MANUAL_CONTROL
        if my_joystick.get_button_val(ButtonIndex.TRIGGER) == 1:
            return States.STOP
        if my_joystick.get_button_val(ButtonIndex.EXIT) == 1:
            return States.STOP_BEFORE_EXIT
    # ==============================================================
    elif state==States.STOP:
        return States.IDLE
    # ==============================================================
    elif state == States.STOP_BEFORE_EXIT:
        return States.EXIT
    return state
