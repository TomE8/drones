#!/usr/bin/env python3
import socket
from General.general_common import Modes
from .control_common import AxisIndex

# TODO: read these values from config file
UDP_IP = "172.16.10.1"
UDP_PORT = 8080
BUFFER_SIZE = 1024
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP

def byte9(mSpeedValue,m360RollValue,mNoHeadValue,mStopValue,mToflyValue,mToLandValue):
    return mSpeedValue | m360RollValue<<2 | mNoHeadValue<<4 | mStopValue<<5 | mToflyValue<<6 | mToLandValue<<7

def send_command(up_down, rotate, foward_backwards, left_right, byte6, byte7, byte8, byte9):
    command = bytearray([255,8,up_down,rotate,foward_backwards,left_right,byte6,byte7,byte8,byte9])
    command.extend([255 - sum(command[1:]) % 256]) # check sum
    sock.sendto(command, (UDP_IP, UDP_PORT))

def command_center(mode, my_joystick):
    if mode == Modes.IDLE:
        send_command(0, 63, 64, 63, 144, 16, 16, 0) # stand by
    elif mode == Modes.STAND_BY:
        send_command(126, 63, 64, 63, 144, 16, 16, 64)  # start engines
    elif mode == Modes.STOP or mode == Modes.STOP_BEFORE_EXIT:
        send_command(126, 63, 64, 63, 144, 16, 16, 160)  # stop
    elif mode == Modes.MANUAL_CONTROL:
        up_down = 126 + int(-1 * my_joystick.get_axis_val(AxisIndex.UP_DOWN) * 126)
        left_right = 63 + int(my_joystick.get_axis_val(AxisIndex.LEFT_RIGHT) * 63)
        rotate = 63 + int(my_joystick.get_axis_val(AxisIndex.ROTATE) * 63)
        forward_backwards = 64 + int(my_joystick.get_axis_val(AxisIndex.FORWARD_BACKWARDS) * 63)
        send_command(up_down, rotate, forward_backwards, left_right, 144, 16, 16, 0)