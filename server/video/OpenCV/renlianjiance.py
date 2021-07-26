from __future__ import print_function
from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2

# 人脸识别分类器
#初始化行人检测器
hog = cv2.HOGDescriptor()   #初始化方向梯度直方图描述子
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())  #设置支持向量机(Support Vector Machine)使得它成为一个预先训练好了的行人检测器

faceCascade = cv2.CascadeClassifier(r'D:\Python\Python38\Lib\site-packages\cv2\data\haarcascade_frontalface_alt.xml')
# 识别眼睛的分类器
eyeCascade = cv2.CascadeClassifier(r'D:\Python\Python38\Lib\site-packages\cv2\data\haarcascade_eye.xml')
# 开启摄像头
cap = cv2.VideoCapture(0)
ok = True
result = []
while ok:
    # 读取摄像头中的图像，ok为是否读取成功的判断参数
    ok, frame = cap.read()
    # 转换成灰度图像
    frame = imutils.resize(frame, width=min(400, frame.shape[1]))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # gray = cv2.GaussianBlur(gray,(21,21),0)  # 对灰阶图像进行高斯模糊
    # 人脸检测
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # 在检测人脸的基础上检测眼睛
    for (x, y, w, h) in faces:
        fac_gray = gray[y: (y+h), x: (x+w)]
        result = []
        eyes = eyeCascade.detectMultiScale(fac_gray, 1.3, 2)

        # 眼睛坐标的换算，将相对位置换成绝对位置
        for (ex, ey, ew, eh) in eyes:
            result.append((x+ex, y+ey, ew, eh))

    # 画矩形
    for (x, y, w, h) in faces:

        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    for (ex, ey, ew, eh) in result:
        cv2.rectangle(frame, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

    cv2.imshow('video', frame)

    k = cv2.waitKey(1)
    # press 'ESC' to quit
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
