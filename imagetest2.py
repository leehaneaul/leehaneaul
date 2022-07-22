import cv2
import numpy as np
import math
import sys

ori_img = cv2.imread("img/test/6.jfif", cv2.IMREAD_COLOR)
gray = cv2.cvtColor(ori_img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.adaptiveThreshold(
            blur,
            maxValue=255.0,
            adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            thresholdType=cv2.THRESH_BINARY_INV,
            blockSize=19,
            C=9
        )

contours, hi = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
tmp = 0
for i in range(len(contours)):
    img = ori_img
    cnt = contours[i]
    #area = cv2.contourArea(cnt)
    x, y, w, h = cv2.boundingRect(cnt)
    rect_area = w*h
    if(rect_area > 10000):
        print(rect_area)
        if tmp == 0:
            tmp = rect_area
            tmp_cnt = cnt
        else:
            if tmp > rect_area:
                tmp = rect_area
                tmp_cnt = cnt
try:
    x, y, w, h = cv2.boundingRect(tmp_cnt)
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
except:
    print("이미지 못찾음")
    sys.exit()
crop_img = img[y: y + h, x: x + w]
crop_img = cv2.resize(crop_img, (300, 188))
cv2.imshow('test', crop_img)
cv2.waitKey()
cv2.destroyAllWindows()

src_cp = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(src_cp, 100, 200)
lines = cv2.HoughLines(edges, 1, np.pi/180, 110)

min_theta = np.pi / 2
if lines is not None:
    for line in lines:
        r, theta = line[0]
        if (theta < min_theta and theta > 0):
            min_theta = theta
        tx, ty = np.cos(theta), np.sin(theta)
        x0, y0 = tx*r, ty*r
        cv2.circle((src_cp), (int(abs(x0)), int(abs(y0))), 3, (0, 0, 255), -1)
        x1, y1 = int(x0 + w*(-ty)), int(y0 + h * tx)
        x2, y2 = int(x0 - w*(-ty)), int(y0 - h * tx)
        cv2.line(src_cp, (x1, y1), (x2, y2), (0,255,0), 1)

merged = np.hstack((gray, src_cp))
ver, hor = src_cp.shape
diag = int(((hor * hor + ver * ver) ** 0.5))
center = int(hor / 2), int(ver / 2)
degree = -math.degrees((np.pi / 2) - min_theta)
rotate = cv2.getRotationMatrix2D(center, degree, 1)
res_rotate = cv2.warpAffine(src_cp, rotate, (hor, ver))

np_hor = np.hstack((src_cp, res_rotate))
np_hor_con = np.concatenate((src_cp, res_rotate), axis=1)

cv2.imshow('test', np_hor)
cv2.waitKey(0)
cv2.destroyAllWindows()