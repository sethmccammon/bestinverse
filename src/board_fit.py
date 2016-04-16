import cv2
import numpy as np
from vision_utils import getFrame, autoCanny, findCircleMask, maskBlue, drawMatches



def main():
  
  #From Video
  #cap = cv2.VideoCapture('../data/sample2.mp4')

  board_template = cv2.imread('../data/board_template_with_stickers.jpg')
  board_template = cv2.pyrDown(board_template)

  board_template = cv2.cvtColor(board_template, cv2.COLOR_BGR2GRAY)
  [val, board_template] = cv2.threshold(board_template, 125, 255, cv2.THRESH_BINARY)
  contours, hierarchy = cv2.findContours(board_template.copy(), cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
  true_centers = []
  for cnt in contours:
    M = cv2.moments(cnt)


    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    
    cv2.drawContours(board_template, [cnt], -1, [125, 125, 125], 2)
    # cv2.ellipse(frame,ell,(0,255,0),-1)
    # cv2.circle(frame, (cx, cy), 2, [255, 255, 255])
    true_centers.append((cx, cy))

  for center in true_centers:
    cv2.circle(board_template, center, 5, [125, 125, 125], -1)


  cv2.imshow("Template", board_template)
  #Webcam Support
  cap = cv2.VideoCapture(1)
  cap2 = cv2.VideoCapture(2)
  frame = getFrame(cap)

  circle_mask = findCircleMask(frame)

  frame2 = getFrame(cap2)
  circle_mask2 = findCircleMask(frame2)

  while cap.isOpened(): #and cap2.isOpened():
    frame = getFrame(cap)
    frame2 = getFrame(cap2)

    c1 = getCenters(frame, circle_mask)
    c2 = getCenters(frame2, circle_mask2)





    #frame = cv2.GaussianBlur(frame, (9, 9), 0)

    for center in c1:
      cv2.circle(frame, center, 5, [255, 255, 255], -1)

    for center in c2:
      cv2.circle(frame2, center, 5, [255, 255, 255], -1)




    # #print c1
    # for idx, pt in enumerate(c1):
    #   c1[idx] = [float(i) for i in pt]

    # for idx, pt in enumerate(true_centers):
    #   true_centers[idx] = [float(i) for i in pt]

    # #true_centers = [float(i) for i in true_centers]
    # print len(true_centers), len(c1)


    # src_pts = np.array(true_centers)
    # dst_pts = np.array(c1)

    # print src_pts.shape, dst_pts.shape

    # src_pts = uniqueRows(src_pts)
    # dst_pts = uniqueRows(dst_pts)

    # print src_pts.shape, dst_pts.shape


    # if len(src_pts) > len(dst_pts):
    #   print "Adding to dst_pts"
    #   for ii in range(0, len(src_pts)-len(dst_pts)):
    #     dst_pts = np.vstack((dst_pts, np.array([0,0])))
    # else:
    #   print "adding to src_pts"
    #   for ii in range(0, len(dst_pts)-len(src_pts)):
    #     src_pts = np.vstack((src_pts, np.array([0,0])))

    # print src_pts.shape, dst_pts.shape

    # # print type(src_pts), type(src_pts[0]), type(src_pts[0][0])
    # # print "------------------------------"
    # # print type(dst_pts), type(dst_pts[0]), type(dst_pts[0][0])


    # #src_pts = np.array([[141.0, 131.0], [480.0, 159.0], [493.0, 630.0], [64.0, 601.0]])
    # #dst_pts = np.array([[318.0, 256.0], [534.0, 372.0], [316.0, 670.0], [73.0, 473.0]])


    # transform, homography_mask = cv2.findHomography(src_pts, dst_pts, cv2.cv.CV_RANSAC, 0)
    # #transform, homography_mask = cv2.findHomography(true_centers, c1, cv2.cv.CV_RANSAC)
    # img = cv2.warpPerspective(board_template, transform, frame.shape[:2])










    cv2.imshow("Frame", frame)
    cv2.imshow("Frame2", frame2)
    #cv2.imshow("Transformed", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

def uniqueRows(a):
    a = np.ascontiguousarray(a)
    unique_a = np.unique(a.view([('', a.dtype)]*a.shape[1]))
    return unique_a.view(a.dtype).reshape((unique_a.shape[0], a.shape[1]))


def getCenters(frame, circle_mask):
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
  #canny_frame = cv2.GaussianBlur(canny_frame, (3, 3), 0)
  contours, hierarchy = cv2.findContours(canny_frame,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

  fish_contours = []
  fish_ell = []
  min_area = 250
  for cnt in contours:
    area = cv2.contourArea(cnt)
    if (area > min_area): #and cv2.isContourConvex(cnt):
     
      fish_contours.append(cnt)
      ell = cv2.fitEllipse(cnt)
      fish_ell.append(ell)
  centers = []
  for ii, cnt in enumerate(fish_contours):
    M = cv2.moments(cnt)
    ell = fish_ell[ii]

    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    
    #cv2.drawContours(frame, [cnt], -1, [255, 255, 255], -1)
    # cv2.ellipse(frame,ell,(0,255,0),-1)
    # cv2.circle(frame, (cx, cy), 2, [255, 255, 255])
    centers.append((cx, cy))

  return centers



if __name__ == "__main__":
  main()