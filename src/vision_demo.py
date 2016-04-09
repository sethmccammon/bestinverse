from vision import maskRed, maskBlue, maskGreen, maskYellow
from serialcomm import serialComm
import operator
import cv2
import struct

def demo():
  #Webcam Support
  cap = cv2.VideoCapture(0)
  ret, frame = cap.read()
  frame = cv2.pyrDown(cv2.pyrDown(frame))
  height, width = frame.shape[:2]
  img_ctr = (width/2, height/2)

  comm = serialComm()

  while cap.isOpened():
    ret, frame = cap.read()
    frame = cv2.pyrDown(cv2.pyrDown(frame))
    frame = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    color_mask = maskBlue(hsv)
    area_bounds = [200, 1000]
    contours, hierarchy = cv2.findContours(color_mask.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


    cv2.imshow('Red Mask', color_mask)
    
    if contours:
      max_area = -1
      for cnt in contours:
        if cv2.contourArea(cnt) > max_area:
          max_area = cv2.contourArea(cnt)
          max_cnt = cnt

      
      x,y,w,h = cv2.boundingRect(max_cnt)
      cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

      ctr = (x+(w/2), y+(h/2))
      cv2.circle(frame, ctr, 5, (0,0,0),2)
      diff = map(operator.sub, img_ctr, ctr)
      print diff
      msg = struct.pack('!b', -diff[1])
      msg = msg + "$" +struct.pack('!b', diff[0])

      comm.sendPacket(msg)
      
    cv2.imshow('Object_Id', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
      break


if __name__ == "__main__":
  demo()
