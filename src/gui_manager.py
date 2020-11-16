# -*- coding: utf-8 -*-

"""

作成者：兼平大輔
日付：2020.11.16
バージョン：3.0
変更内容：絶対エントロピー，相対エントロピーを描画する処理を追加．

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
		self.__img

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
		# アラートメッセージ
		self.alert_text = tkinter.StringVar()
		self.alert_text.set(self.NORMAL_STR)
		self.alert_text_label = tkinter.Label(master, textvariable=self.alert_text)

		# 絶対エントロピー
		self.absolute_entropy_text = tkinter.StringVar()
		self.absolute_entropy_text.set('absolute entropy = ' + '0')
		self.absolute_entropy_text_label = tkinter.Label(self.master, textvariable=self.absolute_entropy_text)

		# 相対エントロピー
		self.relative_entropy_text = tkinter.StringVar()
		self.relative_entropy_text.set('relative entropy = ' + '0')
		self.relative_entropy_text_label = tkinter.Label(self.master, textvariable=self.relative_entropy_text)


		self.alert_text_label.pack(side='bottom', expand=1)
		self.absolute_entropy_text_label.pack(side='left', expand=1)
		self.relative_entropy_text_label.pack(side='left', expand=1)

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
			absolute_entropy = i % 3
			relative_entropy = i % 3
			entropy_level = self.__to_entropy_level(relative_entropy)
			self.update_gui(entropy_level=entropy_level, 
				absolute_entropy=absolute_entropy, 
				relative_entropy=relative_entropy, 
				img_array=self.__img_array)
			self.__img_array[i % 600] = np.full(300, 255)
			print(self.__img_array[i % 600])
			print(i)
			i += 1

    # room_entropyの値に応じてアラートメッセージを更新する
	def update_gui(self, entropy_level, absolute_entropy, relative_entropy, img_array):
		self.__print_img(img_array)

		self.__print_exception(entropy_level)

		self.__reprint_absolute_entropy(absolute_entropy)

		self.__reprint_relative_entropy(relative_entropy)

	# 画像の描画
	def __print_img(self, __img_array):
		self.img = ImageTk.PhotoImage(image=Image.fromarray(__img_array))
		self.canvas.itemconfig(self.item, image=self.img)

	# アラートの表示
	def __print_exception(self, entropy_level):
		if entropy_level == 0:
			self.alert_text_label.config(fg='green')
			self.alert_text.set(self.PRAISE_STR)
		elif entropy_level == 1:
			self.alert_text_label.config(fg='black')
			self.alert_text.set(self.NORMAL_STR)
		else:
			self.alert_text_label.config(fg='red')
			self.alert_text.set(self.WARN_STR)

	# 絶対エントロピーを表示
	def __reprint_absolute_entropy(self, absolute_entropy):
		self.absolute_entropy_text.set('absolute entropy = ' + str(absolute_entropy))

	# 相対エントロピーを表示
	def __reprint_relative_entropy(self, relative_entropy):
		self.relative_entropy_text.set('relative entropy = ' + str(relative_entropy))

	# 乱雑度のレベルを求める
	def __to_entropy_level(self, relative_entropy):
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
