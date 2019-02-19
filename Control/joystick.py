import pygame
from Control.control_common import AxisIndex, ButtonIndex

class Joystick:
    def __init__(self,left_right_clip_val,forward_backwards_clip_val,rotate_clip_val,up_down_clip_val):
        pygame.init()
        pygame.joystick.init()
        self.joystick = pygame.joystick.Joystick(0) # TODO: throw error if no joystick was found
        self.joystick.init()
        self.clip_val={AxisIndex.LEFT_RIGHT:left_right_clip_val,
                       AxisIndex.FORWARD_BACKWARDS:forward_backwards_clip_val,
                       AxisIndex.ROTATE:rotate_clip_val,
                       AxisIndex.UP_DOWN:up_down_clip_val}
        self.button_list=[ButtonIndex.EXIT,ButtonIndex.SIDE_BUTTON,ButtonIndex.TRIGGER, ButtonIndex.HOVERING] # TODO: read these values automaticly
        self.prev_button_val = {}
        for button in self.button_list:
            self.prev_button_val[button]=0


    def get_axis_val(self,axis_index):
        return self.__clip(self.joystick.get_axis(axis_index),self.clip_val.get(axis_index))

    def get_button_val(self,button_index):
        return self.joystick.get_button(button_index) - self.prev_button_val.get(button_index)

    def __del__(self):  # destructor
        pygame.quit()

    @staticmethod
    def __clip(x, pivot):
        if abs(x) < pivot:
            return 0
        elif x > pivot:
            return (x - pivot) / (1 - pivot)
        else:  # x<-pivot
            return (x + pivot) / (1 - pivot)

    @staticmethod
    def refresh():
        pygame.event.get()

    def update_values(self):
        for button in self.button_list:
            self.prev_button_val[button]=self.joystick.get_button(button)


