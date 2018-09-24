#!/usr/bin/env python3

import cv2
import numpy as np

# cap = cv2.VideoCapture('video_pipe')
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280);
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720);
# cap.read()
f = open("raw_yuv_image",'rb')
raw_image = f.read(720 * 1280 * 3)
raw_image = bytearray(raw_image)
def YUVtoRGB(byteArray):
    e = 1280 * 720
    Y = byteArray[0:e]
    Y = np.reshape(Y, (720, 1280))

    s = e
    # V = byteArray[s::2]
    print(s*1.5)
    V=byteArray[s:int(s*1.25)]
    V = np.repeat(V, 2,0)
    V = np.reshape(V, (360, 1280))
    V = np.repeat(V, 2, 0)

    # U = byteArray[s + 1::2]
    U=byteArray[int(s*1.25):]
    U = np.repeat(U, 2,0)
    U = np.reshape(U, (360, 1280))
    U = np.repeat(U, 2, 0)

    RGBMatrix = (np.dstack([Y, U, V])).astype(np.uint8)
    RGBMatrix = cv2.cvtColor(RGBMatrix, cv2.COLOR_YUV2RGB, 3)
    return RGBMatrix

# raw_image=raw_image[:720 * 1280]
# raw_image=raw_image[720 * 1280:720 * 1280*2]
# raw_image=raw_image[720 * 1280*2:720 * 1280*3]
# raw_image=raw_image[360 * 1280:]
# print(type(raw_image))
# raw_image = f.read(720 * 1280)
# raw_image = f.read(720 * 1280)
# raw_image = f.read(720 * 1280)

# raw_image.decode("utf-8",'replace')
# image = np.fromstring(raw_image, dtype='uint8')
# image=np.frombuffer(raw_image,dtype='uint8')
# image=numpy.delete(image,range(720*1280+1,720*1280*3))
# image = image.reshape((720,1280))
# image = image.reshape((360,1280))
# image = cv2.cvtColor(image, cv2.COLOR_)
# image1=numpy.delete(image,range(141),1)
# image2=numpy.delete(image,range(141,1280),1)
# image=numpy.concatenate((image[:,141:],image[:,:141]),axis=1)
# image=image1
# image = cv2.cvtColor(image,cv2.COLOR_YUV2RGB)
# image=YUVtoRGB(raw_image)


# e = 1280 * 720
# Y = raw_image[0:e]
# Y = np.reshape(Y, (720, 1280))
#
# V=raw_image[e::2]
# V=np.repeat(V,2)
# V=np.reshape(V,(360,1280))
# V=np.repeat(V,2,0)
#
#
# V=range(4)
# print(V)
# V_temp=np.repeat(V,2)
#
# V_temp=np.reshape(V_temp,(2,4))
# print(V_temp)
# print("=============")
# V_temp=np.repeat(V_temp,2,0)
# print(V_temp)
# V = raw_image[e:*e:2]
# print(len(V))

image=YUVtoRGB(raw_image)
cv2.imshow('Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)

