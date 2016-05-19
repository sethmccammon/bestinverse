#Control.py is the unified control program for the robot.  
import cv2
from serialcomm import serialComm, buildMsg
from vision import calibrateRamps, calibrateBoard, filterFish
from vision_utils import getFrame, findCircleMask, findFish, makeCircleMask
from utils import dist
import numpy as np








def main():
  #initialize Vision
  cap = cv2.VideoCapture(1)
  ramp_pts = calibrateRamps(cap)
  pixel_len, robot_pts = calibrateBoard(cap)
  cv2.destroyAllWindows()




  print "Pixel Length:", pixel_len


  #initialize Comms
  comm = serialComm("dummy_port")

  calibrateRobot(comm)

  if not comm.valid:
    print "No Comm - Exiting"
    return 0
  else:
    frame = getFrame(cap)
    height, width = frame.shape[:2]
    circle_mask, mask_center, mask_radius = makeCircleMask(frame, robot_pts)
    # circle_mask = findCircleMask(frame)


    # while True:
    #   #GOTO ramp location
    #   #Wait for fish
    #   #Grab Fish
    #   #Deposit Fish



    while cap.isOpened():
      frame = getFrame(cap)
      frame = cv2.bitwise_and(frame, circle_mask)
      
      #crop image
      # c1 = (mask_center[0]-mask_radius,mask_center[1]-mask_radius)
      # c2 = (mask_center[0]+mask_radius,mask_center[1]+mask_radius)
      # frame = frame[c1[0]:c2[0], c1[1]:c2[1]]
      # circle_mask = circle_mask[c1[0]:c2[0], c1[1]:c2[1]]


      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      gray_circle_mask = cv2.cvtColor(circle_mask, cv2.COLOR_BGR2GRAY)
      img_mean, img_std_dev = cv2.meanStdDev(gray, mask=gray_circle_mask)
      #print img_mean

      circles = cv2.HoughCircles(gray,cv2.cv.CV_HOUGH_GRADIENT,1, minDist=50, param1=50,param2=30,minRadius=20,maxRadius=40)

      if circles is not None:
      # print circles.size
        circles = np.uint16(np.around(circles))
        for circle_num, i in enumerate(circles[0,:]):
          fish_mask = np.zeros(frame.shape, np.uint8)


          cv2.circle(fish_mask, (i[0], i[1]), i[2], (255, 255, 255),-1)
          fish_mask = cv2.cvtColor(fish_mask, cv2.COLOR_BGR2GRAY)
          # c1 = (i[0],i[1]-i[2])
          # c2 = (i[0],i[1]+i[2])
          # fish_mask, fish_mask_center, fish_mask_radius = makeCircleMask(frame, (c1, c2))
          #cv2.imshow("fish_mask",fish_mask)
          # fish_mask = cv2.cvtColor(fish_mask, cv2.COLOR_BGR2GRAY)
          fish_mean, fish_std_dev = cv2.meanStdDev(gray, mask=fish_mask) 
          #print type(fish_mean[0][0])
          if fish_mean[0][0] > img_mean[0][0]*.55:

            # if fis
            # draw the outer circle
            cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            cv2.circle(frame,(i[0],i[1]),2,(0,0,255),3)






      # for pt in ramp_pts:
      #   cv2.circle(frame, pt, 2, (255, 255, 0), 2)
      

      # fish_contours = findFish(frame, circle_mask)
      # filtered_fish_contours = filterFish(fish_contours)


      # for ii in range(0, len(filtered_fish_contours)):
      #   filtered_fish_contours[ii] = cv2.convexHull(filtered_fish_contours[ii])

      #   (x,y),radius = cv2.minEnclosingCircle(filtered_fish_contours[ii])
      #   center = (int(x),int(y))
      #   radius = int(radius)
      #   cv2.circle(frame,center,radius,(0,255,0),2)


      #   for ramp_pt in ramp_pts:
      #     if dist(ramp_pt, center) < radius*.75:
      #       cv2.circle(frame,center,radius,(0,255,0),2)
      #       break
      #   else:
      #     cv2.circle(frame,center,radius,(0,0,255),2)

      cv2.imshow("Frame", frame)
      if cv2.waitKey(1) & 0xFF == ord('q'):
        break





def calibrateRobot(comm):
  msg = buildMsg(1)
  print "Message",msg
  comm.sendPacket(msg)
  return 0



if __name__ == "__main__":
  main()
