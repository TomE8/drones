#!/usr/bin/env python3
import numpy
import cv2
import subprocess as sp

class Camera():
    def __init__(self):
        pipe = sp.Popen(["/home/tom/Desktop/drone/Vision/camera_tcp_session.py"], shell=True, stdout=sp.PIPE,bufsize=10 ** 8)
        self.pipe2 = sp.Popen(["gst-launch-1.0 fdsrc ! h264parse ! avdec_h264 ! filesink location=/dev/stdout sync=false"],
                         shell=True, stdout=sp.PIPE, stdin=pipe.stdout, bufsize=10 ** 8)
        self.pipe2.stdout.flush()

    def get_image(self):
        while True:
            raw_image = self.pipe2.stdout.read(720 * 1280 * 3)
            if len(raw_image)>=720 * 1280 * 3:
                break
        raw_image = raw_image[:720 * 1280]
        image = numpy.fromstring(raw_image, dtype='uint8')
        image = image.reshape(720, 1280)
        image = numpy.concatenate((image[:, 141:], image[:, :141]), axis=1)
        return image

    def display_video(self):
        while True:
            image=self.get_image()
            if image is not None:
                cv2.imshow('Video', image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()