import cv2
import numpy as np
from vision_utils import getFrame, findCircleMask
import math


def main():
  board_template = cv2.imread('../data/board_template.jpg')


  cap = cv2.VideoCapture(1)

  frame = getFrame(cap)
  height, width = board_template.shape[:2]
  print width, height

  circle_mask = findCircleMask(frame)
  contours, hierarchy = cv2.findContours(circle_mask.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


  max_contour = getLargestContour(contours)
  ellipse = cv2.fitEllipse(max_contour)
  T = calcCircleTransform(ellipse)
  print T
  while cap.isOpened():
    # cv2.imshow("temp", board_template)
    frame = getFrame(cap)
    cv2.ellipse(frame,ellipse,(0,255,0),2)
    # cv2.ellipse(frame,(center, size, 90), (255, 0, 2))
    # cv2.circle(frame, center, 2, (0,255,0))
    aug_frame = cv2.warpAffine(board_template, np.delete(T, 2, 0), (width, height))

    cv2.imshow("Aug Frame", aug_frame)

    cv2.imshow("Frame", frame)
    cv2.imshow("Circle Mask", circle_mask)




    if cv2.waitKey(1) & 0xFF == ord('q'):
      break




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