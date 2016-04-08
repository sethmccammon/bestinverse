import cv2
import numpy as np

#HSV Table
#red Fish     2, 91, 96
#OJ Fish      19, 94, 100
#Yaller Fish  49, 100, 99
#Green Fish   128, 98, 46
#Blue Fish    195 89, 73
#Background   199 82 82

def main():

  
  #From Video
  cap = cv2.VideoCapture('../data/sample2.mp4')

  #Webcam Support
  #cap = cv2.VideoCapture(1)
  

  ret, frame = cap.read()
  frame = cv2.pyrDown(cv2.pyrDown(frame))



  height, width = frame.shape[:2]

  video = cv2.VideoWriter('vision_demo.avi', cv2.cv.CV_FOURCC(*'XVID'),30,(width,height))
  print "Video Open:", video.isOpened()


  ff_mask = np.zeros((height+2,width+2),np.uint8)

  while(cap.isOpened()):
      ret, frame = cap.read()



      frame = cv2.pyrDown(cv2.pyrDown(frame))
      #frame = cv2.GaussianBlur(frame, (11, 11), 0)


      cv2.imshow("Live", frame)
      
      hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

      red_mask = maskRed(hsv)
      blue_mask = maskBlue(hsv)
      green_mask = maskGreen(hsv)
      yellow_mask = maskYellow(hsv)

      contours, hierarchy = cv2.findContours(blue_mask.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


      max_area = 0
      max_contour = False
      for cnt in contours:        
        area = cv2.contourArea(cnt)
        if area > max_area:
          max_area = area
          max_contour = cnt


      if contours:
        hull = cv2.convexHull(max_contour)
        circle_mask = np.zeros(red_mask.shape, np.uint8)
        cv2.drawContours(circle_mask, [hull],-1, 255,-1)



        final_mask_a = cv2.bitwise_and(circle_mask, red_mask)
        final_mask_b = cv2.bitwise_and(circle_mask, green_mask)
        final_mask_c = cv2.bitwise_and(circle_mask, yellow_mask)


        area_bounds = [200, 1000]
        fish_contours = []

        contours, hierarchy = cv2.findContours(final_mask_a.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:        
          area = cv2.contourArea(cnt)
          if (area > area_bounds[0]) and (area < area_bounds[1]):
            fish_contours.append(cnt)

        contours, hierarchy = cv2.findContours(final_mask_b.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:        
          area = cv2.contourArea(cnt)
          if (area > area_bounds[0]) and (area < area_bounds[1]):
            fish_contours.append(cnt)
        
        contours, hierarchy = cv2.findContours(final_mask_c.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:        
          area = cv2.contourArea(cnt)
          if (area > area_bounds[0]) and (area < area_bounds[1]):
            fish_contours.append(cnt)


        for ii in range(0, len(fish_contours)):
          fish_contours[ii] = cv2.convexHull(fish_contours[ii])
          x,y,w,h = cv2.boundingRect(fish_contours[ii])
          cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)


        final_mask = cv2.bitwise_or(cv2.bitwise_or(final_mask_a, final_mask_b), final_mask_c)

        final_mask = morphology(final_mask)

        diff = cv2.subtract(yellow_mask, circle_mask)

        cv2.imshow('Frame', frame)
        cv2.imshow('Red', diff)
        video.write(frame)

      if cv2.waitKey(1) & 0xFF == ord('q'):
          break

  cap.release()
  video.release()
  cv2.destroyAllWindows()






def maskRed(img_in):
  red_lower_bound_1 = np.array([175,0,0], np.uint8)
  red_upper_bound_1 = np.array([180,255,255], np.uint8)

  red_lower_bound_2 = np.array([0,0,0], np.uint8)
  red_upper_bound_2 = np.array([10,255,255], np.uint8)

  mask_1 = cv2.inRange(img_in, red_lower_bound_1, red_upper_bound_1)
  mask_2 = cv2.inRange(img_in, red_lower_bound_2, red_upper_bound_2)

  red_mask = cv2.bitwise_or(mask_2, mask_1)
  return red_mask

def maskBlue(img_in):
  blue_lower_bound = np.array([105,0,0], np.uint8)
  blue_upper_bound = np.array([115,255,255], np.uint8)

  blue_mask = cv2.inRange(img_in, blue_lower_bound, blue_upper_bound)
  #return morphology(blue_mask)
  return blue_mask

def maskGreen(img_in):
  green_lower_bound = np.array([65,0,0], np.uint8)
  green_upper_bound = np.array([80,255,255], np.uint8)
  green_mask = cv2.inRange(img_in, green_lower_bound, green_upper_bound)
  return morphology(green_mask)

def maskYellow(img_in):
  yellow_lower_bound = np.array([20,0,0], np.uint8)
  yellow_upper_bound = np.array([30,255,255], np.uint8)
  yellow_mask = cv2.inRange(img_in, yellow_lower_bound, yellow_upper_bound)
  return morphology(yellow_mask)

def auto_canny(image, sigma=0.1):
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

  return res


if __name__ == "__main__":
  main()