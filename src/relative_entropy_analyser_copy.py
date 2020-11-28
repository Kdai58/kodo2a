# -*def _coding: utf-8 -*-

"""

作成者：AL18036 片岡凪
日付：2020.11.23
バージョン：1.1
変更内容：属性の初期化をコンストラクタ内で行うように変更
変更内容：リストを{}と勘違いしていたのを[]に変更
変更予定：メソッドの実装

"""

import numpy as np

class RelativeEntropyAnalyser:
  """
  相対エントロピーの解析器
  
  Attributes
  ----------
  _absolute_entropy_logs: float[]
    以前までの絶対エントロピーのログを保存
  _relative_entropy: float
    求める相対エントロピーを保存

  Methods
  -------
  _new_entropy_logs_if_needed(): void
    ログファイルが存在しなければ生成
  _load_entropy_logs(): void
    相対エントロピーをログファイルからロード
  calc_relative_entropy(img: int[][], absolute_entropy: float): float
    今の絶対エントロピーを受け取り，相対エントロピーを計算
  _update_entropy_logs(): void
    受け取った絶対エントロピーをログファイルに記録
  close_log_file(): void
    ログファイルのクローズ
  """

  def __init__(self):
    """
    コンストラクタ（今のところ不要）
    """
    self._absolute_entropy_logs = None
    # = [0.0, 0.1, 0.9, 1.0, 1.1, 1.9, 2.0, 2.1, 2.9, 3.0]  # イメージするための仮のfloat[], 旧 previous_entropies
    self._relative_entropy = 1.5  # 結合用の仮のfloat
    self._LOG_FILE_PATH = '../dest/previous_entropies.log'  #.logファイルに変更 名前がわかりやすいだけ
    self._new_entropy_logs_if_needed()
    self._load_entropy_logs()



  def _new_entropy_logs_if_needed(self):
    """
    ログファイルが存在しなければ生成
    @see https://note.nkmk.me/python-file-io-open-with/
    """
    try:
      # mode x: 存在'する'場合にエラー
      with open(self._LOG_FILE_PATH, mode='x') as log_file:
        log_file.write('')
    except FileExistsError:
      pass


  def _load_entropy_logs(self):
    """
    相対エントロピーをログファイルからロード
    """
    with open(self._LOG_FILE_PATH, mode='r') as log_file:
      str_entropy_list = log_file.readlines()
      self._absolute_entropy_logs = [float(s) for s in str_entropy_list] # To float list

  def calc_relative_entropy(self, img, absolute_entropy):
    """
    今の絶対エントロピーを受け取り，相対エントロピーを計算

    Parameters
    ----------
    img: int[][]
      今のカメラの画像。不要説が濃厚だけど、取り合えず受け取っときます
    absolute_entropy: float
      今の絶対エントロピー

    Returns
    -------
    float
      計算した相対エントロピー
    """
    # logのリストに引数のabsを追加
    self._absolute_entropy_logs.append(absolute_entropy)

    # リストをnarrayに変更
    abs_entropy_logs = np.array(self._absolute_entropy_logs)

    # calc _relative_entropy (\in [0.0, 3.0])
    max_abs_entropy = abs_entropy_logs.max()
    min_abs_entropy = abs_entropy_logs.min()

    range = max_abs_entropy - min_abs_entropy
    relative_pos = absolute_entropy - min_abs_entropy
    
    self._relative_entropy = relative_pos / range
    self._relative_entropy *= 3.0 # [0,3]に正規化

    self._absolute_entropy_logs.append(self._relative_entropy)
    self._update_entropy_logs()
    # self.close_log_file() # 不要（closeは各メソッドで行うようにしている）

    # 副作用：[0, 1.0): キレイ, [1.0, 2.0): 普通, [2.0, 3.0]: 汚い
    return self._relative_entropy


  def _update_entropy_logs(self):
    """
    絶対エントロピーをログファイルに上書き
    速度が落ちるようであれば追記にするとよい
    """
    with open(self._LOG_FILE_PATH, mode='w') as log_file:
      str_entropy_list = [str(float_entropy) + '\n' for float_entropy in self._absolute_entropy_logs] # To string list
      log_file.writelines(str_entropy_list)


  # def close_log_file(self):
  #   """
  #   ログファイルのクローズ
  #   """
  #   # void
  #   pass
