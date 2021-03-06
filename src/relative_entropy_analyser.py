# -*def _coding: utf-8 -*-

"""

作成者：AL18036 片岡凪
日付：2020.11.29 24：00
バージョン：1.5
変更内容：destフォルダやlogファイルがなければ生成
変更予定：logが膨大になると重くなるので、あるsizeを超えたら古いlogから削除
変更予定：同様な理由で、相対エントロピーがあまり変わらないときはそもそもlogを追加しない（POPする）

"""

import numpy as np
import random
import sys
import os

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
  _rtn_dest_folder_relative_path(): string
    destフォルダのパスを返す
  _rtn_log_file_relative_path(): string
    logファイルのパスを返す
  _new_dest_folder_if_needed(): void
    destフォルダが存在しなければ生成
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
  _append_abs_entropy_noise: void
    精度のため、logの記録時に付近のabs-entropyをノイズとして記録
  """

  def __init__(self):
    """
    コンストラクタ（今のところ不要）
    """
    self._absolute_entropy_logs = None
    # = [0.0, 0.1, 0.9, 1.0, 1.1, 1.9, 2.0, 2.1, 2.9, 3.0]  # イメージするための仮のfloat[], 旧 previous_entropies
    self._relative_entropy = 1.5  # 結合用の仮のfloat
    self._DEST_RELATIVE_PATH = "../dest"
    self._LOG_FILE_NAME = "previous_entropies.log"
    self._new_dest_folder_if_needed()
    self._new_entropy_logs_if_needed()
    self._load_entropy_logs()


  def _rtn_dest_folder_relative_path(self):
    """
    destフォルダのパスを返す
    @see https://qiita.com/FGtatsuro/items/52ad08640df6bfad5c2a

    Returns
    -------
    string
      destフォルダのパス
    """
    this_src_abs_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(this_src_abs_path, self._DEST_RELATIVE_PATH))


  def _rtn_log_file_relative_path(self):
    """
    logファイルのパスを返す
    @see https://qiita.com/FGtatsuro/items/52ad08640df6bfad5c2a

    Returns
    -------
    string
      logファイルのパス
    """
    dest_path = self._rtn_dest_folder_relative_path()
    return os.path.normpath(os.path.join(dest_path, self._LOG_FILE_NAME))


  def _new_dest_folder_if_needed(self):
    """
    destフォルダが存在しなければ生成
    @see https://qiita.com/FGtatsuro/items/52ad08640df6bfad5c2a
    @see https://khid.net/2019/12/python-check-exists-dir-make-dir/
    """
    dest_path = self._rtn_dest_folder_relative_path()
    if not os.path.exists(dest_path):
      print("Made dest folder")
      os.makedirs(dest_path)


  def _new_entropy_logs_if_needed(self):
    """
    ログファイルが存在しなければ生成
    @see https://note.nkmk.me/python-file-io-open-with/
    """
    log_path = self._rtn_log_file_relative_path()
    try:
      # mode x: 存在'する'場合にエラー
      with open(log_path, mode='x') as log_file:
        log_file.write('')
    except FileExistsError:
      pass


  def _load_entropy_logs(self):
    """
    相対エントロピーをログファイルからロード
    """
    log_path = self._rtn_log_file_relative_path()
    with open(log_path, mode='r') as log_file:
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
    self._append_abs_entropy_noise()
    self._update_entropy_logs()

    # リストをnarrayに変更
    abs_entropy_logs = np.array(self._absolute_entropy_logs)

    # _relative_entropy を計算 (\in [0.0, 3.0])
    max_abs_entropy = abs_entropy_logs.max()
    min_abs_entropy = abs_entropy_logs.min()

    range = max_abs_entropy - min_abs_entropy
    relative_pos = absolute_entropy - min_abs_entropy
    
    if (range != 0): # 0除算の例外処理
      self._relative_entropy = float(relative_pos) / range
      self._relative_entropy *= 3.0  # [0,3]に正規化
    else:
      # データが1つ or 同じデータしかない場合
      self._relative_entropy = 3.0 / 2 # 正規化の中央の値

    # self.close_log_file() # 不要（closeは各メソッドで行うようにしている）

    # 副作用：[0, 1.0): キレイ, [1.0, 2.0): 普通, [2.0, 3.0]: 汚い
    return self._relative_entropy


  def _update_entropy_logs(self):
    """
    絶対エントロピーをログファイルに上書き
    速度が落ちるようであれば追記にするとよい
    """
    log_path = self._rtn_log_file_relative_path()
    with open(log_path, mode='w') as log_file:
      str_entropy_list = [str(float_entropy) + '\n' for float_entropy in self._absolute_entropy_logs] # To string list
      log_file.writelines(str_entropy_list)


  def _append_abs_entropy_noise(self):
    """
    精度のため、logの記録時に付近のabs-entropyをノイズとして記録
    """
    # 要調節
    NOISE_NUM = 10
    DELTA_RATE = 0.01

    noise_delta = None
    latest_abs = None
    logs_len = len(self._absolute_entropy_logs)

    if logs_len in {None, 0}:
      print('Error: Failed to append abs-entropy')
      sys.exit()
    else:
      latest_abs = self._absolute_entropy_logs[logs_len - 1]

    if logs_len == 1:
      noise_delta = latest_abs * DELTA_RATE
    else:
      prev_abs = self._absolute_entropy_logs[logs_len - 2]
      noise_delta = (latest_abs - prev_abs) * DELTA_RATE

    for i in range(NOISE_NUM):
      self._absolute_entropy_logs.append(latest_abs + (noise_delta * (i - (NOISE_NUM / 2.0))))


  # def close_log_file(self):
  #   """
  #   ログファイルのクローズ
  #   """
  #   # void
  #   pass

# # (済)デバッグ１：ファイル関係
# # logを消して3回実行できればよい
# debug_img = [[1, 0], [0, 1]]
# debug_abs_entropy = 1.5
# relative_entropy_analyser = RelativeEntropyAnalyser()
# relative_entropy_analyser.calc_relative_entropy(debug_img, debug_abs_entropy)
# print("Done!")


# # (済)デバッグ２：_calc_entropy_analyser()
# # logを消して3回実行し、0.0-3.0の数値が標準出力されればよい
#   def _debug_print(self, debug_abs_entropy):
#     print("Updated a-entropies: ", self._absolute_entropy_logs)
#     print("Added a-entropy: ", str(debug_abs_entropy))
#     print("Calced r-entropy: ", str(self._relative_entropy))


# debug_img = [[1, 0], [0, 1]] # 動作に関係ない
# # debug_abs_entropy = random.uniform(0, 100)  # [0.0, 100.0]
# debug_abs_entropy = random.randint(0, 100) # [0, 100]

# # new
# relative_entropy_analyser = RelativeEntropyAnalyser()
# # calc
# relative_entropy_analyser.calc_relative_entropy(debug_img, debug_abs_entropy)
# # print
# relative_entropy_analyser._debug_print(debug_abs_entropy)
