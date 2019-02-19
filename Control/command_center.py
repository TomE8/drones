#!/usr/bin/env python3
import socket
import time
from General.general_common import States
from .control_common import AxisIndex, ThresHold


class CommandCenter():
    def __init__(self):
        self.UDP_IP = "172.16.10.1" # TODO: read these values from config file
        self.UDP_PORT = 8080
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
        self.prev_time = time.time()
        self.prev_command_hash = 0

    def __send_to_drone(self, up_down, rotate, forward_backwards, left_right, byte6, byte7, byte8, byte9):
        current_time = time.time()
        current_command_hash = hash((up_down, rotate, forward_backwards, left_right))
        # we will send a massage if:
        # 1) it has been ThresHold.SENDING_TIME seconds from the last message
        # 2) the new message is not as the one sent before
        if (current_time - self.prev_time) > ThresHold.SENDING_TIME or current_command_hash != self.prev_command_hash:
            command = bytearray([255, 8, up_down, rotate, forward_backwards, left_right, byte6, byte7, byte8, byte9])
            command.extend([255 - sum(command[1:]) % 256])  # check sum
            self.sock.sendto(command, (self.UDP_IP, self.UDP_PORT))
            self.prev_time = current_time
            self.prev_command_hash = current_command_hash

    def perform_action(self, state, my_joystick):
        if state == States.IDLE:
            self.__send_to_drone(0, 63, 64, 63, 144, 16, 16, 0)  # stand by
        elif state == States.STAND_BY:
                self.__send_to_drone(126, 63, 64, 63, 144, 16, 16, 64)  # start engines
        elif state == States.MANUAL_CONTROL:
            up_down = 126 + int(-1 * my_joystick.get_axis_val(AxisIndex.UP_DOWN) * 126)
            rotate = 63 + int(my_joystick.get_axis_val(AxisIndex.ROTATE) * 63)
            forward_backwards = 64 + int(my_joystick.get_axis_val(AxisIndex.FORWARD_BACKWARDS) * 63)
            left_right = 63 + int(my_joystick.get_axis_val(AxisIndex.LEFT_RIGHT) * 63)
            self.__send_to_drone(up_down, rotate, forward_backwards, left_right, 144, 16, 16, 0)
        elif state == States.HOVERING:
            self.__send_to_drone(160, 63, 64, 63, 144, 16, 16, 0)  # hovering
        if state == States.STOP or state == States.STOP_BEFORE_EXIT:
            self.__send_to_drone(126, 63, 64, 63, 144, 16, 16, 160)  # stop


    @staticmethod
    def __byte9(mSpeedValue, m360RollValue, mNoHeadValue, mStopValue, mToflyValue, mToLandValue):
        return mSpeedValue | m360RollValue << 2 | mNoHeadValue << 4 | mStopValue << 5 | mToflyValue << 6 | mToLandValue << 7