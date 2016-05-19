import cv2
from vision_utils import getFrame
from utils import dist
import numpy as np


ramp_pts = []
robot_pts = []


def nullCallback(event, x, y, flags, param):
  None


def getRampPixelLoc(event, x, y, flags, param):
  global ramp_pts
  if event == cv2.EVENT_LBUTTONDOWN:
    print "Ramp Pixel:", x, y
    ramp_pts.append((x,y))

def getRobotPixelLoc(event, x, y, flags, param):
  global robot_pts
  if event == cv2.EVENT_LBUTTONDOWN:
    print "Robot Pixel:", x, y
    robot_pts.append((x,y))

def calibrateRamps(cap):
  global ramp_pts


  # cap = cv2.VideoCapture(1)
  cv2.namedWindow("Frame")
  cv2.setMouseCallback("Frame", getRampPixelLoc)

  while cap.isOpened():

    frame = getFrame(cap)
    for pt in ramp_pts:
      cv2.circle(frame, pt, 2, (255, 255, 0), 2)
    cv2.imshow("Frame", frame)

    if len(ramp_pts) > 7:
      cv2.setMouseCallback("Frame", nullCallback)
      break

    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

  # cap.release()
  # cv2.destroyAllWindows()

  print "Ramp Calibration Complete"
  return ramp_pts


def calibrateBoard(cap):
  global robot_pts
  calib_dist = 7.875

  # cap = cv2.VideoCapture(1)
  cv2.setMouseCallback("Frame", getRobotPixelLoc)

  while cap.isOpened():

    frame = getFrame(cap)
    for pt in robot_pts:
      cv2.circle(frame, pt, 2, (255, 0, 255), 2)
    cv2.imshow("Frame", frame)

    if len(robot_pts) >= 2:
      cv2.setMouseCallback("Frame", nullCallback)
      break

    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

  pt_dist = dist(robot_pts[1], robot_pts[0])
  pixel_len = calib_dist/pt_dist
  return pixel_len, robot_pts


def filterFish(fish_contours):
  centers = []
  radii = []

  margin = .25

  for ii in range(0, len(fish_contours)):
    fish_contours[ii] = cv2.convexHull(fish_contours[ii])

    (x,y),radius = cv2.minEnclosingCircle(fish_contours[ii])
    centers.append((int(x),int(y)))
    radii.append(int(radius))
    
  med_radius = np.median(radii)

  final_contours = []
  for ii in range(0, len(fish_contours)):
    if (radii[ii] < med_radius * (1+margin)) and (radii[ii] > med_radius * (1-margin)):
      final_contours.append(fish_contours[ii])

  return final_contours