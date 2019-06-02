# -*- coding: utf-8 -*-

import cv2

filepath = "data/girl.png"
img = cv2.imread(filepath)
cv2.namedWindow('Girl')
cv2.imshow('Girl', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
