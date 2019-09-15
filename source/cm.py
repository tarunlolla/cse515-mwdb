#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 16:13:53 2019

@author: tarunlolla

This file returns the computed mean, standard deviation and skewness for a given image as a tuple and has the below functions:

split_image: Takes as input the path to image, and the height and width in which the image is to be split to compute color moments block by block.

compute_yuv: This function converts the given BGR to YUV and returns only the Y value. For convinience of calculation, we only consider the Y channel to calculate color moments

     
    
"""
import scipy.stats as scs
import math
import cv2
from PIL import Image
import numpy as np
import sys
np.set_printoptions(threshold=sys.maxsize);

block_mean=[]
block_sd=[]
block_sk=[]

def split_image(image,split_height,split_width):
    img=cv2.imread(image)
    img=cv2.cvtColor(img,cv2.COLOR_BGR2YUV)
    height,width,depth = img.shape
    blocks=[]
    for j in range(0,height,split_height):
        for i in range(0,width,split_width):
            temp_block=img[i:i+split_width,j:j+split_height]
            blocks.append(temp_block)
    #print(str(len(blocks))+" blocks created.")
    return blocks


def compute_yuv_cm(block,idx):
    block_channel=[]
    for i in block:
        for j in i:
            block_channel.append(j[idx])
    mean=np.mean(block_channel)
    std=np.std(block_channel)
    skew=scs.skew(block_channel)
    return [mean,std,skew]

def compute_img_cm(blocks_cm):
    blocks_y_mean=[]
    blocks_u_mean=[]
    blocks_v_mean=[]
    blocks_y_std=[]
    blocks_u_std=[]
    blocks_v_std=[]
    blocks_y_skew=[]
    blocks_u_skew=[]
    blocks_v_skew=[]
    for i in blocks_cm:
        blocks_y_mean.append(i[0][0])
        blocks_u_mean.append(i[1][0])
        blocks_v_mean.append(i[2][0])
        blocks_y_std.append(i[0][1])
        blocks_u_std.append(i[1][1])
        blocks_v_std.append(i[2][1])
        blocks_y_skew.append(i[0][2])
        blocks_u_skew.append(i[1][2])
        blocks_v_skew.append(i[2][2])
    y_cm= [np.mean(blocks_y_mean),np.std(blocks_y_std),scs.skew(blocks_y_skew)]
    u_cm= [np.mean(blocks_u_mean),np.std(blocks_u_std),scs.skew(blocks_u_skew)]
    v_cm= [np.mean(blocks_v_mean),np.std(blocks_v_std),scs.skew(blocks_v_skew)]
    return [y_cm,u_cm,v_cm]
    
def compute_cm(image_path,block_height,block_width):
    b=split_image(image_path,block_height,block_width)
    # Calculating Resultant mean for the image
    blocks_cm=[]
    for i in b:
        y=compute_yuv_cm(i,0)
        u=compute_yuv_cm(i,1)
        v=compute_yuv_cm(i,2)
        blocks_cm.append(np.nan_to_num([y,u,v]))
    img_cm=compute_img_cm(blocks_cm)
    #print(img_cm)
    return img_cm 
   

"""
Comments :: This code demonstrates how the blocks are being created.

import cv2
img=cv2.imread('/home/tarunlolla/MWDB/Project/Hand_0005140.jpg');
img[0:100,0:100]=[0,0,255];
img[0:100,100:200]=[0,0,0];
img[100:200,100:200]=[0,255,0];
img[200:300,200:300]=[255,0,0];
cv2.imshow('image',img);cv2.waitKey(0);cv2.destroyAllWindows();
"""