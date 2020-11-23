# -*- coding: utf-8 -*-
#kanamori
#2020.11.23
#ver2.0
#open_wecamの編集→兼平君に手伝ってもらって完成したみたいです。金森の環境では映らなかったので確認お願いします。

import numpy as np
import cv2
import tkinter
import threading
import random
import time
from PIL import Image, ImageTk

class CameraImgExtractor:

    def __init__(self):
        self.cap = None
        self._WEB_CAMERA_NUMBER = 0

    def _open_webcam_stream(self):
        self.cap = cv2.VideoCapture(self._WEB_CAMERA_NUMBER)

    def exists_webcam(self):
        return True
    def read_img(self):
        return np.random.randint(0, 256, (300, 600))

    def release_webcam_stream(self):
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    camera_img_extractor = CameraImgExtractor()
    camera_img_extractor._open_webcam_stream()

    while 1:
        ret, frame = camera_img_extractor.cap.read()
        cv2.imshow('sample', frame)

        # k = cv2.waitkey(1)
        # if k == 27:
        #     break
    camera_img_extractor.release_webcam_stream()