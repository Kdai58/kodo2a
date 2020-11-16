# -*- coding: utf-8 -*-

"""

作成者：兼平大輔
日付：2020.11.16
バージョン：2.0
変更内容：画像描画処理を追加．

"""

import numpy as np
import cv2
import tkinter
import threading
import random
import time
from PIL import Image, ImageTk

WEB_CAMERA_NUMBER = 1

class GuiManager(tkinter.Frame):
	def __init__(self, master=None):
		super().__init__(master)

		self.PRAISE_STR = 'How beautiful your room is'
		self.NORMAL_STR = 'Endeavor putting your room in order'
		self.WARN_STR = 'How dirty your room is'

		self.__img_array = np.zeros((600, 300))

		master.geometry('600x400')

		# フレームの初期化
		self.master = master
		self.master.title('Room entropy checker')
		self.pack()

		# ボタンの設定
		self.destroy_btn = tkinter.Button(master, text='stop', command=self.destroy_gui)
		self.start_btn = tkinter.Button(master, text='start', command=self.monitor_callback)

		self.destroy_btn.pack(side='bottom')
		self.start_btn.pack(side='bottom')

		# テキストの設定
		self.alert_text = tkinter.StringVar()
		self.alert_text.set(self.NORMAL_STR)
		self.alert_text_label = tkinter.Label(master, textvariable=self.alert_text)

		self.alert_text_label.pack(side='bottom', expand=1)

		# 画像の描画
		self.img = ImageTk.PhotoImage(image=Image.fromarray(self.__img_array))
		self.canvas = tkinter.Canvas(self.master, width=600, height=300)
		self.canvas.place(x=100, y=40)
		self.item = self.canvas.create_image(30, 30, image=self.img, anchor=tkinter.NW)

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
			self.update_gui(i % 3, self.__img_array)
			self.__img_array[i % 600] = np.full(300, 255)
			print(self.__img_array[i % 600])
			print(i)
			i += 1

    # room_entropyの値に応じてアラートメッセージを更新する
	def update_gui(self, room_entropy, __img_array):
		self.__print_img(__img_array)

		if room_entropy == 0:
			self.alert_text_label.config(fg='green')
			self.alert_text.set(self.PRAISE_STR)
		elif room_entropy == 1:
			self.alert_text_label.config(fg='black')
			self.alert_text.set(self.NORMAL_STR)
		else:
			self.alert_text_label.config(fg='red')
			self.alert_text.set(self.WARN_STR)

	def __print_img(self, __img_array):
		self.img = ImageTk.PhotoImage(image=Image.fromarray(__img_array))
		self.canvas.itemconfig(self.item, image=self.img)

	def destroy_gui(self):
		self.master.destroy()


if __name__ == "__main__":
	root = tkinter.Tk()
	dlg = GuiManager(master=root)
	dlg.mainloop()
