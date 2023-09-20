import cv2
import numpy as np


img = np.zeros((512,512,3), np.uint8)

# color image
# img[:] = 255,255,0

# line
cv2.line(img, (0,0), (200,200), (0,255,0))

# rectangle
cv2.rectangle(img, (30,30), (200,200), (255,255,0), thickness=1) # replace thickness for cv2.FILLED to fill

# circle
cv2.circle(img, (400,40), 100, (0,255,255), 3)

# text
cv2.putText(img, "Hiiiiiiiii", (300,200), cv2.FONT_HERSHEY_SIMPLEX, 1, (100,100,0), 2)

cv2.imshow("img", img)
cv2.waitKey(0)