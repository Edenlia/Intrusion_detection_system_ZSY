from django.http import HttpResponse, StreamingHttpResponse

from django.views.decorators.csrf import csrf_exempt
import cv2
import threading
from django.views.decorators import gzip


class VideoCameras(object):
    def __init__(self):
        self.cameras = []


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


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@gzip.gzip_page
@csrf_exempt
def test1(request):
    try:
        cam = VideoCamera("rtmp://localhost:1935/live/home")
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except BaseException:  # This is bad! replace it with proper handling
        pass


@gzip.gzip_page
@csrf_exempt
def test2(request):
    try:
        cam = VideoCamera('http://admin:12345@192.168.43.1:8081/')
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        pass


