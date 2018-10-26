#!/usr/bin/env python3

import cv2
import numpy as np

def YUV_to_RGB(byteArray): # the format is I420
    # we start with getting the Y,U and V matrices
    Y = byteArray[0:921600] # 1280 * 720 = 921600
    Y = np.reshape(Y, (720, 1280))

    V=byteArray[921600:1152000] # 1280 * 720 * 1,25 = 1152000
    V = np.repeat(V, 2,0)
    V = np.reshape(V, (360, 1280))
    V = np.repeat(V, 2, 0)

    U=byteArray[1152000:]
    U = np.repeat(U, 2,0)
    U = np.reshape(U, (360, 1280))
    U = np.repeat(U, 2, 0)

    # we preform the conversion of the YUV format into RGB format:
    RGBMatrix = (np.dstack([Y, U, V])).astype(np.uint8)
    RGBMatrix = cv2.cvtColor(RGBMatrix, cv2.COLOR_YUV2RGB, 3)
    return RGBMatrix

def YUV_to_gray(byteArray):
    return np.reshape(byteArray[0:921600], (720, 1280)) # 1280 * 720 = 921600