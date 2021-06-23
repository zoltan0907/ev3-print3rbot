import cv2
#import matplotlib
import numpy as np
#import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", type=str,
                        help="use this svg", required = True)
args = parser.parse_args()

image = cv2.imread(args.file)
image = cv2.cvtColor(image, cv2.COLOR_BGR2YCR_CB)[...,0]

def getBordered(image, width):
    bg = np.zeros(image.shape)
    _, contours = cv2.findContours(image.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    biggest = 0
    bigcontour = None
    for contour in contours:
        area = cv2.contourArea(contour) 
        if area > biggest:
            biggest = area
            bigcontour = contour
    return cv2.drawContours(bg, [bigcontour], 0, (255, 255, 255), width).astype(bool) 

im2 = getBordered(image, 10)

cv2.imshow('image', im2)

while cv2.waitKey(1) & 0xFF != 27:
    pass

cv2.destroyAllWindows()
