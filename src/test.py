# -*- coding: utf-8 -*-

"""

作成者：兼平大輔
日付：2020.11.18
バージョン：2.0
変更内容：GuiManager._to_entropy_level()のテストを書いた．

"""

import unittest
import tkinter
from gui_manager import GuiManager

class TestGuiManager(unittest.TestCase):

	"""

	test class of gui_manager.py
	
	"""

	def setUp(self):
		self.root = tkinter.Tk()
		self.gui = GuiManager(master=self.root)

	def test_to_entropy_level(self):

		"""

		test method for _to_entropy_level

		"""

		# テストケースの設定
		test_cases = [0, 1, 2]

		for test_case in test_cases:
			with self.subTest(value=test_case):
				if test_case == 0:
					actual = self.gui._to_entropy_level(test_case)
					expected = 0
				elif test_case == 1:
					actual = self.gui._to_entropy_level(test_case)
					expected = 1
				else:
					actual = self.gui._to_entropy_level(test_case)
					expected = 2

				self.assertEqual(actual, expected)

	# def test_print_exception(self):
	# 	"""test method for __print_exception
	# 	"""
	# 	root = tkinter.Tk()
	# 	sut = GuiManager(master=root)

	# 	# テストケースの設定
	# 	values = [0, 1, 2]

	# 	# 期待出力の設定
	# 	expected_results = [0] * 3
	# 	for i in range(3):
	# 		expected_results[i] = tkinter.StringVar()

	# 	expected_results[0].set(sut.PRAISE_STR)
	# 	expected_results[1].set(sut.NORMAL_STR)
	# 	expected_results[2].set(sut.WARN_STR)

	# 	for i in range(3):
	# 		expected_results[i] = expected_results[i].get()

	# 	# 全てのテストケースでテスト
	# 	for value, expected_result in zip(values, expected_results):
	# 		with self.subTest(value=value):
	# 			sut._print_exception(value)
	# 			actual_result = sut.alert_text.get()
	# 			self.assertEqual(actual_result, expected_result)