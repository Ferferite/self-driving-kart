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

h_max = 179
s_max = 130
previouslinecount = 0
linecount = 0
highlinecount = 0
highestvalue = 0
foundhmax = False

lines = 0
min_LineLenght = 10
maxLineGap = 5

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
    img = cv2.imread('testroad.png')
    imgresized = cv2.resize(img, (640, 480))
    imgblur = cv2.GaussianBlur(imgresized,(7,7),0)
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
    lines = cv2.HoughLinesP(imgcanny, 1, np.pi/180, 40 ,2, min_LineLenght, maxLineGap)#image,rtho,theta,threshhold,lines,minlinelenght,maxlinegap
    try:
        for x in range(0, len(lines)):
            for x1, y1, x2, y2 in lines[x]:
                cv2.line(imgResult, (x1, y1), (x2, y2), (0, 0, 255), 2)
        for i in lines:
            linecount += 1
    except (ValueError, TypeError):
        print('no lines found,dumbass')
    if previouslinecount > linecount:
        if previouslinecount > highlinecount:
            highlinecount = previouslinecount
            besth_max = s_max
    elif previouslinecount < linecount:
        if linecount > highlinecount:
            highlinecount = linecount
            besth_max = s_max
    if s_max!=0 and foundhmax== False:
        s_max -= 1
    else:
        foundhmax = True
        s_max = besth_max
    HorStack = np.hstack((imgresized,imgResult))
    cv2.putText(HorStack, 'line count: '+str(linecount),(0,25),cv2.FONT_HERSHEY_COMPLEX, 1,(0,255,0),1)
    cv2.putText(HorStack, 's_max: ' + str(s_max), (0, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)
    #cv2.putText(HorStack, 'best s_max: ' + str(besth_max), (0, 75), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)
    cv2.imshow('Original + Final img + HSV filter', HorStack)
    cv2.imshow('test', imgcanny)
    previouslinecount = linecount
    linecount = 0
    print('------------------')
    cv2.waitKey(1)