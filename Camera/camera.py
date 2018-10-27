#!/usr/bin/env python3
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

from .create_gstreamer_pipe import create_gstreamer_pipe
from .convert_YUV import YUV_to_RGB, YUV_to_gray

class Camera():
    def __init__(self):
        pipeline, self.sink = create_gstreamer_pipe()
        ret = pipeline.set_state(Gst.State.PLAYING)  # TODO: print this value to the LOG file
        buffer = bytearray(self.__get_buffer())
        self.RGB_image = YUV_to_RGB(buffer)
        self.gray_image = YUV_to_gray(buffer)

    def __get_buffer(self):
        sample = self.sink.emit("pull-sample")
        buff = sample.get_buffer()
        buffer = buff.extract_dup(0, buff.get_size())
        return buffer

    def update_RGB_image(self):
        self.RGB_image = YUV_to_RGB(bytearray(self.__get_buffer()))

    def update_gray_image(self):
        self.gray_image = YUV_to_gray(bytearray(self.__get_buffer()))

    def get_RGB_image(self):
        return self.RGB_image

    def get_gray_image(self):
        return self.gray_image





