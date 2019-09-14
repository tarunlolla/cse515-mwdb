#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 16:13:53 2019

@author: tarunlolla
"""
import scipy
import cv2
import numpy as np
import sys
import os
np.set_printoptions(threshold=sys.maxsize);
import cm
import sift
import time
start_time = time.time()
color_moments=[]
sift_des=[]

work_dir=input("Enter the location of dataset:")

z=1
for i in os.listdir(work_dir):
    print(str(z)+" image running now")
    print("Computing color moments for "+i)
    x=cm.compute_cm(work_dir+'/'+i,100,100)
    color_moments.append([i,x])
    print("Finding descriptor vectors for "+i)
    y=sift.compute_des(work_dir+'/'+i)
    sift_des.append([i,list(y)])
    z += 1

print("--- %s seconds ---" % (time.time() - start_time))    
"""
/home/tarunlolla/MWDB/Project/Hands
Comments :: This code demonstrates how the blocks are being created.

import cv2
img=cv2.imread('/home/tarunlolla/MWDB/Project/Hand_0005140.jpg');
img[0:100,0:100]=[0,0,255];
img[0:100,100:200]=[0,0,0];
img[100:200,100:200]=[0,255,0];
img[200:300,200:300]=[255,0,0];
cv2.imshow('image',img);cv2.waitKey(0);cv2.destroyAllWindows();
"""
