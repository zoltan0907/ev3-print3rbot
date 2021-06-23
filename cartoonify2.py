import cv2
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", type=str,
                        help="use this svg", required = True)
args = parser.parse_args()

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

original_image = cv2.imread(args.file)
original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
grayscale_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
smooth_grayscale_image = cv2.medianBlur(grayscale_image, 5)
#get_edge = cv2.adaptiveThreshold(smooth_grayscale_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, 3)
get_edge = auto_canny(smooth_grayscale_image)
#get_edge = cv2.Canny(smooth_grayscale_image, 10, 200)
#get_edge = cv2.Canny(smooth_grayscale_image, 255, 250)
get_edge = cv2.morphologyEx(get_edge, cv2.MORPH_GRADIENT, kernel)
get_edge = cv2.dilate(get_edge, kernel, iterations = 5)
get_edge = cv2.bitwise_not(get_edge)
contours, hierarchy = cv2.findContours(get_edge, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(original_image, contours, -1, (0,255,0), 3)
#color_image = cv2.bilateralFilter(original_image, 9, 300, 300)
#cartoon_image = cv2.bitwise_and(color_image, color_image, mask=get_edge)

cv2.imshow('image', get_edge)

while cv2.waitKey(1) & 0xFF != 27:
    pass

cv2.destroyAllWindows()
