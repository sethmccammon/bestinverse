import cv2
import numpy as np
from vision_utils import findCircleMask, getFrame, drawMatches



right_pts = []
left_pts = []


def main():
  calibrateStereo()
  # global left_pts
  # global right_pts

  # cv2.namedWindow("Left Frame")
  # cv2.namedWindow("Right Frame")
  # cv2.setMouseCallback("Left Frame", getLeftPixelLoc)
  # cv2.setMouseCallback("Right Frame", getRightPixelLoc)




  # min_matches = 10


  # max_matches = 40
  #From Video
  #cap = cv2.VideoCapture('../data/sample2.mp4')

  #Webcam Support
  # cap = cv2.VideoCapture(1)
  # cap2 = cv2.VideoCapture(2)


  # ret, frame = cap.read()
  # ret2, frame2 = cap2.read()

  # frame = cv2.pyrDown(frame)
  # frame2 = cv2.pyrDown(frame2)


  # gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  # gray_frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
  # img3 = drawMatches(gray_frame, [], gray_frame2, [],[])
  # height, width = img3.shape[:2]
  # print "height", height, "width", width

  # circle_mask = findCircleMask(frame)
  # circle_mask2 = findCircleMask(frame2)

  # orb = cv2.ORB()
  # bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)


  # video = cv2.VideoWriter('stereo_demo.avi', cv2.cv.CV_FOURCC(*'XVID'),30,(width,height))
  # print "Video Open:", video.isOpened()

  # while cap.isOpened() and cap2.isOpened():
  #   frame = getFrame(cap)
  #   frame2 = getFrame(cap2)
  #   cv2.imshow("Left Frame", frame)
  #   cv2.imshow("Right Frame", frame2)

  #   if len(left_pts) > 7:
  #     cv2.setMouseCallback("Left Frame", nullCallback)

  #   if len(right_pts) > 7:
  #     cv2.setMouseCallback("Right Frame", nullCallback)

  #   if (len(left_pts) > 7) and (len(right_pts) > 7):
  #     break

    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # masked_frame = cv2.bitwise_and(circle_mask, frame)
    # masked_frame2 = cv2.bitwise_and(circle_mask2, frame2)


    # img = cv2.imread('../data/image1.jpg')


    # kp1, des1 = orb.detectAndCompute(masked_frame, None)
    # kp2, des2 = orb.detectAndCompute(masked_frame2, None)

    # feature_frame = cv2.drawKeypoints(frame, kp1, color=(0,255,0), flags=0)
    # feature_frame2 = cv2.drawKeypoints(frame2, kp2, color=(0,255,0), flags=0)

    # # create BFMatcher object
    

    # # Match descriptors.
    # matches = bf.match(des1,des2)
    # matches = sorted(matches, key = lambda x:x.distance)


    # # print [ kp1[idx].pt for idx, m in enumerate(matches)]

    # if len(matches) > min_matches:
    #   matches = matches[:max_matches]
    #   src_pts = np.float32([ kp1[idx].pt for idx, m in enumerate(matches)]).reshape(-1,1,2)
    #   dst_pts = np.float32([ kp2[idx].pt for idx, m in enumerate(matches)]).reshape(-1,1,2)

      
    #   # print src_pts

    #   M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
    #   print type(M)
    #   frame3 = cv2.warpPerspective(frame, M, frame.shape[:2])
    #   # cv2.imshow("Frame3", frame3)
      


    # # gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # # gray_frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # # Draw first 10 matches.
    # img3 = drawMatches(frame, kp1, frame2, kp2, matches[:20])
    # video.write(img3)
    



    # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # hsv2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)

    # color_mask = maskBlue(hsv)
    # color_mask = cv2.bitwise_and(color_mask, circle_mask)
    # color_mask = cv2.bitwise_or(color_mask, cv2.bitwise_not(circle_mask))
    # color_mask = cv2.bitwise_not(color_mask)



    # color_mask2 = maskBlue(hsv2)
    # color_mask2 = cv2.bitwise_and(color_mask2, circle_mask2)
    # color_mask2 = cv2.bitwise_or(color_mask2, cv2.bitwise_not(circle_mask2))
    # color_mask2 = cv2.bitwise_not(color_mask2)





    # cv2.imshow("Frame", frame)
    # cv2.imshow("Frame2", frame2)




    # cv2.imshow("Features", feature_frame)
    # cv2.imshow("Features 2", feature_frame2)

    # cv2.imshow("Matches", img3)



    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #   break

  # cap.release()
  # # video.release()
  # cv2.destroyAllWindows()



def calibrateStereo():
  global left_pts
  global right_pts

  cv2.namedWindow("Left Frame")
  cv2.namedWindow("Right Frame")
  cv2.setMouseCallback("Left Frame", getLeftPixelLoc)
  cv2.setMouseCallback("Right Frame", getRightPixelLoc)


  cap = cv2.VideoCapture(1)
  cap2 = cv2.VideoCapture(2)


  while cap.isOpened() and cap2.isOpened():
    frame = getFrame(cap)
    frame2 = getFrame(cap2)
    cv2.imshow("Left Frame", frame)
    cv2.imshow("Right Frame", frame2)

    if len(left_pts) > 7:
      cv2.setMouseCallback("Left Frame", nullCallback)

    if len(right_pts) > 7:
      cv2.setMouseCallback("Right Frame", nullCallback)

    if (len(left_pts) > 7) and (len(right_pts) > 7):
      break

    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

  cap.release()
  cap2.release()
  cv2.destroyAllWindows()

  cap.release()
  cv2.destroyAllWindows()
  print "Calibration Complete"


def nullCallback(event, x, y, flags, param):
  None


def getLeftPixelLoc(event, x, y, flags, param):
  global left_pts
  if event == cv2.EVENT_LBUTTONDOWN:
    print "Left Image:", x, y
    left_pts.append([x,y])
    # return [x, y]
  # cv2.setMouseCallback("image", click_and_crop)


def getRightPixelLoc(event, x, y, flags, param):
  global right_pts
  if event == cv2.EVENT_LBUTTONDOWN:
    print "Right Image:", x, y
    right_pts.append([x,y])

if __name__ == "__main__":
  main()