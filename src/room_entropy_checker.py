#kanamori
#2020.11.22
#ver1.0
#書きはじめ

import tkinter
from gui_manager import GuiManager

class RoomEntropyChecker:
    _SLEEP_SEC = 3
    _IMG_WIDTH = 600
    _IMG_HEIGHT = 300
    def loop_gui(self):
    	root = tkinter.Tk()
    	gui_manager = GuiManager(master=root, 
    		width=self._IMG_WIDTH, 
    		height=self._IMG_HEIGHT, 
    		sleep_sec=self._SLEEP_SEC)
    	gui_manager.mainloop()

room_entropy_checker = RoomEntropyChecker()
room_entropy_checker.loop_gui()
