import cv2
import numpy as np
import cv2 as cv
import time
from imutils.object_detection import non_max_suppression
import imutils
import pygame
# 调用成熟的库，识别陌生人大概特征
# 识别陌生人一直存在
def stretch(img):
    '''
    图像拉伸函数
    '''
    maxi = float(img.max())
    mini = float(img.min())

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img[i, j] = (255 / (maxi - mini) * img[i, j] - (255 * mini) / (maxi - mini))
    return img


def dobinaryzation(img):
    '''
    二值化处理函数
    '''
    maxi = float(img.max())
    mini = float(img.min())

    x = maxi - ((maxi - mini) / 2)
    # 二值化,返回阈值ret  和  二值化操作后的图像thresh
    ret, thresh = cv2.threshold(img, x, 255, cv2.THRESH_BINARY)
    # 返回二值化后的黑白图像
    return thresh


def find_rectangle(contour):
    '''
    寻找矩形轮廓
    '''
    y, x = [], []

    for p in contour:
        y.append(p[0][0])
        x.append(p[0][1])

    return [min(y), min(x), max(y), max(x)]


def locate_license(img, afterimg):
    '''
    定位车牌号
    '''
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 找出最大的三个区域
    block = []
    for c in contours:
        # 找出轮廓的左上点和右下点，由此计算它的面积和长度比
        r = find_rectangle(c)
        a = (r[2] - r[0]) * (r[3] - r[1])  # 面积
        s = (r[2] - r[0]) * (r[3] - r[1])  # 长度比

        block.append([r, a, s])
    # 选出面积最大的3个区域
    block = sorted(block, key=lambda b: b[1])[-3:]

    # 使用颜色识别判断找出最像车牌的区域
    maxweight, maxindex = 0, -1
    for i in range(len(block)):
        b = afterimg[block[i][0][1]:block[i][0][3], block[i][0][0]:block[i][0][2]]
        # BGR转HSV
        hsv = cv2.cvtColor(b, cv2.COLOR_BGR2HSV)
        # 蓝色车牌的范围
        lower = np.array([100, 50, 50])
        upper = np.array([140, 255, 255])
        # 根据阈值构建掩膜
        mask = cv2.inRange(hsv, lower, upper)
        # 统计权值
        w1 = 0
        for m in mask:
            w1 += m / 255

        w2 = 0
        for n in w1:
            w2 += n

        # 选出最大权值的区域
        if w2 > maxweight:
            maxindex = i
            maxweight = w2

    return block[maxindex][0]


def find_license(img):
    '''
    预处理函数
    '''
    m = 400 * img.shape[0] / img.shape[1]

    # 压缩图像
    img = cv2.resize(img, (400, int(m)), interpolation=cv2.INTER_CUBIC)

    # BGR转换为灰度图像
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 灰度拉伸
    stretchedimg = stretch(gray_img)

    '''进行开运算，用来去除噪声'''
    r = 16
    h = w = r * 2 + 1
    kernel = np.zeros((h, w), np.uint8)
    cv2.circle(kernel, (r, r), r, 1, -1)
    # 开运算
    openingimg = cv2.morphologyEx(stretchedimg, cv2.MORPH_OPEN, kernel)
    # 获取差分图，两幅图像做差  cv2.absdiff('图像1','图像2')
    strtimg = cv2.absdiff(stretchedimg, openingimg)

    # 图像二值化
    binaryimg = dobinaryzation(strtimg)

    # canny边缘检测
    canny = cv2.Canny(binaryimg, binaryimg.shape[0], binaryimg.shape[1])

    '''消除小的区域，保留大块的区域，从而定位车牌'''
    # 进行闭运算
    kernel = np.ones((5, 19), np.uint8)
    closingimg = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, kernel)

    # 进行开运算
    openingimg = cv2.morphologyEx(closingimg, cv2.MORPH_OPEN, kernel)

    # 再次进行开运算
    kernel = np.ones((11, 5), np.uint8)
    openingimg = cv2.morphologyEx(openingimg, cv2.MORPH_OPEN, kernel)

    # 消除小区域，定位车牌位置
    rect = locate_license(openingimg, img)

    return rect, img


