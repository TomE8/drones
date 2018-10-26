#!/usr/bin/env python3

import subprocess as sp
import os
import signal
import time

pipe = sp.Popen(["./Camera/camera_tcp_session.py"], shell=True, stdout=sp.PIPE, bufsize=10 ** 8,preexec_fn=os.setsid)
pipe2 = sp.Popen(["./main.py"],  shell=True,stdin=pipe.stdout,preexec_fn=os.setsid)
time.sleep(1)
while pipe2.poll() is None: # if pipe2 is still working, go to sleep for 1 second
    time.sleep(1)
os.killpg(os.getpgid(pipe.pid), signal.SIGTERM)
