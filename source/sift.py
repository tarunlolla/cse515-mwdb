#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 11:39:27 2019

@author: tarunlolla

This file contains one function, compute_des which takes the path to an image as a parameter and returns the feature descriptors vector in the format:
    [x,y,scale,orientation,a1,...,a128].

"""

import cv2
import numpy as np

def compute_des(img_path):
    img=cv2.imread(img_path)
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    sift = cv2.xfeatures2d.SIFT_create()
    kp,des = sift.detectAndCompute(gray,None)
    #img=cv2.drawKeypoints(gray,kp,img,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    return des[0]