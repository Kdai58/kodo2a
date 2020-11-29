# -*- coding: utf-8 -*-

"""

作成者：金森三尭，兼平大輔
日付：2020.11.29
バージョン：4.0
変更内容：open_wecamの編集→兼平君に手伝ってもらって完成したみたいです。金森の環境では映らなかったので確認お願いします。
変更内容：read_img()に，webカメラから読み取った画像をリサイズする処理を追加．縮小率はとりあえず2にしている．
変更内容：webカメラの有無によって出力を変える

"""

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
        self._WEB_CAMERA_NUMBER = 1
        self._REDUCTION_RATIO = 2
        self._open_webcam_stream()
        self.is_exist_webcam = False

    def _open_webcam_stream(self):
        # self.cap = cv2.VideoCapture(self._WEB_CAMERA_NUMBER)
        try:
            self.cap = cv2.VideoCapture(self._WEB_CAMERA_NUMBER)
            self.is_exist_webcam = True
        except cv2.error:
            self.is_exist_webcam = False


    def exists_webcam(self):
        # while(True):
        #     ret, frame = self.cap.read()
        #     if ret == False:
        #         print("fialed to open webcam")
        #         break
        # else:
        return self.is_exist_webcam

    def read_img(self):
        try:
            ret, frame = self.cap.read()
            self.is_exist_webcam = True
        except cv2.error:
            self.is_exist_webcam = False
        frame = cv2.resize(frame, (frame.shape[1] // self._REDUCTION_RATIO, frame.shape[0] // self._REDUCTION_RATIO))
        return frame

    def release_webcam_stream(self):
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    camera_img_extractor = CameraImgExtractor()
    print(f"open webcam stream:{camera_img_extractor.is_exist_webcam}")

    while 1:
        ret, frame = camera_img_extractor.cap.read()
        print(f"read image:{camera_img_extractor.is_exist_webcam}")
        cv2.imshow('sample', frame)

        k = cv2.waitKey(1)
        if k == 27:
            break
    camera_img_extractor.release_webcam_stream()