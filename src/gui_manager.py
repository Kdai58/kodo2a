# -*- coding: utf-8 -*-
import tkinter
import threading
import random
import time

class GuiManager(tkinter.Frame):
	def __init__(self, master=None):
		super().__init__(master)

		self.PRAISE_STR = 'How beautiful your room is'
		self.NORMAL_STR = 'Endeavor putting your room in order'
		self.WARN_STR = 'How dirty your room is'

		master.geometry('500x300')

		# フレームの初期化
		self.master = master
		self.master.title('Room entropy checker')
		self.pack()

		# ボタンの設定
		self.destroy_btn = tkinter.Button(master, text='destroy', command=self.destroy_gui)
		self.start_btn = tkinter.Button(master, text='start', command=self.monitor_callback)

		self.destroy_btn.pack(side='bottom')
		self.start_btn.pack(side='bottom')

		# テキストの設定
		self.alert_text = tkinter.StringVar()
		self.alert_text.set(self.NORMAL_STR)
		self.alert_text_label = tkinter.Label(master, textvariable=self.alert_text)

		self.alert_text_label.pack(anchor='center', expand=1)

	def monitor_callback(self):
		thread = threading.Thread(target=self.monitor, args=())
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

	def update_gui(self, room_entropy):
		if room_entropy == 0:
			self.alert_text.set(self.PRAISE_STR)
		elif room_entropy == 1:
			self.alert_text.set(self.NORMAL_STR)
		else:
			self.alert_text.set(self.WARN_STR)


	def destroy_gui(self):
		self.master.destroy()

if __name__ == "__main__":
	root = tkinter.Tk()
	dlg = GuiManager(master=root)
	dlg.mainloop()
