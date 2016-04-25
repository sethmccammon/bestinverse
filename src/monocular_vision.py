import cv2
import numpy as np
from vision_utils import getFrame, findCircleMask, findFish
from utils import dist
import math


ramp_pts = []

def main(): 
  calibrateVision()
  cap = cv2.VideoCapture(1)
  frame = getFrame(cap)
  circle_mask = findCircleMask(frame)

  while cap.isOpened():
    frame = getFrame(cap)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_and(gray, circle_mask)
    cv2.imshow("Gray", gray)


    for pt in ramp_pts:
      cv2.circle(frame, pt, 2, (255, 255, 0), 2)
    

    fish_contours = findFish(frame, circle_mask)
    filtered_fish_contours = filterFish(fish_contours)


    for ii in range(0, len(filtered_fish_contours)):
      filtered_fish_contours[ii] = cv2.convexHull(filtered_fish_contours[ii])

      (x,y),radius = cv2.minEnclosingCircle(filtered_fish_contours[ii])
      center = (int(x),int(y))
      radius = int(radius)
      cv2.circle(frame,center,radius,(0,255,0),2)


      for ramp_pt in ramp_pts:
        if dist(ramp_pt, center) < radius:
          cv2.circle(frame,center,radius,(0,255,0),2)
          break
      else:
        cv2.circle(frame,center,radius,(0,0,255),2)
      # for ramp_pt in ramp_pts:
      #   if inRect(ramp_pt, (x,y), (x+w,y+h)):
      #     cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
      #     break
      # else:
      #   cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)


    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
      break



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



def inRect(query, p1, p2):
  if query[0] in range(p1[0], p2[0]) and query[1] in range(p1[1], p2[1]):
    return True
  else:
    return False



def calibrateVision():
  global ramp_pts


  cap = cv2.VideoCapture(1)
  cv2.namedWindow("Frame")
  cv2.setMouseCallback("Frame", getPixelLoc)

  while cap.isOpened():
    frame = getFrame(cap)
    cv2.imshow("Frame", frame)

    if len(ramp_pts) > 7:
      cv2.setMouseCallback("Frame", nullCallback)
      break

    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

  cap.release()
  cv2.destroyAllWindows()

  print "Calibration Complete"
  raw_input()


def nullCallback(event, x, y, flags, param):
  None


def getPixelLoc(event, x, y, flags, param):
  global ramp_pts
  if event == cv2.EVENT_LBUTTONDOWN:
    print "Left Image:", x, y
    ramp_pts.append((x,y))
    # return [x, y]
  # cv2.setMouseCallback("image", click_and_crop)

def getLargestContour(contours):
  max_area = -1
  for cnt in contours:        
    area = cv2.contourArea(cnt)
    if area > max_area:
      max_area = area
      max_contour = cnt

  return max_contour


def calcCircleTransform(ellipse):

  angle = ellipse[2]
  size = ellipse[1]
  center = ellipse[0]


  center = tuple([int(x) for x in center])
  size = tuple([int(x) for x in size])

  print "angle", angle
  print "center", center
  print "size", size


  # angle = angle*math.pi/180

  T_scale = getScaleMat(float(size[0])/875, float(size[1])/875)
  T_rot = cv2.getRotationMatrix2D((875/2, 875/2),angle,1.0)
  T_rot = np.vstack((T_rot, np.array([0, 0, 1])))
  T_trans = getTranslateMat(center[0], center[1])
  # T = np.array([[.112, 0, 0], [0, .208, 0], [0, 0, 1]], dtype='float32')
  T = np.dot(T_rot, T_scale) 
  # T = np.dot(T_rot, T)

  # T = np.dot(T, T_scale)
  return T


def getScaleMat(scaleX, scaleY):
  T = np.array([[scaleX, 0, 0], [0, scaleY, 0], [0, 0, 1]], dtype='float32')
  return T

def getRotMat(theta):
  theta = theta * math.pi / 180
  print theta
  T = np.array([[math.cos(theta), -math.sin(theta), 0], [math.sin(theta), math.cos(theta), 0], [0, 0, 1]], dtype='float32')
  return T


def getTranslateMat(movX, movY):
  T = np.array([[1, 0, movX], [0, 1, movY], [0, 0, 1]], dtype='float32')
  return T


if __name__ == "__main__":
  main()