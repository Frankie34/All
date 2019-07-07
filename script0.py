#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 14:11:58 2019

@author: junchengzhu
    
    image edge detection

"""

"""
# about how to capture a video from cam

import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame by frame
    ret, frame = cap.read();
    
    # Our operations on the frame comes here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Display the resulting frame
    cv2.imshow('frame', gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
"""
"""
import numpy as np
import cv2

# Load an color image in grayscale
img = cv2.imread('jet.jpg',0)

rows,cols = img.shape

M = cv2.getRotationMatrix2D((cols/2,rows/2),90,1)
dst = cv2.warpAffine(img,M,(cols,rows))

cv2.imshow('jet', dst)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""


from PyQt5.QtWidgets import QApplication, QLabel
app = QApplication([])
label = QLabel('Hello World')
label.show()
app.exec()


    
    
    
    
    
    
    
    
    
    