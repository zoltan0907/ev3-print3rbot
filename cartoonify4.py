import cv2
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", type=int,
                        help="use this svg", required = True)
args = parser.parse_args()

cap = cv2.VideoCapture(args.file)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

def auto_canny(image, sigma=0.33):
	# compute the median of the single channel pixel intensities
	v = np.median(image)
	# apply automatic Canny edge detection using the computed median
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)
	# return the edged image
	return edged

kernel = np.ones((2,2),np.uint8)

while True:
    ret, image = cap.read()
    cartoon_image1, cartoon_image2  = cv2.pencilSketch(image, sigma_s=30, sigma_r=0.5, shade_factor=0.02)

    #cv2.imshow('image', get_edge)
    cv2.imshow('image', cartoon_image2)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
