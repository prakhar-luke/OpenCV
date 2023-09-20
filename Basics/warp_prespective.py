import cv2
import numpy as np

img = cv2.imread("card.jpg")
width, height = 250, 350
pts1 = np.float32([[142, 24], [230, 38], [126, 147], [213, 161]])
pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
matrix = cv2.getPerspectiveTransform(pts1, pts2)
img_put = cv2.warpPerspective(img, matrix, (width, height))
cv2.imshow("img", img)
cv2.imshow("warpPerspective_img", img_put)
cv2.waitKey(0)