#!/usr/bin/env python3
import numpy as np
import cv2

# read the image:
img = cv2.imread('Tilapia.jpg',cv2.IMREAD_COLOR)

# split to RGB:
b,g,r = cv2.split(img)
split=[r,g,b]

# display RGB image:
cv2.imshow('image',img)
cv2.waitKey(0)

# display R,G,B images:
for i in range(3):
    split_img = np.zeros(img.shape, dtype="uint8")
    split_img[:,:,i]=split[i]
    cv2.imshow('image',split_img)
    cv2.imwrite("/home/tom/Desktop/temp/drones/"+str(i)+".jpg", split_img)
    cv2.waitKey(0)

# close all windows:
HSV = cv2.cvtColor(img, cv2.COLOR_RGB2HSV, 3)
split_HSV = cv2.split(HSV)
for i in range(3):
    split_img = np.zeros(HSV.shape, dtype="uint8")
    split_img[:, :, 0] = split_HSV[i]
    split_img[:, :, 1] = split_HSV[i]
    split_img[:, :, 2] = split_HSV[i]
    cv2.imshow('image',split_img)
    cv2.imwrite("/home/tom/Desktop/temp/drones/"+str(i+3)+".jpg", split_img)
    cv2.waitKey(0)

cv2.destroyAllWindows()


