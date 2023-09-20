import cv2
import numpy as np


frame_h = 640
frame_w = 480
cap = cv2.VideoCapture(0)
cap.set(3, frame_w)
cap.set(4, frame_h)
cap.set(10, 100) # brightness

pen_colors = [[0,6,132,255,20,241],
                  [99,134,119,255,86,207],
                  [56,82,63,255,0,202]]
color_values = [[0,0,255],
                [255,0,0],
                [0,128,0]]
points = []  # [x, y, color_idx]
def find_color(img, pen_colors, color_values):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    new_point = []
    for colours in pen_colors:
        lower = np.array(colours[0:3])
        upper = np.array(colours[3:6])
        mask = cv2.inRange(img_hsv, lower, upper)
        x, y = getContours(mask)
        cv2.circle(result_img, (x,y), 10, color_values[count], cv2.FILLED)
        if x!= 0 and y != 0:
            new_point.append([x,y,count])
        count += 1
    return new_point

def getContours(img):
    countours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for i in countours:
        area = cv2.contourArea(i)
        if area > 500:
            perimeter = cv2.arcLength(i, True)
            aprox_corner_point = cv2.approxPolyDP(i, 0.02*perimeter, True)
            x, y, w, h = cv2.boundingRect(aprox_corner_point)
    return x+w//2, y

def draw_lines(points, color_values):
    for point in points:
        cv2.circle(result_img, (point[0], point[1]), 10, color_values[point[2]], cv2.FILLED)

while True:
    success , frame = cap.read()
    result_img = frame.copy()
    new_point = find_color(frame, pen_colors, color_values)
    if len(new_point) != 0:
        for i in new_point:
            points.append(i)
    if len(points) != 0:
        draw_lines(points, color_values)
    cv2.imshow('result_img', result_img)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break