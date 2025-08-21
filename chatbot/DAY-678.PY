import cv2
import numpy as np

img = np.zeros((200,200,3), dtype=np.uint8)
print(img.shape)

cv2.imshow("black image", img)

cv2.waitKey(0)

cv2.destroyAllwindows()