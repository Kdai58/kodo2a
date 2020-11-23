# -*- coding: utf-8 -*-

"""

作成者：
日付：2020.11.23
バージョン：2.0
変更内容：GuiManagerのmainloopを呼ぶ処理を追加．
変更内容：GuiManagerのインスタンスを生成している部分の，画像サイズの指定部分を削除した．
         コンストラクタの中で_SLEEP_SECを初期化するようにした．

"""

import tkinter
from gui_manager import GuiManager

class RoomEntropyChecker:
	def __init__(self):
	    self._SLEEP_SEC = 3

	def loop_gui(self):
		root = tkinter.Tk()
		gui_manager = GuiManager(master=root, sleep_sec=self._SLEEP_SEC)
		gui_manager.mainloop()

room_entropy_checker = RoomEntropyChecker()
room_entropy_checker.loop_gui()