def cut_license(afterimg, rect):
    '''
    图像分割函数
    '''
    # 转换为宽度和高度
    rect[2] = rect[2] - rect[0]
    rect[3] = rect[3] - rect[1]
    rect_copy = tuple(rect.copy())
    rect = [0, 0, 0, 0]
    # 创建掩膜
    mask = np.zeros(afterimg.shape[:2], np.uint8)
    # 创建背景模型  大小只能为13*5，行数只能为1，单通道浮点型
    bgdModel = np.zeros((1, 65), np.float64)
    # 创建前景模型
    fgdModel = np.zeros((1, 65), np.float64)
    # 分割图像
    cv2.grabCut(afterimg, mask, rect_copy, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    img_show = afterimg * mask2[:, :, np.newaxis]

    return img_show


def deal_license(licenseimg):
    '''
    车牌图片二值化
    '''
    # 车牌变为灰度图像
    gray_img = cv2.cvtColor(licenseimg, cv2.COLOR_BGR2GRAY)

    # 均值滤波  去除噪声
    kernel = np.ones((3, 3), np.float32) / 9
    gray_img = cv2.filter2D(gray_img, -1, kernel)

    # 二值化处理
    ret, thresh = cv2.threshold(gray_img, 120, 255, cv2.THRESH_BINARY)

    return thresh


def find_end(start, arg, black, white, width, black_max, white_max):
    end = start + 1
    for m in range(start + 1, width - 1):
        if (black[m] if arg else white[m]) > (0.98 * black_max if arg else 0.98 * white_max):
            end = m
            break
    return end


# 神经网络实现人的年龄及性别预测
# 检测人脸并绘制人脸bounding box
def getFaceBox(net, frame, conf_threshold=0.7):
    frameOpencvDnn = frame.copy()
    frameHeight = frameOpencvDnn.shape[0]  # 高就是矩阵有多少行
    frameWidth = frameOpencvDnn.shape[1]  # 宽就是矩阵有多少列
    blob = cv.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)
    #  blobFromImage(image[, scalefactor[, size[, mean[, swapRB[, crop[, ddepth]]]]]]) -> retval  返回值   # swapRB是交换第一个和最后一个通道   返回按NCHW尺寸顺序排列的4 Mat值
    net.setInput(blob)
    detections = net.forward()  # 网络进行前向传播，检测人脸
    bboxes = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:
            x1 = int(detections[0, 0, i, 3] * frameWidth)
            y1 = int(detections[0, 0, i, 4] * frameHeight)
            x2 = int(detections[0, 0, i, 5] * frameWidth)
            y2 = int(detections[0, 0, i, 6] * frameHeight)
            bboxes.append([x1, y1, x2, y2])  # bounding box 的坐标
            cv.rectangle(frameOpencvDnn, (x1, y1), (x2, y2), (0, 255, 0), int(round(frameHeight / 150)),
                         8)  # rectangle(img, pt1, pt2, color[, thickness[, lineType[, shift]]]) -> img
    return frameOpencvDnn, bboxes


# 网络模型  和  预训练模型
faceProto = "age_gender/opencv_face_detector.pbtxt"
faceModel = "age_gender/opencv_face_detector_uint8.pb"

ageProto = "age_gender/age_deploy.prototxt"
ageModel = "age_gender/age_net.caffemodel"

genderProto = "age_gender/gender_deploy.prototxt"
genderModel = "age_gender/gender_net.caffemodel"

# 模型均值
MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-30)', '(38-43)', '(48-53)', '(60-100)']
genderList = ['Male', 'Female']

# 加载网络
ageNet = cv.dnn.readNet(ageModel, ageProto)
genderNet = cv.dnn.readNet(genderModel, genderProto)

# 人脸检测的网络和模型
faceNet = cv.dnn.readNet(faceModel, faceProto)
padding = 20

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('TrainData/train.yml')
# gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# new_faces = face_detector.detectMultiScale(gray)
cascadePath = r'cv2-Haar\haarcascade_frontalface_alt.xml'
faceCascade = cv2.CascadeClassifier(cascadePath)

faceCascade02 = cv2.CascadeClassifier(r'cv2-Haar\haarcascade_licence_plate_rus_16stages.xml')

font = cv2.FONT_HERSHEY_SIMPLEX

idnum = 0  # id与names数组里面的不相同，相差1
# names = ['yy', 'yx', 'yz']  # names中存储人的名字，若该人id为0则他的名字在第一位，id位1则排在第二位，以此类推。
#初始化方向梯度直方图描述子
hog = cv2.HOGDescriptor()
# 行人检测器
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cam = cv2.VideoCapture(0)
minW = 0.1 * cam.get(3)
minH = 0.1 * cam.get(4)

