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
from keep_alive import CommandCenter

# create the elements:
# source = Gst.ElementFactory.make("appsrc", "file-source")
source = Gst.ElementFactory.make("fdsrc", "file-source")
queue = Gst.ElementFactory.make('queue',"Q") # !
h264parse = Gst.ElementFactory.make("h264parse", "h264")
avdec_h264 = Gst.ElementFactory.make("avdec_h264", "avdec_h264")
sink = Gst.ElementFactory.make("appsink", "appsink")

# create the pipeline:
pipeline = Gst.Pipeline.new("drone-pipeline")
pipeline.add(source)
pipeline.add(queue)
pipeline.add(h264parse)
pipeline.add(avdec_h264)
pipeline.add(sink)

# link the elements:
# source.link(h264parse)
source.link(queue)
queue.link(h264parse)
h264parse.link(avdec_h264)
avdec_h264.link(sink)

sink.set_property("emit-signals", True)
# queue.set_property("min-threshold-bytes",int(720*1280*1.5))

bus = pipeline.get_bus()



def wait_for_data(source, length):
    print("waiting")
    time.sleep(0.1)


# def on_source_setup(element, source):
# source.connect("need-data", wait_for_data)

# pipeline.connect("source-setup",on_source_setup)


ret = pipeline.set_state(Gst.State.PLAYING) #TODO: print this value to the LOG file


# from multiprocessing import Process
# from tcp_session import tcp_session
# import threading
# source.set_property('stream-type', 'stream')
# p1 = threading.Thread(target=tcp_session, args=(source,))
# p1.start()
# data = open("raw_yuv_image","rb").read()
# source.emit("push-buffer", Gst.Buffer.new_wrapped(data))
# print(ret)
# time.sleep(2)
# print("starting while")
# my_comand_center=CommandCenter()
while(1):
    # my_comand_center.keep_alive()
    sample = sink.emit("pull-sample")
    if sample:
        buff=sample.get_buffer()
        # TODO: print to the LOG file the format and the size of the image
        message = bus.timed_pop_filtered(10000, Gst.MessageType.ANY)
        if message:
            print(message.type)
            #print(len(message))
        # caps=sample.get_caps()
        buffer = buff.extract_dup(0, buff.get_size())
        image= YUVtoRGB(bytearray(buffer))
        cv2.imshow("video", image)
        cv2.waitKey(1)
        time.sleep(0.01)
