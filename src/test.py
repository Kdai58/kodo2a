import unittest
import tkinter
from gui_manager import GuiManager

class TestGuiManager(unittest.TestCase):
	"""test class of gui_manager.py
	"""

	def test_print_exception(self):
		"""test method for __print_exception
		"""
		root = tkinter.Tk()
		sut = GuiManager(master=root)

		# テストケースの設定
		values = [0, 1, 2]

		# 期待出力の設定
		expected_results = [0] * 3
		for i in range(3):
			expected_results[i] = tkinter.StringVar()

		expected_results[0].set(sut.PRAISE_STR)
		expected_results[1].set(sut.NORMAL_STR)
		expected_results[2].set(sut.WARN_STR)

		for i in range(3):
			expected_results[i] = expected_results[i].get()

		# 全てのテストケースでテスト
		for value, expected_result in zip(values, expected_results):
			with self.subTest(value=value):
				sut._print_exception(value)
				actual_result = sut.alert_text.get()
				self.assertEqual(actual_result, expected_result)