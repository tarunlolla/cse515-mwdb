#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 15:44:58 2019

@author: tarunlolla
"""
import cv2
import pymongo
import numpy as np
conn=pymongo.MongoClient('localhost',27017)
db=conn.phase1
collection_cm=db.color_moments
collection_sift=db.sift
collection_img_path=db.img_path

def eucl_dist(img1,img2):
    img1_id=img1[0]
    img1_vector=img1[1]
    img2_id=img2[0]
    img2_vector=img2[1]
    dist=0.0
    for i in range(0,len(img1_vector)):
        dist += (img1_vector[i]-img2_vector[i])**2
    return img2_id,dist**(1/2)

def query_img_cm(qimg_id,k):
    query={ '_id' : qimg_id }
    doc=collection_cm.find(query)
    for x in doc:
        query_y=x['y_cm']
        query_u=x['u_cm']
        query_v=x['v_cm']
        query_img_vector=[qimg_id,query_y+query_u+query_v]
    condition='$ne'
    all_images_query=collection_cm.find({'_id' : {condition: qimg_id}})
    all_images=[]
    for i in all_images_query:
        all_images.append([i['_id'],i['y_cm']+i['u_cm']+i['v_cm']])
    dist=[]
    for i in all_images:
        x,y=eucl_dist(query_img_vector,i)
        dist.append([x,y])
    dist=sorted(dist,key=lambda i:i[1])
    return dist[:k]

def query_img_sift(qimg_id,k):
    query={ '_id' : qimg_id }
    doc=collection_sift.find(query)
    for x in doc:
        query_img=[qimg_id,list(np.mean(x['descr'],axis=0))]
    condition='$ne'
    all_images_query=collection_sift.find({'_id' : {condition: qimg_id}})
    all_images=[]
    for i in all_images_query:
        all_images.append([i['_id'],list(np.mean(i['descr'],axis=0))])
    dist=[]
    for i in all_images:
        a,b=eucl_dist(query_img,i)
        dist.append([a,b])
    dist=list(sorted(dist,key=lambda i:i[1]))
    return dist[:k]

def main():
    img=input("Enter the id of the image to be queried :")
    feature=input("Select your preference of the model (Enter 1 or 2): \n 1. Color Moments \n 2. SIFT : \t")
    k=input("Enter the number of images to be matched :")
    if feature == '1':
        output=query_img_cm(img,int(k))
    elif feature == '2':
        output=query_img_sift(img,int(k))
    else:
        print("Error!!!! Invalid input for model")
    
    print("As per your choice of model, the result is as follows:")
    
    z=1
    for i in output:
        print("At rank ",z,"Image with ID ",i[0],"with a score of ",i[1])
        z+=1
    
    print("Images will be displayed now ...")
    path_query=collection_img_path.find({'_id' : { '$eq' : img }})
    path_query_img=list(path_query)[0]['location']
    disp_query_img=cv2.imread(path_query_img)
    cv2.imshow('Query Image',disp_query_img)
    cv2.waitKey(0)
    z=1
    disp_ans_img=[]
    for i in output:
        path_query=collection_img_path.find({'_id' : { '$eq' : i[0] }})
        for x in path_query:
            path=x['location']
        disp_img=cv2.imread(path)
        disp_ans_img.append(disp_img)
        #cv2.imshow('Rank '+str(z),disp_img)
    cv2.imshow('Ranked from left to right',np.concatenate(disp_ans_img[0:len(disp_ans_img)],axis=1))    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
if __name__ == '__main__' :
    main()
    
    
    
#Hand_0011684jpg