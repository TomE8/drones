#!/usr/bin/env python3

import numpy
import cv2
import subprocess as sp

pipe = sp.Popen(["Camera/camera_tcp_session.py"], shell=True, stdout=sp.PIPE, bufsize=10 ** 8)
pipe2 = sp.Popen(["gst-launch-1.0 fdsrc ! h264parse ! avdec_h264 ! filesink location=/dev/stdout sync=false"], shell=True, stdout=sp.PIPE, stdin=pipe.stdout, bufsize=10 ** 8)
pipe2.stdout.flush()
while True:
    raw_image = pipe2.stdout.read(720 * 1280 * 3)
    if len(raw_image)<720 * 1280 * 3:
        continue # TODO: count the number of failure and exit if it is greater then a threshold
    raw_image = raw_image[:720*1280]
    image = numpy.fromstring(raw_image, dtype='uint8')
    image = image.reshape(720, 1280)
    image = numpy.concatenate((image[:, 141:], image[:, :141]), axis=1)
    if image is not None:
        cv2.imshow('Video', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()

