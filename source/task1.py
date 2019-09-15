#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 00:31:07 2019

@author: tarunlolla
"""

import scipy
import cv2
import numpy as np
import sys
np.set_printoptions(threshold=sys.maxsize);
import cm
import sift
import warnings
warnings.filterwarnings("ignore")

def main():
    img_path=input("Enter the path to the image : ")
    feature=input("Select your preference of the model (Enter 1 or 2): \n 1. Color Moments \n 2. SIFT : \t")
    if feature == '1':
        img=cv2.imread(img_path)
        height,width,depth = img.shape
        print("\nThis feature involves splitting the image into smaller windows. The dimensions of image are ",height," X ",width)
        height=input("Enter the preferred height of each window : ")
        width=input("Enter the preferred height of each window : ")
        output=cm.compute_cm(img_path,int(height),int(width))
        print("\nThe obtained color moments for the image are: ")
        print("For channel Y :")
        print("\tMean : ",output[0][0])
        print("\tStandard Deviation : ",output[0][1])
        print("\tSkewness : ",output[0][2])
        print("For channel U :")
        print("\tMean : ",output[1][0])
        print("\tStandard Deviation : ",output[1][1])
        print("\tSkewness : ",output[1][2])
        print("For channel V :")
        print("\tMean : ",output[2][0])
        print("\tStandard Deviation : ",output[2][1])
        print("\tSkewness : ",output[2][2])
    elif feature == '2':
        output=sift.compute_des(img_path)
        print("After SIFT computation, ",len(output)," keypoints are obtained.")
        z=1
        for i in output:
            print("Keypoint ",z,":\n",i)
            z+=1
    else:
        print("Error!!!! Invalid input for model")
    
    

if __name__ == '__main__':
    main()