# -*- coding: utf-8 -*-

"""

作成者：金森三尭，兼平大輔
日付：2020.11.29
バージョン：5.0
変更内容：open_wecamの編集→兼平君に手伝ってもらって完成したみたいです。金森の環境では映らなかったので確認お願いします。
変更内容：read_img()に，webカメラから読み取った画像をリサイズする処理を追加．縮小率はとりあえず2にしている．
変更内容：webカメラの有無によって出力を変える
変更内容：read_img()の例外処理を修正．

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
        self._WEB_CAMERA_NUMBER = 0
        self._REDUCTION_RATIO = 2
        self.is_exist_webcam = False
        self._open_webcam_stream()

    def _open_webcam_stream(self):
        # self.cap = cv2.VideoCapture(self._WEB_CAMERA_NUMBER)
        try:
            self.cap = cv2.VideoCapture(self._WEB_CAMERA_NUMBER)
            self.is_exist_webcam = True
        except cv2.error:
            self.is_exist_webcam = False


    def exists_webcam(self):
        return self.is_exist_webcam

    def read_img(self):
        # 常にis_exist_webcam == Trueになってしまうので，とりあえずコメントアウト．
        # try:
        #     ret, frame = self.cap.read()
        #     self.is_exist_webcam = True
        # except cv2.error:
        #     self.is_exist_webcam = False
        # frame = cv2.resize(frame, (frame.shape[1] // self._REDUCTION_RATIO, frame.shape[0] // self._REDUCTION_RATIO))
        # return frame

        ret, frame = self.cap.read()

        if (ret != True):
            self.is_exist_webcam = False
            return frame

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_rgb = cv2.resize(frame_rgb, (frame_rgb.shape[1] // self._REDUCTION_RATIO, frame_rgb.shape[0] // self._REDUCTION_RATIO))
        return frame_rgb

    def release_webcam_stream(self):
        self.cap.release()
        cv2.destroyAllWindows()

# デバッグ文
# if __name__ == "__main__":
#     camera_img_extractor = CameraImgExtractor()
#     print(f"open webcam stream:{camera_img_extractor.is_exist_webcam}")

#     i = 0
#     while 1:
#         frame = camera_img_extractor.read_img()
#         print(f"{i}:read image:{camera_img_extractor.is_exist_webcam}")

#         if (type(frame) != None):
#             cv2.imshow('sample', frame)

#         k = cv2.waitKey(1)
#         if k == 27:
#             break

#         i += 1
#         time.sleep(3)
#     camera_img_extractor.release_webcam_stream()