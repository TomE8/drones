#!/usr/bin/env python3

import cv2

import cv2
import numpy

# cap = cv2.VideoCapture('video_pipe')
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280);
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720);
# cap.read()
f = open("raw_image",'rb')
raw_image = f.read(720 * 1280 * 3)
# raw_image=raw_image[:720 * 1280]
# raw_image=raw_image[720 * 1280:720 * 1280*2]
raw_image=raw_image[720 * 1280*2:720 * 1280*3]
# raw_image=raw_image[360 * 1280:]
print(type(raw_image))
# raw_image = f.read(720 * 1280)
# raw_image = f.read(720 * 1280)
# raw_image = f.read(720 * 1280)

# raw_image.decode("utf-8",'replace')
# image = numpy.fromstring(raw_image, dtype='uint8')
image=numpy.frombuffer(raw_image,dtype='uint8')
# image=numpy.delete(image,range(720*1280+1,720*1280*3))
image = image.reshape((720,1280))
# image = image.reshape((360,1280))
# image = cv2.cvtColor(image, cv2.COLOR_)
# image1=numpy.delete(image,range(141),1)
# image2=numpy.delete(image,range(141,1280),1)
image=numpy.concatenate((image[:,141:],image[:,:141]),axis=1)
# image=image1
# image = cv2.cvtColor(image,cv2.COLOR_YUV2RGB)
cv2.imshow('Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)

