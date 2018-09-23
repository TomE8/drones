#!/usr/bin/env python3
import numpy
import cv2
import subprocess as sp
import os
import signal

class Camera():
    def __init__(self):
        self.pipe = sp.Popen(["Camera/camera_tcp_session.py"], shell=True, stdout=sp.PIPE,bufsize=10 ** 8,preexec_fn=os.setsid)
        self.pipe2 = sp.Popen(["gst-launch-1.0 fdsrc ! h264parse ! avdec_h264 ! filesink location=/dev/stdout sync=false"],
                         shell=True, stdout=sp.PIPE, stdin=self.pipe.stdout, bufsize=10 ** 8,preexec_fn=os.setsid)
        self.pipe2.stdout.flush()
        self.update_image()

    def get_image(self):
        return self.image

    def update_image(self):
        while True:
            raw_image = self.pipe2.stdout.read(720 * 1280 * 3)
            if len(raw_image)>=720 * 1280 * 3:
                break
        raw_image = raw_image[:720 * 1280]
        self.image = numpy.fromstring(raw_image, dtype='uint8')
        self.image = self.image.reshape(720, 1280)
        self.image = numpy.concatenate((self.image[:, 141:], self.image[:, :141]), axis=1)

    def display_video_debug(self): # this method is only for debug
        while True:
            image=self.get_image()
            if image is not None:
                cv2.imshow('Video', image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()

    def __del__(self):
        os.killpg(os.getpgid(self.pipe.pid), signal.SIGTERM)
        os.killpg(os.getpgid(self.pipe2.pid), signal.SIGTERM)