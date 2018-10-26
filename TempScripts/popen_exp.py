#!/usr/bin/env python3

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject
Gst.init(None)
import numpy
import cv2
import time
import subprocess as sp
import os
import signal
import multiprocessing

import _thread
import threading

def print_list(list2):
    list=range(10)
    for elem in list2:
        print(elem)
        time.sleep(0.5)
    print("finish printing")

# _thread.start_new_thread(print_list(range(10)), ())
# t=threading.Thread(target=print_list)
t=multiprocessing.Process(target=print_list,args=(range(2,12),))
t.start()
for i in range(20,40):
    print("main " + str(i))
    time.sleep(0.3)
t.join()


