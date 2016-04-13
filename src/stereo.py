
##THIS CODE IS PROBABLY BROKEN

# import cv2
# import numpy as np
# #from vision import findFish, maskRed, maskBlue, maskGreen, maskYellow

# def main():

  
#   #From Video
#   #cap = cv2.VideoCapture('../data/sample2.mp4')

#   #Webcam Support
#   cap = cv2.VideoCapture(1)
#   cap2 = cv2.VideoCapture(2)

#   ret, frame = cap.read()
#   ret2, frame2 = cap2.read()

#   frame = cv2.pyrDown(frame)
#   frame2 = cv2.pyrDown(frame2)

#   circle_mask = findCircleMask(frame)
#   circle_mask2 = findCircleMask(frame2)

#   while cap.isOpened() and cap2.isOpened():
#     frame = getFrame(cap)
#     frame2 = getFrame(cap2)

#     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#     hsv2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)

#     color_mask = maskBlue(hsv)
#     color_mask = cv2.bitwise_and(color_mask, circle_mask)
#     color_mask = cv2.bitwise_or(color_mask, cv2.bitwise_not(circle_mask))
#     color_mask = cv2.bitwise_not(color_mask)



#     color_mask2 = maskBlue(hsv2)
#     color_mask2 = cv2.bitwise_and(color_mask2, circle_mask2)
#     color_mask2 = cv2.bitwise_or(color_mask2, cv2.bitwise_not(circle_mask2))
#     color_mask2 = cv2.bitwise_not(color_mask2)





#     cv2.imshow("Frame", frame)
#     cv2.imshow("Frame2", frame2)

#     cv2.imshow("Fish", color_mask)
#     cv2.imshow("Fish 2", color_mask2)



#     if cv2.waitKey(1) & 0xFF == ord('q'):
#       break










# def maskBlue(img_in):
#   blue_lower_bound = np.array([105,50,50], np.uint8)
#   blue_upper_bound = np.array([115,255,255], np.uint8)

#   blue_mask = cv2.inRange(img_in, blue_lower_bound, blue_upper_bound)
#   #return morphology(blue_mask)
#   return blue_mask




# if __name__ == "__main__":
#   main()