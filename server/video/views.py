from django.http import HttpResponse, StreamingHttpResponse
import numpy as np
from django.views.decorators.csrf import csrf_exempt
import cv2 as cv
import threading
from django.views.decorators import gzip
from imutils.object_detection import non_max_suppression
import time
import pygame
import base64
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import requests

import cv2
import numpy as np
from qiniu import Auth, put_file, etag
import qiniu.config

ak = 'gllUD3Ik4X7BaXw44GBY6jKfqI9K5qLhNCFZ7uf8'
sk = 'La3cQhn95ATO4pACyogVtHWxeFvkLejMEwHh1vVv'
bn = 'intrusion-detection-system'


def send_img_to_server(AK, SK, BUCKET_NAME, KEY, DATA):
    # 构建鉴权对象
    q = Auth(AK, SK)
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(BUCKET_NAME, KEY, 3600)
    # 要上传文件的本地路径
    ret, info = put_file(token, KEY, DATA, version='v2')


class VideoCamera(object):
    def __init__(self, url):
        self.video = cv2.VideoCapture(url)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        try:
            while True:
                (self.grabbed, self.frame) = self.video.read()
        except BaseException:
            print("error")


# test licence camera
class VideoCamera1(object):
    def __init__(self, url):
        self.video = cv2.VideoCapture(url)
        (self.grabbed, self.frame) = self.video.read()

        threading.Thread(target=self.license_check, args=()).start()
        # elif (self.type is 2):
        #     threading.Thread(target=self.license_check, args=()).start()
        # elif (self.type is 3):
        #     threading.Thread(target=self.license_check, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def dealPicture(self, img01):
        msg_from = '1761106187@qq.com'  # 发送方邮箱
        passwd = 'drqsmnsigutddhie'  # 就是上面的授权码
        to = ['1761106187@qq.com']  # 接受方邮箱
        # 设置邮件内容
        # MIMEMultipart类可以放任何内容
        msg = MIMEMultipart()
        params = {"image": img01}
        access_token = '24.9515cd4eb810ad1b9793ae4b1735f6d1.2592000.1629558405.282335-24591576'
        request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/license_plate"
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(request_url, data=params, headers=headers)
        my_result = response.json()

        if response:
            print(my_result)
            newStr = my_result['words_result']['number']
            print(newStr)

            # key = newStr+'.jpg'
            # data = 'Car.jpg'
            #
            # send_img_to_server(ak, sk, bn, key, data)

            data = {
                "case_type": 1,
                "case_description": newStr,
                "img": "Car.jpg",
                "detect_camera_id": 1

            }
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url='http://172.30.68.249:8000/api/case/add_case/', headers=headers,
                                     data=json.dumps(data))
            print(response.json())

            # 发送邮件
            conntent = "异常车辆进入！异常车辆进入！"
            msg.attach(MIMEText(conntent, 'plain', 'utf-8'))
            msg['Subject'] = "这个是邮件主题"
            msg['From'] = msg_from
            s = smtplib.SMTP_SSL("smtp.qq.com", 465)
            s.login(msg_from, passwd)
            s.sendmail(msg_from, to, msg.as_string())
            # print("邮件发送成功")

    # def add_case(self):
    #     data = {
    #         'username': "zsy",
    #         'password': "123"
    #     }
    #     headers = {'Content-Type': 'application/json'}
    #     response = requests.post(url='url', headers=headers, data=json.dumps(data))
    #     print(response)

    def license_check(self):
        # msg_from = '1761106187@qq.com'  # 发送方邮箱
        # passwd = 'drqsmnsigutddhie'  # 就是上面的授权码
        # to = ['1761106187@qq.com']  # 接受方邮箱
        # # 设置邮件内容
        # # MIMEMultipart类可以放任何内容
        # msg = MIMEMultipart()
        # request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/license_plate"
        classfier = cv2.CascadeClassifier("F:\Intrusion_detection_system_ZSY\server\\video\\License.xml")
        # cam = cv2.VideoCapture(0)
        minW = 0.1 * self.video.get(3)
        minH = 0.1 * self.video.get(4)
        licenseStr = ""

        width = int(self.video.get(1))
        height = int(self.video.get(1))
        firstFrame = None

        number = 30

        while True:
            wheMove = False
            (self.grabbed, self.frame) = self.video.read()
            # ret, img = cam.read()
            gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            cars = classfier.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=3, minSize=(40, 40))

            gray = cv2.GaussianBlur(gray, (31, 31), 0)
            if firstFrame is None:
                firstFrame = gray
                continue

            frameDelta = cv2.absdiff(firstFrame, gray)
            thresh = cv2.threshold(frameDelta, 30, 220, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)
            (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
            for c in cnts:
                if cv2.contourArea(c) < 2500:
                    continue
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(self.frame, (x, y), (x + w, y + h), (96, 96, 96), 2)
                wheMove = True
            # cv2.imshow("Security Feed", frame)
            firstFrame = gray.copy()

            if (wheMove == False):
                for (x, y, w, h) in cars:
                    cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    img2gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                    imageVar = cv2.Laplacian(img2gray, cv2.CV_64F).var()
                    # print(imageVar)
                    if (imageVar > 180):
                        image = cv2.GaussianBlur(self.frame, (3, 3), 0)
                        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
                        Sobel_x = cv2.Sobel(image, cv2.CV_16S, 1, 0)
                        absX = cv2.convertScaleAbs(Sobel_x)  # 转回uint8
                        image = absX
                        # 二值化：图像的二值化，就是将图像上的像素点的灰度值设置为0或255,图像呈现出明显的只有黑和白
                        self.grabbed, image = cv2.threshold(image, 0, 255, cv2.THRESH_OTSU)
                        # 闭操作：闭操作可以将目标区域连成一个整体，便于后续轮廓的提取。
                        kernelX = cv2.getStructuringElement(cv2.MORPH_RECT, (17, 5))
                        image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernelX)
                        # 膨胀腐蚀(形态学处理)
                        kernelX = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 1))
                        kernelY = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 19))
                        image = cv2.dilate(image, kernelX)
                        image = cv2.erode(image, kernelX)
                        image = cv2.erode(image, kernelY)
                        image = cv2.dilate(image, kernelY)
                        # 平滑处理，中值滤波
                        image = cv2.medianBlur(image, 15)
                        # 查找轮廓
                        contours, w1 = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                        for item in contours:
                            rect = cv2.boundingRect(item)
                            x = rect[0]
                            y = rect[1]
                            weight = rect[2]
                            height = rect[3]
                            if weight > (height * 2):
                                # 裁剪区域图片
                                chepai = self.frame[y:y + height, x:x + weight]
                                # cv2.imshow('img', img)
                                cv2.imwrite("Car" + '.jpg', self.frame)
                                cv2.circle(self.frame, (60, 60), 60, (0, 0, 255), 0)
                                # cv2.imshow('chepai' + str(x), chepai)
                                f = open('Car.jpg', 'rb')
                                img01 = base64.b64encode(f.read())

                                # threading.Thread(target=self.dealPicture, args=(img01,)).start()
                                if number == 30:
                                    number = 0
                                    threading.Thread(target=self.dealPicture, args=(img01,)).start()
                                else:
                                    number = number + 1

            cv2.waitKey(1)


