import cv2
import numpy as np


img_path = "C:/Users/prakh/fiftyone/open-images-v7/validation/data/3d4789f13f7f6d1c.jpg"
img = cv2.imread(img_path)
imggray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imggray, (7,7),0)
cannyImg = cv2.Canny(imgBlur, 100, 150)
kernel = np.ones((3,3), np.uint8)
img_dilation = cv2.dilate(cannyImg, kernel, iterations=4)
img_erod = cv2.erode(img_dilation, kernel, iterations=4)
cv2.imshow("Precessed image", img_erod)
cv2.waitKey(0)