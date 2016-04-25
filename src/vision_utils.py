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
  return frame
  #return cv2.pyrDown(frame)

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

def drawMatches(img1, kp1, img2, kp2, matches):
  """
  My own implementation of cv2.drawMatches as OpenCV 2.4.9
  does not have this function available but it's supported in
  OpenCV 3.0.0

  This function takes in two images with their associated 
  keypoints, as well as a list of DMatch data structure (matches) 
  that contains which keypoints matched in which images.

  An image will be produced where a montage is shown with
  the first image followed by the second image beside it.

  Keypoints are delineated with circles, while lines are connected
  between matching keypoints.

  img1,img2 - Grayscale images
  kp1,kp2 - Detected list of keypoints through any of the OpenCV keypoint 
            detection algorithms
  matches - A list of matches of corresponding keypoints through any
            OpenCV keypoint matching algorithm
  """

  # Create a new output image that concatenates the two images together
  # (a.k.a) a montage
  rows1 = img1.shape[0]
  cols1 = img1.shape[1]
  rows2 = img2.shape[0]
  cols2 = img2.shape[1]

  out = np.zeros((max([rows1,rows2]),cols1+cols2,3), dtype='uint8')

  # Place the first image to the left
  out[:rows1,:cols1,:] = np.dstack([img1, img1, img1])

  # Place the next image to the right of it
  out[:rows2,cols1:cols1+cols2,:] = np.dstack([img2, img2, img2])

  # For each pair of points we have between both images
  # draw circles, then connect a line between them
  for mat in matches:

    # Get the matching keypoints for each of the images
    img1_idx = mat.queryIdx
    img2_idx = mat.trainIdx

    # x - columns
    # y - rows
    (x1,y1) = kp1[img1_idx].pt
    (x2,y2) = kp2[img2_idx].pt

    # Draw a small circle at both co-ordinates
    # radius 4
    # colour blue
    # thickness = 1
    cv2.circle(out, (int(x1),int(y1)), 4, (255, 0, 0), 1)   
    cv2.circle(out, (int(x2)+cols1,int(y2)), 4, (255, 0, 0), 1)

    # Draw a line in between the two points
    # thickness = 1
    # colour blue
    cv2.line(out, (int(x1),int(y1)), (int(x2)+cols1,int(y2)), (255, 0, 0), 1)


  # Show the image
  return out

def findFish(frame, circle_mask):
  kernel = np.ones((3,3),np.uint8)
  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


  color_mask = maskBlue(hsv)
  color_mask = cv2.bitwise_and(color_mask, circle_mask)
  color_mask = cv2.bitwise_or(color_mask, cv2.bitwise_not(circle_mask))
  color_mask = cv2.bitwise_not(color_mask)
  color_mask = cv2.morphologyEx(color_mask, cv2.MORPH_OPEN, kernel)
  color_mask = cv2.GaussianBlur(color_mask, (3, 3), 0)



  canny_frame = autoCanny(color_mask, .2)
  canny_frame = cv2.bitwise_and(circle_mask, canny_frame)
  contours, hierarchy = cv2.findContours(canny_frame,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

  fish_contours = []
  min_area = 250
  for cnt in contours:
    hull = cv2.convexHull(cnt)
    area = cv2.contourArea(hull)
    if (area > min_area):
     
      fish_contours.append(hull)

  return fish_contours