class VideoCamera2(object):
    def __init__(self, url):
        self.video = cv2.VideoCapture(url)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()
        # threading.Thread(target=self.age(),args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def send_email(self, msg_from, passwd, msg_to, text_content):
        msg = MIMEMultipart()
        subject = "陌生人进入，危险报警 ！"  # 主题
        text = MIMEText(text_content)
        msg.attach(text)
        # docFile = 'C:/Users/main.py'  如果需要添加附件，就给定路径
        # if file_path:  # 最开始的函数参数我默认设置了None ，想添加附件，自行更改一下就好
        #     docFile = file_path
        #     docApart = MIMEApplication(open(docFile, 'rb').read())
        #     docApart.add_header('Content-Disposition', 'attachment', filename=docFile)
        #     msg.attach(docApart)
        #     print('发送附件！')
        msg['Subject'] = subject
        msg['From'] = msg_from
        msg['To'] = msg_to
        try:
            s = smtplib.SMTP_SSL("smtp.qq.com", 465)
            s.login(msg_from, passwd)
            s.sendmail(msg_from, msg_to, msg.as_string())
            print("发送成功")
        except smtplib.SMTPException as e:
            print("发送失败")
        finally:
            s.quit()

    def baojing(self, gender, age):
        face_detector = cv2.CascadeClassifier(
            r'F:/Intrusion_detection_system_ZSY/server/video/cv2-Haar/haarcascade_frontalface_alt.xml')
        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.1, 3)
        for (x, y, w, h) in faces:
            cv2.rectangle(self.frame, (x, y), (x + w, y + w), (255, 0, 0))
            # 保存图像

            # cv2.imwrite(r"unknownData\wrong-" + str(
            #     time.strftime('%Y%m%d%H%M', time.localtime(time.time()))) + '.jpg',
            #             gray[y: y + h, x: x + w])
            cv2.imwrite(r"Human.jpg", self.frame)

        # 发送邮件提醒

        msg_from = '1393371859@qq.com'  # 发送方邮箱
        passwd = 'vgfgezofbpcbibca'  # 填入发送方邮箱的授权码（就是刚刚你拿到的那个授权码）
        msg_to = '19301105@bjtu.edu.cn'  # 收件人邮箱
        text_content = "有陌生人进入，危险!"  # 发送的邮件内容
        # file_path = r"D:\xiaoxueqi\Intrusion_detection_system_ZSY-cdx\unknownData\wrong-{0}.jpg".format(
        #  time.strftime('%Y%m%d%H%M', time.localtime(time.time())))
        self.send_email(msg_from, passwd, msg_to, text_content)

        data = {
            "case_type": 2,  # 人员入侵
            "case_description": str(gender) + ',' + str(age),
            "img": "Human.jpg",
            "detect_camera_id": 4  # 第二个监控人脸摄像头
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url='http://172.30.68.249:8000/api/case/add_case/', headers=headers,
                                 data=json.dumps(data))
        print(response.json())

    def getFaceBox(self, net, frame, conf_threshold=0.7):
        frameOpencvDnn = self.frame.copy()
        frameHeight = frameOpencvDnn.shape[0]  # 高就是矩阵有多少行
        frameWidth = frameOpencvDnn.shape[1]  # 宽就是矩阵有多少列
        blob = cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)
        #  blobFromImage(image[, scalefactor[, size[, mean[, swapRB[, crop[, ddepth]]]]]]) -> retval  返回值   # swapRB是交换第一个和最后一个通道   返回按NCHW尺寸顺序排列的4 Mat值
        net.setInput(blob)
        detections = net.forward()  # 网络进行前向传播，检测人脸
        bboxes = []
        for i in range(detections.shape[2]):
            confidence1 = detections[0, 0, i, 2]
            if confidence1 > conf_threshold:
                x1 = int(detections[0, 0, i, 3] * frameWidth)
                y1 = int(detections[0, 0, i, 4] * frameHeight)
                x2 = int(detections[0, 0, i, 5] * frameWidth)
                y2 = int(detections[0, 0, i, 6] * frameHeight)
                bboxes.append([x1, y1, x2, y2])  # bounding box 的坐标
                # cv.rectangle(frameOpencvDnn, (x1, y1), (x2, y2), (0, 255, 0), int(round(frameHeight / 150)),
                #  8)  # rectangle(img, pt1, pt2, color[, thickness[, lineType[, shift]]]) -> img
        return frameOpencvDnn, bboxes

    def update(self):
        # global confidence, idnum, x, y, h
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(r'F:/Intrusion_detection_system_ZSY/server/video/train.yml')
        cascadePath = r'F:/Intrusion_detection_system_ZSY/server/video/cv2-Haar/haarcascade_frontalface_alt.xml'
        faceCascade = cv2.CascadeClassifier(cascadePath)

        faceProto = r"F:/Intrusion_detection_system_ZSY/server/video/age_gender/opencv_face_detector.pbtxt"
        faceModel = r"F:/Intrusion_detection_system_ZSY/server/video/age_gender/opencv_face_detector_uint8.pb"

        ageProto = r"F:/Intrusion_detection_system_ZSY/server/video/age_gender/age_deploy.prototxt"
        ageModel = r"F:/Intrusion_detection_system_ZSY/server/video/age_gender/age_net.caffemodel"

        genderProto = r"F:/Intrusion_detection_system_ZSY/server/video/age_gender/gender_deploy.prototxt"
        genderModel = r"F:/Intrusion_detection_system_ZSY/server/video/age_gender/gender_net.caffemodel"

        # 模型均值
        MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
        # ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-30)', '(38-43)', '(48-53)', '(60-100)']
        ageList = ['(0-1)', '(1-2)', '(2-4)', '(4-5)', '(6-18)', '(18-30)', '(43-60)', '(60-100)']
        genderList = ['Male', 'Female']

        # 加载网络
        ageNet = cv.dnn.readNet(ageModel, ageProto)
        genderNet = cv.dnn.readNet(genderModel, genderProto)

        # 人脸检测的网络和模型
        faceNet = cv.dnn.readNet(faceModel, faceProto)
        padding = 20
        minW = 0.1 * self.video.get(3)
        minH = 0.1 * self.video.get(4)
        font = cv2.FONT_HERSHEY_SIMPLEX
        number = 150
        idnum = 0
        while True:
            (self.grabbed, self.frame) = self.video.read()
            t = time.time()
            hasFrame, frame = self.video.read()
            self.frame, bboxes = self.getFaceBox(faceNet, frame)
            gender, age = genderList[0], ageList[4]
            for bbox in bboxes:
                # 取出box框住的脸部进行检测,返回的是脸部图片
                face = frame[max(0, bbox[1] - padding):min(bbox[3] + padding, frame.shape[0] - 1),
                       max(0, bbox[0] - padding):min(bbox[2] + padding, frame.shape[1] - 1)]
                blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
                genderNet.setInput(blob)  # blob输入网络进行性别的检测
                genderPreds = genderNet.forward()  # 性别检测进行前向传播
                gender = genderList[genderPreds[0].argmax()]  # 分类  返回性别类型
                ageNet.setInput(blob)
                agePreds = ageNet.forward()
                age = ageList[agePreds[0].argmax()]
                label = "{},{}".format(gender, age)
                # print(gender + ',' + age)
                # post request 年龄性别 descrition Male,(0-10)

                cv2.putText(self.frame, label, (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 1,
                            cv2.LINE_AA)
            gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(int(minW), int(minH)))
            for (x, y, w, h) in faces:
                cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                idnum, confidence = recognizer.predict(gray[y:y + h, x:x + w])
                # 函数cv2.face_FaceRecognizer.predict()
                # 在对一个待测人脸图像进行判断时，会寻找与当前图像距离最近的人脸图像。与哪个人脸图像最接近，就将待测图像识别为其对应的标签。
                # confiidence 0 完全匹配 <50 可以接受 >80 差别较大

                if number == 150:
                    number = 0
                    print(confidence)
                    if 0 < confidence < 60:
                        confidence = "{0}%".format(round(82))
                    else:
                        idnum = "unknown"
                        confidence = "{0}%".format(round(10))
                        print("bad people")

                        threading.Thread(target=self.baojing, args=(gender, age,)).start()
                        # cv2.putText(self.frame, str(idnum), (x + 5, y - 5), font, 1, (0, 0, 255), 1)
                        # cv2.putText(self.frame, str(confidence), (x + 5, y + h - 5), font, 1, (0, 0, 0), 1)
                else:
                    number = number + 1
                cv2.putText(self.frame, str(idnum), (x + 5, y - 5), font, 1, (0, 0, 255), 1)
                cv2.putText(self.frame, str(confidence), (x + 5, y + h - 5), font, 1, (0, 0, 0), 1)
                cv2.waitKey(10)


