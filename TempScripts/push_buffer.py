#!/usr/bin/env python3
# gst-launch-1.0 fdsrc ! h264parse ! avdec_h264 ! filesink location=/dev/stdout sync=false

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject
Gst.init(None)
import numpy
import cv2
import time
import socket
import sys
import time

from read_raw_image import YUVtoRGB


class TCP_SESSION():
    def __init__(self,src):
        TCP_IP="172.16.10.1" # TODO: read this value from config file
        TCP_PORT=8888 # TODO: read this value from config file
        self.BUFFER_SIZE = 8200 #4096  # TODO: read this value from config file
        try:
            self.TCP_sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.TCP_sock.settimeout(5.0)
            self.TCP_sock.connect((TCP_IP,TCP_PORT))
            self.heartbeat=bytearray([0x0,0x1,0x2,0x3,0x4,0x5,0x6,0x7,0x8,0x9,0x28,0x28])
            self.TCP_sock.send(self.heartbeat)
        except:
            print("TIME OUT")
            exit(-1)
        self.t0=time.time()
        self.src= src
        print("end of init")

    def push_data(self):
        data = self.TCP_sock.recv(self.BUFFER_SIZE)
        self.src.emit("push-buffer", Gst.Buffer.new_wrapped(data))
        self.__heart_beat()
        # print(len(data))

    def __heart_beat(self):
        if time.time()-self.t0>1:
            self.t0=time.time()
            try:
                self.TCP_sock.send(self.heartbeat)
            except:
                exit(-1)

    def __del__(self):
        self.TCP_sock.close()


# create the elements:
source = Gst.ElementFactory.make("appsrc", "file-source")
# source = Gst.ElementFactory.make("fdsrc", "file-source")
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

bus = pipeline.get_bus()
#
# from multiprocessing import Process
# from tcp_session import tcp_session
# source.set_property('stream-type', 'stream')
# p1 = Process(target=tcp_session, args=(source,))
# p1.start()
# data = open("raw_yuv_image","rb").read()
# source.emit("push-buffer", Gst.Buffer.new_wrapped(data))

# fd = open("LOG.txt","w")
# fd.write("Beggining: \n")
# fd = open("LOG.txt","a")
ret = pipeline.set_state(Gst.State.PLAYING) #TODO: print this value to the LOG file
print(ret)
my_tcp_session = TCP_SESSION(source)
while(1):
    for i in range(50):
        my_tcp_session.push_data()
    # print("finish pushing")
    # fd.write("finish pusing\n")
    sample = sink.emit("pull-sample")
    if sample:
        buff=sample.get_buffer()
        # TODO: print to the LOG file the format and the size of the image
        # message = bus.timed_pop_filtered(10000, Gst.MessageType.ANY)
        # if message:
        #     fd.write(str(message) + "\n")
        # caps=sample.get_caps()
        buffer = buff.extract_dup(0, buff.get_size())
        image= YUVtoRGB(bytearray(buffer))
        cv2.imshow("video", image)
        cv2.waitKey(1)
        time.sleep(0.01)
# p1.join()
fd.close()

