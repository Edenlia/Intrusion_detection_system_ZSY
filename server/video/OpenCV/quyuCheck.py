import cv2
import numpy as np
from imutils.object_detection import non_max_suppression
import pygame
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#初始化方向梯度直方图描述子
hog = cv2.HOGDescriptor()
#设置支持向量机使得它成为一个预先训练好了的行人检测器
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

#读取摄像头视频
cap = cv2.VideoCapture(0)

while True:
    ret, img = cap.read()
    # 行人检测
    (rects, weights) = hog.detectMultiScale(img, winStride=(4, 4), padding=(8, 8), scale=1.05)
    # 设置来抑制重叠的框
    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
    pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
    # 绘制红色人体矩形框
    for (x, y, w, h) in pick:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
    # 绘制绿色对比框
    cv2.rectangle(img, (50, 50), (600, 450), (0, 255, 0), 2)
    # 绘制蓝色危险区域框
    cv2.rectangle(img, (350, 50), (600, 450), (255, 0, 0), 2)  # 原图 左上角坐标 有效角坐标  颜色 画线宽度
    # 打印检测到的目标个数
    # k = len(pick)
    if len(pick) > 0:
        print("检测到进入危险区域行人个数为{}".format(len(pick)))

        # 警报声
        file = r'music/baojing1.mp3'
        # 初始化
        pygame.mixer.init()
        # 加载音乐文件
        track = pygame.mixer.music.load(file)
        # 开始播放音乐流
        pygame.mixer.music.play()


        # 发送邮件提醒
        def send_email(msg_from, passwd, msg_to, text_content):
            msg = MIMEMultipart()
            subject = "危险报警"  # 主题
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


        msg_from = '1393371859@qq.com'  # 发送方邮箱
        passwd = 'vgfgezofbpcbibca'  # 填入发送方邮箱的授权码（就是刚刚你拿到的那个授权码）
        msg_to = '19301105@bjtu.edu.cn'  # 收件人邮箱
        text_content = "禁区有人进入，危险!"  # 发送的邮件内容
        # file_path = 'unknownData/User.2.2.jpg'  # 需要发送的附件目录
        send_email(msg_from, passwd, msg_to, text_content)

    # cv2.imshow("test", img)
    # print("检测到进入危险区域行人个数为{}".format(len(pick)))
    # 展示每一帧图像
    cv2.imshow("QuYuBaoJing", img)
    # 按esc键退出循环
    if cv2.waitKey(1) & 0xff == 27:
        break
#释放资源
cap.release()
cv2.destroyAllWindows()