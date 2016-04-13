
##THIS CODE IS PROBABLY BROKEN

# import cv2
# import numpy as np

# #HSV Table
# #red Fish     2, 91, 96
# #OJ Fish      19, 94, 100
# #Yaller Fish  49, 100, 99
# #Green Fish   128, 98, 46
# #Blue Fish    195 89, 73
# #Background   199 82 82

# def main():

  
#   #From Video
#   cap = cv2.VideoCapture('../data/sample2.mp4')

#   #Webcam Support
#   #cap = cv2.VideoCapture(1)
  

#   ret, frame = cap.read()
#   frame = cv2.pyrDown(cv2.pyrDown(frame))



#   height, width = frame.shape[:2]

#   video = cv2.VideoWriter('vision_demo.avi', cv2.cv.CV_FOURCC(*'XVID'),30,(width,height))
#   print "Video Open:", video.isOpened()


#   ff_mask = np.zeros((height+2,width+2),np.uint8)

#   while(cap.isOpened()):
#       ret, frame = cap.read()



#       frame = cv2.pyrDown(cv2.pyrDown(frame))
#       #frame = cv2.GaussianBlur(frame, (11, 11), 0)


#       cv2.imshow("Live", frame)
      
#       hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

#       red_mask = maskRed(hsv)
#       blue_mask = maskBlue(hsv)
#       green_mask = maskGreen(hsv)
#       yellow_mask = maskYellow(hsv)

#       contours, hierarchy = cv2.findContours(blue_mask.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


#       max_area = 0
#       max_contour = False
#       for cnt in contours:        
#         area = cv2.contourArea(cnt)
#         if area > max_area:
#           max_area = area
#           max_contour = cnt


#       if contours:
#         hull = cv2.convexHull(max_contour)
#         circle_mask = np.zeros(red_mask.shape, np.uint8)
#         cv2.drawContours(circle_mask, [hull],-1, 255,-1)



#         final_mask_a = cv2.bitwise_and(circle_mask, red_mask)
#         final_mask_b = cv2.bitwise_and(circle_mask, green_mask)
#         final_mask_c = cv2.bitwise_and(circle_mask, yellow_mask)


#         area_bounds = [200, 1000]
#         fish_contours = []

#         contours, hierarchy = cv2.findContours(final_mask_a.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#         for cnt in contours:        
#           area = cv2.contourArea(cnt)
#           if (area > area_bounds[0]) and (area < area_bounds[1]):
#             fish_contours.append(cnt)

#         contours, hierarchy = cv2.findContours(final_mask_b.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#         for cnt in contours:        
#           area = cv2.contourArea(cnt)
#           if (area > area_bounds[0]) and (area < area_bounds[1]):
#             fish_contours.append(cnt)
        
#         contours, hierarchy = cv2.findContours(final_mask_c.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#         for cnt in contours:        
#           area = cv2.contourArea(cnt)
#           if (area > area_bounds[0]) and (area < area_bounds[1]):
#             fish_contours.append(cnt)


#         for ii in range(0, len(fish_contours)):
#           fish_contours[ii] = cv2.convexHull(fish_contours[ii])
#           x,y,w,h = cv2.boundingRect(fish_contours[ii])
#           cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)


#         final_mask = cv2.bitwise_or(cv2.bitwise_or(final_mask_a, final_mask_b), final_mask_c)

#         final_mask = morphology(final_mask)

#         diff = cv2.subtract(yellow_mask, circle_mask)

#         cv2.imshow('Frame', frame)
#         cv2.imshow('Red', diff)
#         video.write(frame)

#       if cv2.waitKey(1) & 0xFF == ord('q'):
#           break

#   cap.release()
#   video.release()
#   cv2.destroyAllWindows()




# if __name__ == "__main__":
#   main()