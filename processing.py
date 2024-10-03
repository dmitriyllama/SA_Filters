from abc import ABC
import cv2

class Filter(ABC):
    def __init__(self, outputs: list):
        self.outputs = outputs

    def input(self, frame):
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
            if not ret:
                print("End of video " + self.file)
                break
            if cv2.waitKey(1) == ord('q'):
                break
            for out in self.outputs:
                out(frame)
        self.capture.release()


class Display():
    def __init__(self, name: str, outputs: list):
        self.name = name
        self.outputs = outputs

    def show(self, frame):
        cv2.imshow(self.name, frame)
        for out in self.outputs:
            out(frame)