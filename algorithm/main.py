import json
import datetime
import cv2
import threading
import requests
import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


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
        newStr = my_result['words_result']['number']
        print(newStr)

        # 发送邮件
        conntent = "异常车辆进入！异常车辆进入！"
        msg.attach(MIMEText(conntent, 'plain', 'utf-8'))
        msg['Subject'] = "这个是邮件主题"
        msg['From'] = msg_from
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(msg_from, passwd)
        s.sendmail(msg_from, to, msg.as_string())
        # print("邮件发送成功")

    def license_check(self):
        # msg_from = '1761106187@qq.com'  # 发送方邮箱
        # passwd = 'drqsmnsigutddhie'  # 就是上面的授权码
        # to = ['1761106187@qq.com']  # 接受方邮箱
        # # 设置邮件内容
        # # MIMEMultipart类可以放任何内容
        # msg = MIMEMultipart()
        # request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/license_plate"
        classfier = cv2.CascadeClassifier("D:\\license.xml")
        # cam = cv2.VideoCapture(0)
        minW = 0.1 * self.video.get(3)
        minH = 0.1 * self.video.get(4)
        licenseStr = ""

        width = int(self.video.get(1))
        height = int(self.video.get(1))
        firstFrame = None

        number = 15

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

            if wheMove == False:
                for (x, y, w, h) in cars:
                    cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    img2gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                    imageVar = cv2.Laplacian(img2gray, cv2.CV_64F).var()
                    # print(imageVar)
                    if imageVar > 180:
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
                                # if number != 20:
                                #     number = number + 1
                                # params = {"image": img01}
                                # access_token = '24.9515cd4eb810ad1b9793ae4b1735f6d1.2592000.1629558405.282335-24591576'
                                # request_url = request_url + "?access_token=" + access_token
                                # headers = {'content-type': 'application/x-www-form-urlencoded'}
                                # response = requests.post(request_url, data=params, headers=headers)
                                # my_result = response.json()
                                #
                                # if response:
                                #     licenseStr = ''
                                #
                                #     newStr = my_result['words_result']['number']
                                #
                                #     if (newStr != licenseStr):
                                #         print(newStr)
                                #         # licenseStr = newStr
                                #
                                #         # 发送邮件
                                #         conntent = "这个是字符串"
                                #         msg.attach(MIMEText(conntent, 'plain', 'utf-8'))
                                #         msg['Subject'] = "这个是邮件主题"
                                #         msg['From'] = msg_from
                                #         s = smtplib.SMTP_SSL("smtp.qq.com", 465)
                                #         s.login(msg_from, passwd)
                                #         s.sendmail(msg_from, to, msg.as_string())
                                #         # print("邮件发送成功")
            cv2.waitKey(1)

if __name__ == '__main__':
    # video = input("输入摄像头地址")
    # rtmp_url = input("输入rtmp地址url")
    # email_url = input("输入email地址")
    video = 0
    rtmp_url = "rtmp://localhost:1935/live/home"
    email_url = "19301054@bjtu.edu.cn"