while True:
    ret, img = cam.read()
    t = time.time()
    # 每帧图像roi区域扣出来
    # roi = img[50:450,350:600]
    #行人检测
    (rects, weights) = hog.detectMultiScale(img, winStride=(4, 4), padding=(8, 8), scale=1.05)
    #设置来抑制重叠的框
    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
    pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
    # 绘制红色人体矩形框
    for (x, y, w, h) in pick:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
    # 绘制绿色对比框
    cv2.rectangle(img, (50, 50), (600, 450), (0, 255, 0), 2)
    # 绘制蓝色危险区域框
    cv2.rectangle(img, (350, 50), (600, 450), (255, 0, 0), 2)# 原图 左上角坐标 有效角坐标  颜色 画线宽度
    # 打印检测到的目标个数
    # k = int(len(pick))
    if len(pick) > 0:
        print("检测到进入危险区域行人个数为{}".format(len(pick)))

        # 警报声
        file = r'beijing.mp3'
        # 初始化
        pygame.mixer.init()
        # 加载音乐文件
        track = pygame.mixer.music.load(file)
        # 开始播放音乐流
        pygame.mixer.music.play()

    cv2.imshow("test", img)

    hasFrame, frame = cam.read()
    frame = cv.flip(frame, 1)
    if not hasFrame:
        cv.waitKey()
        break

    img, bboxes = getFaceBox(faceNet, frame)
    if not bboxes:
        print("No face Detected, Checking next frame")
        continue

    for bbox in bboxes:
        # 取出box框住的脸部进行检测,返回的是脸部图片
        face = frame[max(0, bbox[1] - padding):min(bbox[3] + padding, frame.shape[0] - 1),
               max(0, bbox[0] - padding):min(bbox[2] + padding, frame.shape[1] - 1)]
        blob = cv.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
        genderNet.setInput(blob)  # blob输入网络进行性别的检测
        genderPreds = genderNet.forward()  # 性别检测进行前向传播
        gender = genderList[genderPreds[0].argmax()]  # 分类  返回性别类型
        ageNet.setInput(blob)
        agePreds = ageNet.forward()
        age = ageList[agePreds[0].argmax()]
        label = "{},{}".format(gender, age)
        cv.putText(img, label, (bbox[0], bbox[1] - 10), cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 1,
                   cv.LINE_AA)
        # cv.imshow("Age Gender Demo", img)


    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(int(minW), int(minH)))
    cars = faceCascade02.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        idnum, confidence = recognizer.predict(gray[y:y + h, x:x + w])
        # 函数cv2.face_FaceRecognizer.predict()
        # 在对一个待测人脸图像进行判断时，会寻找与当前图像距离最近的人脸图像。与哪个人脸图像最接近，就将待测图像识别为其对应的标签。
        # confiidence 0 完全匹配 <50 可以接受 >80 差别较大
        print(confidence)
        if 0 < confidence < 70:
            # idnum = names[idnum]
            confidence = "{0}%".format(round(100 - confidence))
            print("welcome")
        else:
            idnum = "unknown"
            confidence = "{0}%".format(round(100 - confidence))
            print("bad people")

            # 保存整体图片或者只保存一个脸部图片
            face_detector = cv2.CascadeClassifier(r'cv2-Haar\haarcascade_frontalface_alt.xml')
            faces = face_detector.detectMultiScale(gray, 1.3, 5)
            count = 0
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + w), (255, 0, 0))
                count += 1
                # 保存图像
                cv2.imwrite("unknownData/wrong-" + str(time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))) + '.jpg', gray[y: y + h, x: x + w])
            # 发出警报声
            file = r'beijing.mp3'
            # 初始化
            pygame.mixer.init()
            # 加载音乐文件
            track = pygame.mixer.music.load(file)
            # 开始播放音乐流
            pygame.mixer.music.play()

        cv2.putText(img, str(idnum), (x + 5, y - 5), font, 1, (0, 0, 255), 1)
        cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (0, 0, 0), 1)

        for (x, y, w, h) in cars:
            img2gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            imageVar = cv2.Laplacian(img2gray, cv2.CV_64F).var()
            print(imageVar)

            if (imageVar > 180):
            # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.imshow('found', img)

                rect, afterimg = find_license(img)
            # 框出车牌号
            # cv2.rectangle(afterimg, (rect[0], rect[1]), (rect[2], rect[3]), (0, 255, 0), 2)
            # cv2.imshow('afterimg', afterimg)
            # 分割车牌与背景
                cutimg = cut_license(afterimg, rect)
                cv2.imshow('cutimg', cutimg)
            # 二值化生成黑白图
            # thresh = deal_license(cutimg)
            # cv2.imshow('thresh', thresh)
            # cv2.waitKey(0)
            # # 记录黑白像素总和
            # white = []
            # black = []
            # height = thresh.shape[0]  # 263
            # width = thresh.shape[1]  # 400
            # # print('height',height)
            # # print('width',width)
            # white_max = 0
            # black_max = 0
            # # 计算每一列的黑白像素总和
            # for i in range(width):q
            #     line_white = 0
            #     line_black = 0
            #     for j in range(height):
            #         if thresh[j][i] == 255:
            #             line_white += 1
            #         if thresh[j][i] == 0:
            #             line_black += 1
            #     white_max = max(white_max, line_white)
            #     black_max = max(black_max, line_black)
            #     white.append(line_white)
            #     black.append(line_black)
            # # arg为true表示黑底白字，False为白底黑字
            # arg = True
            # if black_max < white_max:
            #     arg = False
            #
            # n = 1
            # start = 1
            # end = 2
            # while n < width - 2:
            #     n += 1
            #     # 判断是白底黑字还是黑底白字  0.05参数对应上面的0.95 可作调整
            #     if (white[n] if arg else black[n]) > (0.02 * white_max if arg else 0.02 * black_max):
            #         start = n
            #         end = find_end(start, arg, black, white, width, black_max, white_max)
            #         n = end
            #         if end - start > 5:
            #             cj = thresh[1:height, start:end]
            #             # cv2.imshow('cutlicense', cj)
            #             cv2.waitKey(0)
    # cv2.resizeWindow('camera', 500, 500)
    cv2.imshow('camera', img)
    k = cv2.waitKey(10)
    if k == 27:
        break

cam.release()
cv2.destroyAllWindows()
