#!/usr/bin/env python3

import subprocess as sp
import os
import signal

tcp_proc = sp.Popen(["./Camera/camera_tcp_session.py"], shell=True, stdout=sp.PIPE, bufsize=10 ** 8, preexec_fn=os.setsid)
main_proc = sp.Popen(["./main.py"],  shell=True, stdin=tcp_proc.stdout, preexec_fn=os.setsid)
main_proc.wait()
os.killpg(os.getpgid(tcp_proc.pid), signal.SIGTERM)
