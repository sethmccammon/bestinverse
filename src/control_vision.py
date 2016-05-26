#Control_vision.py is the display function for the computer vision.  
import cv2
from serialcomm import serialComm, buildMsg
from vision import calibrateRamps, calibrateBoard, filterFish
from vision_utils import getFrame, findCircleMask, findFish, makeCircleMask, pixel2in
from utils import dist
import numpy as np
import random



def main():
  cap = cv2.VideoCapture(1)
  pixel_len, robot_pts = calibrateBoard(cap)
  frame = getFrame(cap)
  height, width = frame.shape[:2]
  circle_mask, mask_center, mask_radius = makeCircleMask(frame, robot_pts)
  cv2.destroyAllWindows()

  while cap.isOpened():
    frame = getFrame(cap)
    frame = cv2.bitwise_and(frame, circle_mask)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_circle_mask = cv2.cvtColor(circle_mask, cv2.COLOR_BGR2GRAY)
    img_mean, img_std_dev = cv2.meanStdDev(gray, mask=gray_circle_mask)

    circles = cv2.HoughCircles(gray,cv2.cv.CV_HOUGH_GRADIENT,1, minDist=50, param1=50,param2=30,minRadius=20,maxRadius=40)

    if circles is not None:
      circles = np.uint16(np.around(circles))
      for circle_num, i in enumerate(circles[0,:]):
        center = (i[0], i[1])
        radius = i[2]

        fish_mask = np.zeros(frame.shape, np.uint8)
        #cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),2)
        #cv2.circle(frame,(i[0],i[1]),2,(0,0,255),3)

        cv2.circle(fish_mask, center, radius, (255, 255, 255),-1)
        fish_mask = cv2.cvtColor(fish_mask, cv2.COLOR_BGR2GRAY)
        fish_mean, fish_std_dev = cv2.meanStdDev(hsv, mask=fish_mask)
        if (fish_mean[0][0] < 95) or (fish_mean[0][0] > 120):
          cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),2)
          cv2.circle(frame,(i[0],i[1]),2,(0,0,255),3)



    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break



if __name__ == "__main__":
  main()