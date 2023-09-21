import cv2
import numpy as np


w_img = 540
h_img = 640
cam = 0 # used droid cam for better image quality 'http://wifi_ip:port_number/video'
cap = cv2.VideoCapture(cam)
cap.set(3, w_img)
cap.set(4, h_img)
cap.set(10, 150)  #Brightness


def pre_process(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img, (5, 5), 1)
    img_canny = cv2.Canny(img_blur, 150, 200)
    kernel = np.ones((5,5))
    img_dilate = cv2.dilate(img_canny, kernel, iterations=2)
    img_erode = cv2.erode(img_dilate, kernel, iterations=1)
    return img_erode


def getContours(img):
    biggest = np.array([])
    max_area = 0
    countours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for i in countours:
        area = cv2.contourArea(i)
        if area > 5000:
            #cv2.drawContours(img_contour, i, -1, (0, 255, 0), 3)
            perimeter = cv2.arcLength(i, True)
            aprox_corner_point = cv2.approxPolyDP(i, 0.02*perimeter, True)
            if area > max_area and len(aprox_corner_point) == 4:
                biggest = aprox_corner_point
                max_area = area
            #print(len(aprox_corner_point))
    cv2.drawContours(img_contour, biggest, -1, (0, 255, 0), 20)
    return biggest


def reorder(myPoints):
    myPoints = myPoints.reshape((4, 2))
    New_points = np.zeros((4, 1, 2), np.int32)
    add = myPoints.sum(1)
    New_points[0] = myPoints[np.argmin(add)]
    New_points[3] = myPoints[np.argmax(add)]
    diff = np.diff(myPoints, axis=1)
    New_points[1] = myPoints[np.argmin(diff)]
    New_points[2] = myPoints[np.argmax(diff)]
    return New_points


def warp_perspective(img, biggest):
    biggest = reorder(biggest)
    pts1 = np.float32(biggest)
    pts2 = np.float32([[0, 0], [w_img, 0], [0, h_img], [w_img, h_img]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    img_output = cv2.warpPerspective(img, matrix, (w_img, h_img))
    # pixel_to_chisel = 20
    # cropped_img = img_output[pixel_to_chisel:img_output.shape[0] - pixel_to_chisel,
    #               pixel_to_chisel: img_output.shape[1] - pixel_to_chisel]
    # cropped_img = cv2.resize(cropped_img, (w_img, h_img))
    # return cropped_img
    return img_output


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


while True:
    sucess, img = cap.read()
    img = cv2.resize(img, (w_img, h_img))
    img_contour = img.copy()

    img_thresh = pre_process(img)
    biggest = getContours(img_thresh)
    # print(biggest.shape)
    if biggest.size != 0:
        warped_img = warp_perspective(img, biggest)
        imgArray = ([img, img_thresh], [img_contour, warped_img])
        # imgArray = ([img_contour, warped_img])
        img_stack = stackImages(0.6, imgArray)
        # cv2.imshow("img stack", img_stack)
        cv2.imshow("result", warped_img)
    else:
        imgArray = ([img_contour, img])
    stackedImages = stackImages(0.6, imgArray)
    cv2.imshow("WorkFlow", stackedImages)
    # cv2.imshow("result", warped_img)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        cv2.destroyAllWindows()
        cap.release()
        break
