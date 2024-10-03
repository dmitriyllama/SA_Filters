from abc import ABC
import cv2
from multiprocessing import Process, Queue

class Filter(ABC):
    def __init__(self, outputs: list):
        self.queue = Queue()
        self.outputs = outputs
        self.process = None

    def input(self, frame):
        self.queue.put(frame)
        if self.process == None:
            self.process = Process(target=self.work)
            self.process.start()

    def work(self):
        while True:
            frame = self.queue.get()
            if frame is None:
                self.process.close()
                self.process = None
                for out in self.outputs:
                    out(None)
                break
            result = self.__apply(frame)
            for out in self.outputs:
                out(result)

class GrayscaleFilter(Filter):
    def _Filter__apply(self, frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

class MirrorFilter(Filter):
    def _Filter__apply(self, frame):
        return cv2.flip(frame, 1)

class ResizeFilter(Filter):
    def __init__(self, outputs, x, y):
        super().__init__(outputs)
        self.x = x
        self.y = y

    def _Filter__apply(self, frame):
        return cv2.resize(frame, (self.x, self.y))

class ColorFilter(Filter):
    def __init__(self, outputs, code):
        super().__init__(outputs)
        self.code = code

    def _Filter__apply(self, frame):
        return cv2.cvtColor(frame, self.code)


class VideoFileSource():
    def __init__(self, file: str, outputs: list):
        self.capture = cv2.VideoCapture(file)
        if not self.capture.isOpened():
            print("Error: Could not open video")
            exit()
        self.outputs = outputs

    def start(self):
        while True:
            ret, frame = self.capture.read()
            if cv2.waitKey(1) == ord('q'):
                ret = False
            if not ret:
                print("Video ended")
                for out in self.outputs:
                    out(None)
                break
            for out in self.outputs:
                out(frame)
        self.capture.release()


class Display():
    def __init__(self, name: str, outputs: list):
        self.queue = Queue()
        self.name = name
        self.outputs = outputs
        self.process = None

    def input(self, frame):
        self.queue.put(frame)
        if self.process == None:
            self.process = Process(target=self.work)
            self.process.start()

    def work(self):
        while True:
            cv2.waitKey(1)
            frame = self.queue.get()
            if frame is None:
                self.process.close()
                self.process = None
                cv2.destroyWindow(self.name)
                for out in self.outputs:
                    out(None)
                break
            cv2.imshow(self.name, frame)
            for out in self.outputs:
                out(frame)