class VideoCamera3(object):
    def __init__(self, url):
        # self.pick = 0
        self.video = cv2.VideoCapture(url)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()
        # threading.Thread(target=self.analyse, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def send_email(self, msg_from, passwd, msg_to, text_content):
        msg = MIMEMultipart()
        subject = "危险报警"  # 主题
        text = MIMEText(text_content)
        msg.attach(text)
        msg['Subject'] = subject
        msg['From'] = msg_from
        msg['To'] = msg_to
        try:
            s = smtplib.SMTP_SSL("smtp.qq.com", 465)
            s.login(msg_from, passwd)
            s.sendmail(msg_from, msg_to, msg.as_string())
            print("发送成功")
        except smtplib.SMTPException as e:
            print("发送失败")
        finally:
            s.quit()

    def analyse(self):
        # 打印检测到的目标个数
        # print("检测到进入危险区域行人个数为{}".format(len(self.pick)))
        # 发送邮件提醒
        msg_from = '1393371859@qq.com'  # 发送方邮箱
        passwd = 'vgfgezofbpcbibca'  # 填入发送方邮箱的授权码（就是刚刚你拿到的那个授权码）
        msg_to = '19301105@bjtu.edu.cn'  # 收件人邮箱
        text_content = "禁区有人进入，危险!"  # 发送的邮件内容
        cv2.imwrite("Area" + '.jpg', self.frame)

        self.send_email(msg_from, passwd, msg_to, text_content)
        data = {
            "case_type": 3,  # 人员入侵
            "case_description": "禁区有人入侵",
            "img": "Area.jpg",
            "detect_camera_id": 5  # 第二个监控人脸摄像头
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url='http://172.30.68.249:8000/api/case/add_case/', headers=headers,
                                 data=json.dumps(data))
        print(response.json())


    def update(self):

        # 初始化方向梯度直方图描述子
        hog = cv2.HOGDescriptor()
        # 设置支持向量机使得它成为一个预先训练好了的行人检测器
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        number = 15

        while True:
            (self.grabbed, self.frame) = self.video.read()
            cv2.rectangle(self.frame, (350, 20), (600, 350), (255, 0, 0), 2)  # 原图 左上角坐标 有效角坐标  颜色 画线宽度
            (rects, weights) = hog.detectMultiScale(self.frame, winStride=(4, 4), padding=(8, 8), scale=1.05)
            # 设置来抑制重叠的框
            rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
            pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
            # 绘制红色人体矩形框
            # for (x, y, w, h) in pick:
            #     cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # # 绘制绿色对比框
            # cv2.rectangle(self.frame, (50, 50), (600, 450), (0, 255, 0), 2)

            # 对图像进行多尺度行人检测，返回结果为矩形框
            #(rects, weights) = hog.detectMultiScale(self.frame, winStride=(4, 4), padding=(8, 8), scale=1.05)
            #rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
            #pick1 = non_max_suppression(rects, probs=None, overlapThresh=0.65)
            for (x, y, w, h) in pick:
                cv2.rectangle(self.frame, (x, y), (w, h), (0, 255, 0), 2)
            # len(pick)
            if number == 150:
                number = 0
                if len(pick) > 0:
                    threading.Thread(target=self.analyse, args=()).start()
            else:
                number = number + 1
            cv2.waitKey(10)


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@gzip.gzip_page
@csrf_exempt
def test1(request):
    try:
        cam = VideoCamera1("rtmp://localhost:1935/live/home")
        # cam = VideoCamera1("rtmp://172.30.68.249:1935/live/home1")
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except BaseException:  # This is bad! replace it with proper handling
        pass


@gzip.gzip_page
@csrf_exempt
def test2(request):
    try:
        cam = VideoCamera2('rtmp://localhost:1935/live/home1')
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except BaseException:  # This is bad! replace it with proper handling
        pass


@gzip.gzip_page
@csrf_exempt
def test3(request):
    try:
        cam = VideoCamera3('rtmp://localhost:1935/live/home2')
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except BaseException:  # This is bad! replace it with proper handling
        pass
