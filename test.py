import cv2
import numpy as np
cap = cv2.VideoCapture(0)
while(cap.isOpened()):
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    ret, thresh1 = cv2.threshold(
        blur, 70, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    contours = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    drawing = np.zeros(img.shape, np.uint8)

    max_area = 0
    cv2.drawContours(img, contours, -1, (0,255,0), 3)


    cv2.imshow('input', img)

    k = cv2.waitKey(10)
    if k == 27:
        break
