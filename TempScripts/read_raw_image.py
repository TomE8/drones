#!/usr/bin/env python3

import cv2
import numpy as np


# f = open("raw_yuv_image",'rb')
# raw_image = f.read(720 * 1280 * 3)
# raw_image = bytearray(raw_image)
def YUVtoRGB(byteArray):
    e = 1280 * 720
    Y = byteArray[0:e]
    Y = np.reshape(Y, (720, 1280))

    V=byteArray[e:int(e*1.25)]
    V = np.repeat(V, 2,0)
    V = np.reshape(V, (360, 1280))
    V = np.repeat(V, 2, 0)

    U=byteArray[int(e*1.25):]
    U = np.repeat(U, 2,0)
    U = np.reshape(U, (360, 1280))
    U = np.repeat(U, 2, 0)

    RGBMatrix = (np.dstack([Y, U, V])).astype(np.uint8)
    RGBMatrix = cv2.cvtColor(RGBMatrix, cv2.COLOR_YUV2RGB, 3)
    return RGBMatrix

# image=YUVtoRGB(raw_image)
# cv2.imshow('Image', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# cv2.waitKey(1)

