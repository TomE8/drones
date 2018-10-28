# drones
The JJRC H47 ELFIE+ is a cheap drone with on-board colored camera. The code in the repository allowes to fully control the movment of the drone using a joystick, and receive the image from the drone's camera as a python object (which can be used for image-prosessing). The code is written in python 3 and tested on Ubunto 16.04.

![alt text](https://image4.geekbuying.com/ggo_pic/2017-09-15/JJRC-H47-ELFIE-Plus-720P-WIFI-FPV-Foldable-Selfie-Drone-RTF-Blue-466215-.jpg)

# needed-packages:
1) opencv
2) numpy
3) gstreamer
4) pygame (for controling the drone using joystick)
5) tkinter (for minimal GUI)
# how to run:
1) connect to the wifi network of your drone
2) run the file: run_me.py
# what's in this repository:
the scripts are orgnized in folders:
1) camera - all the scripts that hendle reciving and displaying the images from the camera
2) control - all the scripts that hendle the movment of the drone
3) general - general scripst such: displaying minimal GUI and state machin of the program
4) sniffes - examples for sniffes of the communication between the drone and it's custom app 

