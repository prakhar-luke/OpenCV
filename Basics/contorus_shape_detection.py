import cv2
import numpy as np


def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver


def getContours(img):
    countours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for i in countours:
        area = cv2.contourArea(i)
        if area > 500:
            cv2.drawContours(img_contour, i, -1, (255,0,0), 3)
            perimeter = cv2.arcLength(i, True)
            aprox_corner_point = cv2.approxPolyDP(i, 0.02*perimeter, True)
            obj_corner = len(aprox_corner_point)
            x, y, w, h = cv2.boundingRect(aprox_corner_point)
            if obj_corner == 3:
                obj_type = 'Triangle'
            elif obj_corner == 4:
                asp_ratio = w/h
                if asp_ratio > 0.95 and asp_ratio < 1.05:
                    obj_type = 'Square'
                else:
                    obj_type = 'Rectangle'
            elif obj_corner > 4 and obj_corner < 8:
                obj_type = 'Polygon'
            elif obj_corner >= 8:
                obj_type = 'Circle'
            else:
                obj_type = 'None'
            cv2.rectangle(img_contour, (x,y), (x+w, y+h), (0,0,255), 2)
            cv2.putText(img_contour, obj_type, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            #cv2.putText(img_contour, str(obj_corner), (x+w, y+h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

img = cv2.imread('shapes.jpg')
img_contour = img.copy()
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_blur = cv2.GaussianBlur(img_gray, (5,5), 1)
img_canny = cv2.Canny(img_blur, 50, 50)
getContours(img_canny)
img_blank = np.zeros_like(img)
img_stack = stackImages(0.6, ([img, img_gray, img_blur], [img_canny, img_contour, img_blank]))
cv2.imshow("stack img", img_stack)
cv2.waitKey(0)