# -*- coding: utf-8 -*-

"""

作成者：兼平大輔
日付：2020.11.16
バージョン：5.0
変更内容：GUIのレイアウトを修正．

"""

import numpy as np
import cv2
import tkinter
import threading
import random
import time
from PIL import Image, ImageTk

class GuiManager(tkinter.Frame):
	def __init__(self, master=None):
		super().__init__(master)

		# 画像のサイズ（とりあえず600x300にしてある）
		self._IMG_WIDTH = 600
		self._IMG_HEIGHT = 300

		self._PRAISE_STR = 'How beautiful your room is'
		self._NORMAL_STR = 'Endeavor putting your room in order'
		self._WARN_STR = 'How dirty your room is'

		# 画像のピクセルを格納するndarray
		self._img_array = np.full((self._IMG_HEIGHT, self._IMG_WIDTH), 255, dtype=float)
		self._binary_img = np.zeros((self._IMG_HEIGHT, self._IMG_WIDTH))

		master.geometry(f'{self._IMG_WIDTH}x{self._IMG_HEIGHT + 100}')

		# フレームの初期化
		self.master = master
		self.master.title('Room entropy checker')
		self.pack()

		# ボタンの設定
		self.destroy_btn = tkinter.Button(master, text='stop', command=self.destroy_gui)
		self.start_btn = tkinter.Button(master, text='start', command=self.monitor_callback)

		self.destroy_btn.pack(side='bottom')
		self.start_btn.pack(side='bottom')

		# 画像の描画
		self.img = ImageTk.PhotoImage(image=Image.fromarray(self._img_array))
		self.canvas = tkinter.Canvas(self.master, width=self._IMG_WIDTH, height=self._IMG_HEIGHT)
		self.canvas.place(x=0, y=0)
		self.img_item = self.canvas.create_image(0, 0, image=self.img, anchor=tkinter.NW)

		# テキストの設定
		# アラートメッセージ
		self.alert_text_item = self.canvas.create_text(10, 0, text=self._NORMAL_STR, anchor=tkinter.NW)

		# 絶対エントロピー
		self.absolute_entropy_text_item = self.canvas.create_text(10, 20, text="absolute entropy = " + '0', anchor=tkinter.NW)

		# 相対エントロピー
		self.relative_entropy_text_item = self.canvas.create_text(10, 40, text="relative entropy = " + '0', anchor=tkinter.NW)

    # 監視処理を別スレッドで実行する
	def monitor_callback(self):
		thread = threading.Thread(target=self.monitor, args=())
		thread.setDaemon(True)
		thread.start()

	def monitor(self):
		i = 0

		# ここに部屋の監視の処理を書く．
		# 今はとりあえず３秒毎に，アラートメッセージの更新と画像の切り替えを行なっている．
		while (1):
			time.sleep(3)
			absolute_entropy = i % 3
			relative_entropy = i % 3
			entropy_level = self._to_entropy_level(relative_entropy)
			self.update_gui(entropy_level=entropy_level, 
				absolute_entropy=absolute_entropy, 
				relative_entropy=relative_entropy, 
				img_array=self._img_array)
			self._img_array[i % self._IMG_HEIGHT] = np.full(self._IMG_WIDTH, 0)
			print(self._img_array[i % 600])
			print(i)
			i += 1

    # room_entropyの値に応じてアラートメッセージを更新する
	def update_gui(self, entropy_level, absolute_entropy, relative_entropy, img_array):
		self._print_img(img_array)

		self._print_exception(entropy_level)

		self._reprint_absolute_entropy(absolute_entropy)

		self._reprint_relative_entropy(relative_entropy)

	# 画像の描画
	def _print_img(self, img_array):
		self.img = ImageTk.PhotoImage(image=Image.fromarray(img_array))
		self.canvas.itemconfig(self.img_item, image=self.img)

	# アラートの表示
	def _print_exception(self, entropy_level):
		if entropy_level == 0:
			self.canvas.itemconfig(self.alert_text_item, text=self._PRAISE_STR, fill='green')
		elif entropy_level == 1:
			self.canvas.itemconfig(self.alert_text_item, text=self._NORMAL_STR, fill='black')
		else:
			self.canvas.itemconfig(self.alert_text_item, text=self._WARN_STR, fill='red')

	# 絶対エントロピーを表示
	def _reprint_absolute_entropy(self, absolute_entropy):
		self.canvas.itemconfig(self.absolute_entropy_text_item, text='absolute entropy = ' + str(absolute_entropy))

	# 相対エントロピーを表示
	def _reprint_relative_entropy(self, relative_entropy):
		self.canvas.itemconfig(self.relative_entropy_text_item, text='relative entropy = ' + str(relative_entropy))

	# 乱雑度のレベルを求める
	def _to_entropy_level(self, relative_entropy):
		if relative_entropy == 0:
			return 0
		elif relative_entropy == 1:
			return 1
		else:
			return 2

	def destroy_gui(self):
		self.master.destroy()


if __name__ == "__main__":
	root = tkinter.Tk()
	dlg = GuiManager(master=root)
	dlg.mainloop()
