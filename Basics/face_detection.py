import cv2


faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
img_path = "smallvslarge-group.jpg"
img = cv2.imread(img_path)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = faceCascade.detectMultiScale(img_gray, 1.1, 4)
for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
cv2.imshow("result", img)
cv2.waitKey(0)