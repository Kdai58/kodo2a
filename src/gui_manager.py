# -*- coding: utf-8 -*-

"""

作成者：兼平大輔
日付：2020.11.30
バージョン：12.0
変更内容：GuiManager.monitor()にwebカメラの画像を読み取る処理を追加する．
変更内容：GuiManagerの画像サイズの初期化処理を修正．
変更内容：GuiManagerに相対エントロピーを求める処理を追加．
変更内容：GuiManagerに絶対エントロピーを求める処理を追加．
変更内容：GuiManagerにwebカメラ接続エラー時の例外処理を追加．
変更内容：GuiManager.monitor()のwebカメラの存在を確認するif文を修正．


"""

import numpy as np
import cv2
import tkinter
import threading
import random
import time
from PIL import Image, ImageTk
from camera_img_extractor import CameraImgExtractor
from AbsoluteEntropyAnalyser import AbsoluteEntropyAnalyser
from relative_entropy_analyser import RelativeEntropyAnalyser

class GuiManager(tkinter.Frame):
	def __init__(self, master=None, sleep_sec=5):
		super().__init__(master)

		self._SLEEP_SEC = sleep_sec

        # webカメラ接続エラー用のアラートメッセージ
		self._ALERT_MESSAGE_FOR_WEBCAM_CONNECTION_ERROR = "エラー：ウェブカメラが見つかりません"

		# 絶対エントロピー
		self._absolute_entropy = 0

		# 相対エントロピー
		self._relative_entropy = 0

		# 部屋の乱雑度
		self._entropy_level = 1

		self.camera_img_extractor = CameraImgExtractor()

		# カラー画像を格納するndarray
		self._img_array = self.camera_img_extractor.read_img()

		# 画像のサイズ（webカメラから読み取った画像にサイズで初期化）
		self._IMG_WIDTH = self._img_array.shape[1]
		self._IMG_HEIGHT = self._img_array.shape[0]

		# 二値画像を格納するndarray
		self._binary_img = np.zeros((self._IMG_HEIGHT, self._IMG_WIDTH))

		self._PRAISE_STR = 'How beautiful your room is'
		self._NORMAL_STR = 'Endeavor putting your room in order'
		self._WARN_STR = 'How dirty your room is'

		master.geometry(f'{self._IMG_WIDTH}x{self._IMG_HEIGHT + 100}')

		# フレームの初期化
		self.master = master
		self.master.title('Room entropy checker')
		self.pack()

		# ボタンの設定
		self.start_btn = tkinter.Button(master, text='start', command=self.monitor_callback)
		self.destroy_btn = tkinter.Button(master, text='stop', command=self.destroy_gui)

		self.start_btn.pack(side='left', anchor=tkinter.S)
		self.destroy_btn.pack(side='left', anchor=tkinter.S)

		# 画像の描画
		self.img = ImageTk.PhotoImage(image=Image.fromarray(self._img_array))
		self.canvas = tkinter.Canvas(self.master, width=self._IMG_WIDTH, height=self._IMG_HEIGHT + 50)
		self.canvas.place(x=0, y=0)
		self.img_item = self.canvas.create_image(0, 0, image=self.img, anchor=tkinter.NW)

		# テキストの設定
		# アラートメッセージ
		self.alert_text_item = self.canvas.create_text(10, 0, text=self._NORMAL_STR, anchor=tkinter.NW, fill='white')

		# 絶対エントロピー
		self.absolute_entropy_text_item = self.canvas.create_text(10, 20, text="absolute entropy = " + str(self._absolute_entropy), anchor=tkinter.NW, fill='white')

		# 相対エントロピー
		self.relative_entropy_text_item = self.canvas.create_text(10, 40, text="relative entropy = " + str(self._relative_entropy), anchor=tkinter.NW, fill='white')

		# webカメラ接続エラー用のアラートメッセージ
		self.alert_text_for_webcam_connecting_error_item = self.canvas.create_text(10, self._IMG_HEIGHT + 10, text="", anchor=tkinter.NW)

	def monitor_callback(self):
		"""
        monitor()で行う処理を別スレッドで行う為のコールバック関数．
		"""

		thread = threading.Thread(target=self.monitor, args=())
		thread.setDaemon(True)
		thread.start()

	def monitor(self):
		"""
		一定時間ごとにwebカメラの画像を受け取り，絶対エントロピー，相対エントロピー，乱雑度を求め，GUIの表示を更新する．
		"""

		absolute_entropy_analyser = AbsoluteEntropyAnalyser()
		relative_entropy_analyser = RelativeEntropyAnalyser()

		i = 0

		# self._SLEEP_SEC毎に，webカメラから画像を読み取り，絶対エントロピー，相対エントロピー，乱雑度を求めてGUIを更新する．
		while (1):
			time.sleep(self._SLEEP_SEC)

			tmp_img_array = self.camera_img_extractor.read_img()
			if (self.camera_img_extractor.is_exist_webcam): # webカメラが存在するなら画像を読み取って，絶対エントロピー，相対エントロピー，乱雑度を求めてGUIを更新．
				self._img_array = tmp_img_array
				self._absolute_entropy = absolute_entropy_analyser.calc_absolute_entropy(self._img_array)
				self._relative_entropy = relative_entropy_analyser.calc_relative_entropy(self._img_array, self._absolute_entropy)
				self._entropy_level = self._to_entropy_level(self._relative_entropy)
				self.update_gui(entropy_level=self._entropy_level,
				                absolute_entropy=self._absolute_entropy,
				                relative_entropy=self._relative_entropy,
				                img_array=self._img_array,
				                alert_message="")
			else: # webカメラが存在しないなら，webカメラ接続エラーのアラートメッセージのみを更新する．
				self.update_gui(entropy_level=self._entropy_level,
					            absolute_entropy=self._absolute_entropy,
					            relative_entropy=self._relative_entropy,
					            img_array=self._img_array,
					            alert_message=self._ALERT_MESSAGE_FOR_WEBCAM_CONNECTION_ERROR)

			

			print(f"{i}:Updated")
			i += 1

	def update_gui(self, entropy_level, absolute_entropy, relative_entropy, img_array, alert_message):
		"""
		表示画像，アラートメッセージの表示，相対エントロピーの表示，絶対エントロピーの表示を更新する．

		Parameters
		----------
		entropy_level: int
		  乱雑度
		absolute_entropy: float
		  絶対エントロピー
		relative_entropy: float
		  相対エントロピー
		img_array: int[][]
		  表示画像
		 alert_message: str
		   webカメラ接続エラー時のアラートメッセージ
		"""
		self._print_img(img_array)

		self._print_exception(entropy_level)

		self._reprint_absolute_entropy(absolute_entropy)

		self._reprint_relative_entropy(relative_entropy)

		self._reprint_alert_message_for_webcam_connetction_error(alert_message)

	def _print_img(self, img_array):
		"""
		GUIに画像を表示する．

		Parameters
		----------
		img_array: int[][]
		  表示画像
		"""
		self.img = ImageTk.PhotoImage(image=Image.fromarray(img_array))
		self.canvas.itemconfig(self.img_item, image=self.img)

	def _print_exception(self, entropy_level):
		"""
		乱雑度に対応したアラートメッセージを表示する．

		Parameters
		----------
		entropy_level: int
		  相対エントロピー
		"""

		if entropy_level == 0:
			self.canvas.itemconfig(self.alert_text_item, text=self._PRAISE_STR, fill='green')
		elif entropy_level == 1:
			self.canvas.itemconfig(self.alert_text_item, text=self._NORMAL_STR, fill='white')
		else:
			self.canvas.itemconfig(self.alert_text_item, text=self._WARN_STR, fill='red')

	def _reprint_absolute_entropy(self, absolute_entropy):
		"""
		絶対エントロピーを表示

		Parameters
		----------
		absolute_entropy: float
		  絶対エントロピー
		"""

		self.canvas.itemconfig(self.absolute_entropy_text_item,
			                   text='absolute entropy = ' + str(absolute_entropy))

	def _reprint_relative_entropy(self, relative_entropy):
		"""
        相対エントロピーを表示する．

        Parameters
        ----------
        relative_entropy: float
	      相対エントロピー
		"""

		self.canvas.itemconfig(self.relative_entropy_text_item,
			                   text='relative entropy = ' + str(relative_entropy))

	def _reprint_alert_message_for_webcam_connetction_error(self, alert_message):
		"""
		webカメラ接続エラー時のアラートメッセージを更新する．

		Parameters
		----------
		alert_message: str
		  アラートメッセージ
		"""

		self.canvas.itemconfig(self.alert_text_for_webcam_connecting_error_item,
			                   text=alert_message)

	# 乱雑度を求める
	def _to_entropy_level(self, relative_entropy):
		"""
	    相対エントロピーを受け取り，乱雑度を求める．

	    Parameters
	    ----------
	    relative_entropy: float
	      相対エントロピー

	    Returns
	    -------
	    int
	      求めた乱雑度
	    """

		if 0 <= relative_entropy and relative_entropy < 1:
			return 0
		elif 1 <= relative_entropy and relative_entropy < 2:
			return 1
		else:
			return 2

	def destroy_gui(self):
		"""
		GUIを停止する．
		"""
		self.master.destroy()


# if __name__ == "__main__":
# 	root = tkinter.Tk()
# 	dlg = GuiManager(master=root)
# 	dlg.mainloop()
