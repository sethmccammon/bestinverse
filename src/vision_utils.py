import cv2
import numpy as np

def autoCanny(image, sigma=0.5):
  # compute the median of the single channel pixel intensities
  v = np.median(image)
 
  # apply automatic Canny edge detection using the computed median
  lower = int(max(0, (1.0 - sigma) * v))
  upper = int(min(255, (1.0 + sigma) * v))
  edged = cv2.Canny(image, lower, upper)
 
  # return the edged image
  return edged  

def morphology(img):
  kernel = np.ones((3,3),np.uint8)
  # opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
  # closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

  closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
  res = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)


def maskRed(img_in):
  red_lower_bound_1 = np.array([175,50,50], np.uint8)
  red_upper_bound_1 = np.array([180,255,255], np.uint8)

  red_lower_bound_2 = np.array([0,50,50], np.uint8)
  red_upper_bound_2 = np.array([10,255,255], np.uint8)

  mask_1 = cv2.inRange(img_in, red_lower_bound_1, red_upper_bound_1)
  mask_2 = cv2.inRange(img_in, red_lower_bound_2, red_upper_bound_2)

  red_mask = cv2.bitwise_or(mask_2, mask_1)
  return red_mask

def maskBlue(img_in):
  blue_lower_bound = np.array([105,50,50], np.uint8)
  blue_upper_bound = np.array([115,255,255], np.uint8)

  blue_mask = cv2.inRange(img_in, blue_lower_bound, blue_upper_bound)
  #return morphology(blue_mask)
  return blue_mask

def maskGreen(img_in):
  green_lower_bound = np.array([65,50,50], np.uint8)
  green_upper_bound = np.array([80,255,255], np.uint8)
  green_mask = cv2.inRange(img_in, green_lower_bound, green_upper_bound)
  return morphology(green_mask)

def maskYellow(img_in):
  yellow_lower_bound = np.array([20,50,50], np.uint8)
  yellow_upper_bound = np.array([30,255,255], np.uint8)
  yellow_mask = cv2.inRange(img_in, yellow_lower_bound, yellow_upper_bound)
  return morphology(yellow_mask)

def getFrame(cap):
  ret, frame = cap.read()
  return cv2.pyrDown(frame)

def findCircleMask(frame):
  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
  color_mask = maskBlue(hsv)

  contours, hierarchy = cv2.findContours(color_mask.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


  max_area = 0
  max_contour = False
  for cnt in contours:        
    area = cv2.contourArea(cnt)
    if area > max_area:
      max_area = area
      max_contour = cnt


  if contours:
    hull = cv2.convexHull(max_contour)
    circle_mask = np.zeros(color_mask.shape, np.uint8)
    cv2.drawContours(circle_mask, [hull],-1, 255,-1)

  return circle_mask