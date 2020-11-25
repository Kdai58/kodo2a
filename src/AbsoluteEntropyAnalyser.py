"""

作成者 寺尾佳祐
作成日 11/25
ver4.0
変更内容 :  関数名を変更．
           関数の機能を「エッジ検出した画像を出力」から「絶対エントロピーを返す」に変更．

"""
#与えられた画像からエッジを検出．乱雑度を仮に数値化
import numpy as np
import sys
import cv2
import random

class AbsoluteEntropyAnalyser:
    def calc_absolute_entropy(self, img):
        self.img = img; #img変数に引数を格納

        #画像読み込み，白黒画像に変換 (輝度)
        img = cv2.imread(img)
        img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        #エッジを検出
        edges = cv2.Canny(img, 90, 180, L2gradient = True)
        """#画像として出力 (いらないかも)
        cv2.imwrite(fname_out, edges)
        """

        #エッジの量を計算(平均画素値が高いほどエッジの量が多いとする)
        mean_value = 0
        height = edges.shape[0]
        width  = edges.shape[1]
        for y in range(height):
            for x in range(width):
                mean_value += edges[y,x]

        mean_value = mean_value / (height * width)

        #画素値から3値に正規化．値が小さいほど綺麗な部屋
        absolute_entropy = 0

        if   mean_value > 20:
            absolute_entropy = 2
        elif 10 < mean_value <= 20:
            absolute_entropy = 1
        elif mean_value <= 10:
            absolute_entropy = 0

        return absolute_entropy
     



"""
#テスト用
fname_in  = sys.argv[1] #読み込み画像名入力
#fname_out = sys.argv[2] #出力画像名入力

test = AbsoluteEntropyAnalyser()#実行
result = test.calc_absolute_entropy(fname_in)
print(result)

"""