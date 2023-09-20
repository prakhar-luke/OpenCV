import cv2


img_path = "C:/Users/prakh/fiftyone/open-images-v7/validation/data/3d4789f13f7f6d1c.jpg"
img = cv2.imread(img_path)
print(img.shape)
resize_img = cv2.resize(img, (342, 512))
img_crop = img[:512, :342]
cv2.imshow("img", img)
cv2.imshow("processed ", img_crop)
cv2.waitKey(0)
