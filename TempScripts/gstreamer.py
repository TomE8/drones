#!/usr/bin/env python3
# gst-launch-1.0 fdsrc ! h264parse ! avdec_h264 ! filesink location=/dev/stdout sync=false

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject
Gst.init(None)
import numpy
import cv2
import time

from read_raw_image import YUVtoRGB
# from tcp_session import tcp_session

# create the elements:
# source = Gst.ElementFactory.make("appsrc", "file-source")
source = Gst.ElementFactory.make("fdsrc", "file-source")
h264parse = Gst.ElementFactory.make("h264parse", "h264")
avdec_h264 = Gst.ElementFactory.make("avdec_h264", "avdec_h264")
sink = Gst.ElementFactory.make("appsink", "appsink")

# create the pipeline:
pipeline = Gst.Pipeline.new("drone-pipeline")
pipeline.add(source)
pipeline.add(h264parse)
pipeline.add(avdec_h264)
pipeline.add(sink)

# link the elements:
source.link(h264parse)
h264parse.link(avdec_h264)
avdec_h264.link(sink)

sink.set_property("emit-signals", True)
#
# from multiprocessing import Process
# source.set_property('stream-type', 'stream')
# p1 = Process(target=tcp_session, args=(source,))
# p1.start()

ret = pipeline.set_state(Gst.State.PLAYING) #TODO: print this value to the LOG file
print(ret)
while(1):
    sample = sink.emit("pull-sample")
    if sample:
        buff=sample.get_buffer()
        # caps=sample.get_caps()
        buffer = buff.extract_dup(0, buff.get_size())
        image= YUVtoRGB(bytearray(buffer))
        cv2.imshow("video", image)
        cv2.waitKey(1)
        time.sleep(0.02)
# p1.join()

