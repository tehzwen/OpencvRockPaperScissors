import cv2
import numpy as np
cap = cv2.VideoCapture(0)
while(cap.isOpened()):
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    ret, thresh1 = cv2.threshold(blur, 127, 255, 0)

    contours = cv2.findContours(thresh1, 1, 2)

    max_area = 0
    #img = cv2.drawContours(img, contours, 3, (0,255,0), 3)

    cnt = contours[0]

    M = cv2.moments(cnt)
    #print (M)

    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])

    #print (cx)

    cv2.imshow('cnt', cnt)
    cv2.imshow('thresh', thresh1)

    k = cv2.waitKey(10)
    if k == 27:
        break
