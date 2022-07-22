import sys
import cv2

ori_img = cv2.imread("img/test/1.jfif", cv2.IMREAD_COLOR)
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
    if(rect_area > 20000):
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
except:
    print("이미지 못찾음")
    sys.exit()
cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv2.imshow('test', img)
cv2.waitKey()
cv2.destroyAllWindows()