#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 21:56:25 2019

@author: fatema khalid
"""

import cv2
import pytesseract as pt
import numpy as np
from PIL import Image
import os



# CANNY algorithm
CANNY_KERRY_WONG_LOW_THRESHOLD_RATIO = 0.66
# we want to low threshold value of candy always below 0.1 #255, some
# image the contrast between button and background not must different
CANNY_RATIO_CONTROL_THRESHOLD = 0.1 / CANNY_KERRY_WONG_LOW_THRESHOLD_RATIO
    
dilationSize = 1
lowThreshold = 30
highThreshold = 80
ratio = 2

def updateLowHeightThreshold(imgData):
    imgHist = cv2.equalizeHist(imgData)
    mean = np.average(imgHist)
    lowThreshold = int(CANNY_KERRY_WONG_LOW_THRESHOLD_RATIO * mean * CANNY_RATIO_CONTROL_THRESHOLD)
    highThreshold = int(CANNY_KERRY_WONG_LOW_THRESHOLD_RATIO * ratio * mean * CANNY_RATIO_CONTROL_THRESHOLD)
    return lowThreshold, highThreshold

def getContours(img):
    # convert the resized image to grayscale, blur it slightly,
    # and threshold it
    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(grayImg, (5,5), 0)  
    #lowThreshold, highThreshold = updateLowHeightThreshold(blurred)
    kernel = np.ones((2 * dilationSize + 1, 2 * dilationSize + 1), np.uint8)
    edges = cv2.Canny(blurred, lowThreshold, highThreshold)
    morph = cv2.dilate(edges,kernel,iterations = 5)

    
    #finding the contours
    (contours, hierarchy, _)= cv2.findContours(morph, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cntr=contours
    

    j = 0
    margin = 10
    for cnt in cntr:
        x,y,w,h = cv2.boundingRect(cnt)
        if not os.path.exists(directory):
            os.makedirs(directory)
        crop_img = img[y-margin:y+h+margin, x-margin:x+w+margin]
        cv2.imwrite("components/comp"+str(j)+".jpg",crop_img)
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        j=j+1
    return cntr


'''
def processSave(directory, subdir, i):
    img=cv2.imread(directory)
    directory = directory.replace('.jpeg','')
    directory = directory.replace('.png','')
    getContours(img, directory)
    cv2.imwrite(subdir+"/output"+str(i)+".jpg",img)

#reading jpeg and png images in subfolders
rootdir = "dataset redraw"

for subdir, dirs, files in os.walk(rootdir):
    i=0
    for file in files:
        string = os.path.join(subdir, file)
        #print string
        if ".png" in string or ".jpeg" in string:
            processSave(string, subdir, i)
            i=i+1
'''
directory='image0.jpeg'
img=cv2.imread(directory)
getContours(img)
cv2.imwrite("output.jpg",img)