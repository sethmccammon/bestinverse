#Control.py is the unified control program for the robot.  
import cv2
from serialcomm import serialComm
from vision import calibrateRamps, calibrateRobot, filterFish
from vision_utils import getFrame, findCircleMask, findFish
from utils import dist


def main():
  #initialize Vision
  cap = cv2.VideoCapture(1)
  ramp_pts = calibrateRamps(cap)
  pixel_len = calibrateRobot(cap)
  cv2.destroyAllWindows()

  print "Pixel Length:", pixel_len


  #initialize Comms
  comm = serialComm()
  comm.valid = True
  if not comm.valid:
    print "No Comm - Exiting"
    return 0
  else:
    frame = getFrame(cap)
    height, width = frame.shape[:2]
    circle_mask = findCircleMask(frame)
    while cap.isOpened():
      # print "foo"
      frame = getFrame(cap)
      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      gray = cv2.bitwise_and(gray, circle_mask)
      cv2.imshow("Frame", gray)

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

      if cv2.waitKey(1) & 0xFF == ord('q'):
        break






if __name__ == "__main__":
  main()
