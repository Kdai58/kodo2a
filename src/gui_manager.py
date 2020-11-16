# -*- coding: utf-8 -*-
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

		master.geometry('600x400')

		# フレームの初期化
		self.master = master
		self.master.title('Room entropy checker')
		self.pack()

		# MainPanel を 全体に配置
		self.mainpanel = tkinter.Label(root)
		self.mainpanel.pack(expand=1)

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

		# webカメラの映像の描画が開始されたかを表すフラグ
		self.is_capture_started = False

		# webカメラの映像の描画を開始
		self.start_cap()

    # 監視処理を別スレッドで実行する
	def monitor_callback(self):
		thread = threading.Thread(target=self.monitor, args=())
		thread.setDaemon(True)
		thread.start()

	def monitor(self):
		i = 0

		# ここに部屋の監視の処理を書く．
		# 今はとりあえず3秒毎にアラートメッセージを更新する処理が書いてある．
		while (1):
			time.sleep(3)
			self.update_gui(i % 3)
			print(i)
			i += 1

    # room_entropyの値に応じてアラートメッセージを更新する
	def update_gui(self, room_entropy):
		if room_entropy == 0:
			self.alert_text_label.config(fg='green')
			self.alert_text.set(self.PRAISE_STR)
		elif room_entropy == 1:
			self.alert_text_label.config(fg='black')
			self.alert_text.set(self.NORMAL_STR)
		else:
			self.alert_text_label.config(fg='red')
			self.alert_text.set(self.WARN_STR)


	def destroy_gui(self):
		self.stop_cap()
		self.master.destroy()

	def start_cap(self):
		if not self.is_capture_started:
			self.is_capture_started = True
			self.cap = cv2.VideoCapture(WEB_CAMERA_NUMBER)
			self.after_id = self.after(33, self.update_cap)

	def update_cap(self):
		ret, frame = self.cap.read()
		if ret:
			frame = cv2.resize(frame, (600, 300), interpolation=cv2.INTER_LANCZOS4)
			imgtk = ImageTk.PhotoImage(image=Image.fromarray(frame))
			self.mainpanel.imgtk = imgtk
			self.mainpanel.configure(image=imgtk)
		
		self.after_id = self.after(33, self.update_cap)

	def stop_cap(self):
		self.after_cancel(self.after_id)
		self.cap.release()
		cv2.destroyAllWindows()
		self.is_capture_started = False


if __name__ == "__main__":
	root = tkinter.Tk()
	dlg = GuiManager(master=root)
	dlg.mainloop()
