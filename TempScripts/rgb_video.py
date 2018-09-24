#!/usr/bin/env python3

import numpy
import cv2
import subprocess as sp
import os
import signal

# from tcp_session import tcp_session
# from multiprocessing import Process

pipe = sp.Popen(["./tcp_session.py"], shell=True, stdout=sp.PIPE, bufsize=10 ** 8,preexec_fn=os.setsid)
pipe2 = sp.Popen(["./gstreamer.py"],  shell=True,stdin=pipe.stdout,preexec_fn=os.setsid)
print("WAIT FOR KEY PRESSED")
pause = input('')
os.killpg(os.getpgid(pipe.pid), signal.SIGTERM)
os.killpg(os.getpgid(pipe2.pid), signal.SIGTERM)
print("STOP")



