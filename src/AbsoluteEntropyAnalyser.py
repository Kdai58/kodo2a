"""

作成者 寺尾佳祐
作成日 11/23
ver3.0
初期内容(ver1.0) : とりあえず動くようにランダム関数を使用
変更内容 :  輝度画像化した画像の平均画素値を計算するプログラムを追加

"""
#与えられた画像からエッジを検出．乱雑度を仮に数値化
import numpy as np
import sys
import cv2
import random

"""
#結合テスト用
class calc_absolute_entropy:
    def __init__(self):
        x = random.uniform(0, 2)
        return x
"""

class calc_absolute_entropy:
    def __init__(self, img):
        self.img = img; #img変数に引数を格納

        #画像読み込み，白黒画像に変換 (輝度)
        img = cv2.imread(img)
        img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        #エッジを検出，画像として出力
        edges = cv2.Canny(img, 90, 180, L2gradient = True)
        cv2.imwrite(fname_out, edges)


        #エッジの量を計算(平均画素値が高いほどエッジの量が多いとする)
        mean_value = 0
        height = edges.shape[0]
        width  = edges.shape[1]
        for y in range(height):
            for x in range(width):
                mean_value += edges[y,x]

        mean_value = mean_value / (height * width)
        
        #平均画素値を出力
        print('平均画素値は{}です'.format(mean_value))

"""ここで正規化はいらないらしいので消すかも

        #画素値から3値に正規化．値が小さいほど綺麗な部屋
        if   mean_value > 20:
            return 2
        elif 10 < mean_value <= 20:
            return 1
        elif mean_value <= 10:
            return 0
"""     




"""
#後で消す
fname_in  = sys.argv[1] #読み込み画像名入力
fname_out = sys.argv[2] #出力画像名入力

test = calc_absolute_entropy(fname_in)#実行
"""
