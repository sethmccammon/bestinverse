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

  

  cap = cv2.VideoCapture('../data/sample2.mp4')

  ret, frame = cap.read()

  frame = cv2.pyrDown(cv2.pyrDown(frame))

  height, width = frame.shape[:2]
  ff_mask = np.zeros((height+2,width+2),np.uint8)

  #Blue
  blue_lower_bound = np.array([95,0,0], np.uint8)
  blue_upper_bound = np.array([105,255,255], np.uint8)

  #Yellow
  yellow_lower_bound = np.array([20,0,0], np.uint8)
  yellow_upper_bound = np.array([30,255,255], np.uint8)

  #green
  green_lower_bound = np.array([65,0,0], np.uint8)
  green_upper_bound = np.array([80,255,255], np.uint8)

  #Red/Orange
  red_lower_bound_1 = np.array([175,0,0], np.uint8)
  red_upper_bound_1 = np.array([180,255,255], np.uint8)

  red_lower_bound_2 = np.array([0,0,0], np.uint8)
  red_upper_bound_2 = np.array([10,255,255], np.uint8)

  while(cap.isOpened()):
      ret, frame = cap.read()

      frame = cv2.pyrDown(cv2.pyrDown(frame))
      #frame = cv2.GaussianBlur(frame, (11, 11), 0)

      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)




      # Threshold the HSV image to get only blue colors
      # yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
      # red_mask = cv2.inRange(hsv, lower_red, upper_red)


      green_mask = cv2.inRange(hsv, green_lower_bound, green_upper_bound)
      yellow_mask = cv2.inRange(hsv, yellow_lower_bound, yellow_upper_bound)

      blue_mask = cv2.inRange(hsv, blue_lower_bound, blue_upper_bound)


      mask_1 = cv2.inRange(hsv, red_lower_bound_1, red_upper_bound_1)
      mask_2 = cv2.inRange(hsv, red_lower_bound_2, red_upper_bound_2)

      red_mask = cv2.bitwise_or(mask_2, mask_1)


      red_mask = morphology(red_mask)
      green_mask = morphology(green_mask)
      yellow_mask = morphology(yellow_mask)



      contours, hierarchy = cv2.findContours(blue_mask.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


      max_area = 0

      for cnt in contours:        
        area = cv2.contourArea(cnt)
        if area > max_area:
          max_area = area
          max_contour = cnt

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
      #cv2.imshow('Red', diff)



      if cv2.waitKey(1) & 0xFF == ord('q'):
          break

  cap.release()
  cv2.destroyAllWindows()



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