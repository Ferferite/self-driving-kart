#------------→X(width)
#|0,0
#|
#|    (x,y)
#|
#↓Y(height)
import cv2
import numpy as np

def empty(a):
    pass
def exitapp(a):
    exit()

minLineLenght = 5
maxLineGap = 10
cv2.namedWindow('options')
cv2.resizeWindow('options', 740,340)
cv2.createTrackbar('Hue min', 'options', 0, 179, empty)#name, window name, min value, max value, function
cv2.createTrackbar('Hue max', 'options', 179, 179, empty)
cv2.createTrackbar('Saturation min', 'options', 0, 255, empty)
cv2.createTrackbar('Saturation max', 'options', 255, 255, empty)
cv2.createTrackbar('Value min', 'options', 0, 255, empty)
cv2.createTrackbar('Value max', 'options', 255, 255, empty)
cv2.createTrackbar('Close', 'options', 0, 1, exitapp)
cap = cv2.VideoCapture('testroad.png')
while True:
    #succes, img = cap.read()
    img = cv2.imread('test_image.png')
    imgresized = cv2.resize(img, (640, 480))
    imgblur = cv2.GaussianBlur(imgresized,(9,9),0)
    imgHSV = cv2.cvtColor(imgblur, cv2.COLOR_BGR2HSV)
    h_min = cv2.getTrackbarPos('Hue min', 'options')
    h_max = cv2.getTrackbarPos('Hue max', 'options')
    s_min = cv2.getTrackbarPos('Saturation min', 'options')
    s_max = cv2.getTrackbarPos('Saturation max', 'options')
    v_min = cv2.getTrackbarPos('Value min', 'options')
    v_max = cv2.getTrackbarPos('Value max', 'options')
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(imgHSV, lower, upper)
    imgResult = cv2.bitwise_and(imgblur,imgblur,mask=mask)
    imgcanny = cv2.Canny(imgResult, 200, 200)
    lines = cv2.HoughLinesP(imgcanny, 1, np.pi/180, 10, minLineLenght, maxLineGap)
    for x in range(0, len(lines)):
        for x1, y1, x2, y2 in lines[x]:
            cv2.line(imgResult, (x1, y1), (x2, y2), (0, 0, 255), 2)
    HorStack = np.hstack((imgresized,imgResult,imgHSV))
    cv2.imshow('Original + Final img + HSV filter', HorStack)
    cv2.imshow('test', imgcanny)
    cv2.waitKey(1)