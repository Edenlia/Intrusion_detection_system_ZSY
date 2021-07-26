import numpy as np
from PIL import Image
import os
import cv2
# 调用笔记本内置摄像头，所以参数为0，如果有其他的摄像头可以调整参数为1，2
cap = cv2.VideoCapture(0)
# CascadeClassifier，是Opencv中做人脸检测的时候的一个级联分类器
face_detector = cv2.CascadeClassifier(r'cv2-Haar\lbpcascade_frontalface.xml')

face_id = input('\n enter user id:')

print('\n 正在采集，请稍等 ...')

count = 0

while True:

    # 从摄像头读取图片

    sucess, img = cap.read()

    # 转为灰度图片

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 检测人脸

    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+w), (255, 0, 0))
        count += 1

        # 保存图像
        cv2.imwrite("Facedata/User." + str(face_id) + '.' + str(count) + '.jpg', gray[y: y + h, x: x + w])

        cv2.imshow('image', img)

    # 保持画面的持续。

    k = cv2.waitKey(1)

    if k == 27:   # 通过esc键退出摄像
        break

    elif count >= 3:  # 得到1000个样本后退出摄像
        break

print('\n 采集完毕')

# 关闭摄像头
cap.release()
cv2.destroyAllWindows()
# 人脸数据路径
path = "D:/xiaoxueqi/Face/FaceData"
# 使用OpenCV中LBPH算法的方法建立人脸数据模型
recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier(r'cv2-Haar\haarcascade_frontalface_alt.xml')

def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faceSamples = []
    ids = []
    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L')   # convert it to grayscale
        img_numpy = np.array(PIL_img, 'uint8')     # 图片格式转换
        if os.path.split(imagePath)[-1].split(".")[-1] != 'jpg':
            continue
        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_numpy)   # 人脸检测
        for (x, y, w, h) in faces:
            faceSamples.append(img_numpy[y:y + h, x: x + w])
            ids.append(id)
    return faceSamples, ids

print('正在人脸训练，请等待 ...')
faces, ids = getImagesAndLabels(path)
# 训练和保存模型
recognizer.train(faces, np.array(ids))
# recognizer.save('TrainData\train.yml')
recognizer.write(r'TrainData\train.yml')
print("{0} faces trained. Exiting Program".format(len(np.unique(ids))))
# cv2.destroyAllWindows()
# recognizer = cv2.face.LBPHFaceRecognizer_create()
# recognizer.read('TrainData/train.yml')
# # gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# # new_faces = face_detector.detectMultiScale(gray)
# cascadePath = r'cv2-Haar\haarcascade_frontalface_alt.xml'
# faceCascade = cv2.CascadeClassifier(cascadePath)
# font = cv2.FONT_HERSHEY_SIMPLEX
#
# idnum = 0  # id与names数组里面的不相同，相差1
#
# names = ['yy', 'yx', 'yz']  # names中存储人的名字，若该人id为0则他的名字在第一位，id位1则排在第二位，以此类推。
#
# cam = cv2.VideoCapture(0)
# minW = 0.1 * cam.get(3)
# minH = 0.1 * cam.get(4)
#
# while True:
#     ret, img = cam.read()
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#
#     faces = faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(int(minW), int(minH)))
#
#     for (x, y, w, h) in faces:
#         cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
#         idnum, confidence = recognizer.predict(gray[y:y + h, x:x + w])
#
#         if confidence < 100:
#             idnum = names[idnum]
#             confidence = "{0}%".format(round(100 - confidence))
#         else:
#             idnum = "unknown"
#             confidence = "{0}%".format(round(100 - confidence))
#         # if confidence < 50:# 低于这个报警
#         cv2.putText(img, str(idnum), (x + 5, y - 5), font, 1, (0, 0, 255), 1)
#         cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (0, 0, 0), 1)
#     if idnum == "unknown":
#         faces = face_detector.detectMultiScale(gray, 1.3, 5)
#         for (x, y, w, h) in faces:
#             cv2.rectangle(img, (x, y), (x + w, y + w), (255, 0, 0))
#             count += 1
#             # 保存图像
#             cv2.imwrite("unknownData/wrong." + str(count) + '.jpg', gray[y: y + h, x: x + w])
#             # cv2.imshow('image', img)
#     cv2.imshow('camera', img)
#     k = cv2.waitKey(10)
#     if k == 27:
#         break
#
# cam.release()
# cv2.destroyAllWindows()