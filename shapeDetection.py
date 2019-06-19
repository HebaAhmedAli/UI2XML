#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 16:41:36 2019

@author: heba
"""

import cv2
import numpy as np
import math

image = cv2.imread("/home/heba/Documents/cmp/fourth_year/gp/UI2XML/data/testImagesShapes/35-android.widget.ImageButton.jpg")

'''
# convert the color image into grayscale
grayScale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Find edges in the image using canny edge detection method
# Calculate lower threshold and upper threshold using sigma = 0.33
sigma = 0.33
v = np.median(grayScale)
low = int(max(0, (1.0 - sigma) * v))
high = int(min(255, (1.0 + sigma) * v))

edged = cv2.Canny(grayScale, low, high)
'''
# After finding edges we have to find contours
# Contour is a curve of points with no gaps in the curve
# It will help us to find location of shapes

# cv2.RETR_EXTERNAL is passed to find the outermost contours (because we want to outline the shapes)
# cv2.CHAIN_APPROX_SIMPLE is removing redundant points along a line

'''
We are going to use contour approximation method to find vertices of
geometric shapes. The alogrithm  is also known as Ramer Douglas Peucker alogrithm.
In OpenCV it is implemented in cv2.approxPolyDP method.abs
detectShape() function below takes a contour as parameter and
then returns its shape
 '''


def detectShape(cnt):
    shape = 'unknown'
    if M['m00'] > 0:
        # calculate perimeter using
        peri = cv2.arcLength(cnt, True)
        area = cv2.contourArea(cnt)
        circularity  = 4*math.pi*(area/(peri*peri))
        # apply contour approximation and store the result in vertices
        vertices = cv2.approxPolyDP(cnt, 0.04 * peri, True)
        x, y, width, height = cv2.boundingRect(vertices)
        aspectRatio = float(width) / height
        if len(vertices) == 4 and aspectRatio >= 0.95 and aspectRatio <= 1.05:
            shape = "square"
        elif len(vertices) > 5 and circularity >= 0.7:
            shape = "circle"
        else:
            shape = "unknown"
    return shape

dilationSize = 1
lowThreshold = 30 #30
highThreshold = 60 #60

# Now we will loop over every contour
# call detectShape() for it and
# write the name of shape in the center of image
def preProcess(image):
    # convert the image to grayscale, blur it slightly, and threshold it
    #ran=str(random.randint(0,100))
    grayImg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(grayImg, (3,3), 0)  
    #cv2.imwrite('data/images/'+ran+'accountblurres.png',blurred)
    kernel = np.ones((2 * dilationSize + 1, 2 * dilationSize + 1), np.uint8)
    edges = cv2.Canny(blurred, lowThreshold, highThreshold)
    #cv2.imwrite('data/images/'+ran+'accountedges.png',edges)
    #morph = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    #morph = cv2.dilate(edges,kernel,iterations = 5)
    #cv2.imwrite('data/images/'+ran+'accountmorph.png',morph)
    return edges
# loop over the contours

edged = preProcess(image)
(_, cnts, _) = cv2.findContours(edged,
                                cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

c = max(cnts, key = cv2.contourArea)

M = cv2.moments(c)
    # From moment we can calculte area, centroid etc
    # The center or centroid can be calculated as follows
if M['m00'] > 0:
    cX = int(M['m10'] / M['m00'])
    cY = int(M['m01'] / M['m00'])

    # call detectShape for contour c
    shape = detectShape(c)
    print(shape)
    # Outline the contours
    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)

    # Write the name of shape on the center of shapes
    cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (255, 255, 255), 2)

'''
for c in cnts:
    # compute the moment of contour
    M = cv2.moments(c)
    # From moment we can calculte area, centroid etc
    # The center or centroid can be calculated as follows
    if M['m00'] > 0:
        cX = int(M['m10'] / M['m00'])
        cY = int(M['m01'] / M['m00'])
    
        # call detectShape for contour c
        shape = detectShape(c)
        print(shape)
        # Outline the contours
        cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
    
        # Write the name of shape on the center of shapes
        cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (255, 255, 255), 2)
'''
# show the output image
#cv2.imshow("Image", image)

#cv2.waitKey(0)
#cv2.destroyAllWindows()