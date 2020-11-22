# -*def _coding: utf-8 -*-

"""

作成者：AL18036 片岡凪
日付：2020.11.22
バージョン：1.0
変更内容：メソッドの作成，仮の返り値
変更予定：メソッドの実装

"""

class RelativeEntropyAnalyser:
  """
  相対エントロピーの解析器
  
  Attributes
  ----------
  previous_absolute_entropies: float[]
    以前までの絶対エントロピーのログを保存
  relative_entropy: float
    求める相対エントロピーを保存

  Methods
  -------
  new_entropies_log_if_needed(): void
    ログファイルが存在しなければ生成
  load_previous_entropies(): void
    相対エントロピーをログファイルからロード
  calc_relative_entropy(img: int[][], absolute_entropy: float): float
    今の絶対エントロピーを受け取り，相対エントロピーを計算
  update_previous_entropies(): void
    受け取った絶対エントロピーをログファイルに記録
  close_log_file(): void
    ログファイルのクローズ
  """


  self._previous_absolute_entropies = \
    {0.0, 0.1, 0.9, 1.0, 1.1, 1.9, 2.0, 2.1, 2.9, 3.0}  # イメージするための仮のfloat[], 旧 previous_entropies
  self._relative_entropy = 1.5 # 結合用の仮のfloat


  def __init__(self):
    """
    コンストラクタ（今のところ不要）
    """
    pass


  def _new_entropies_log_if_needed(self):
    """
    ログファイルが存在しなければ生成
    """
    # void
    pass


  def _load_previous_entropies(self):
    """
    相対エントロピーをログファイルからロード
    """
    # void
    pass


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
    # 結合用の仮のfloatを返す
    # 副作用：[0, 1.0): キレイ, [1.0, 2.0): 普通, [2.0, 3.0]: 汚い
    return self._relative_entropy # 仮値 1.5


  def _update_previous_entropies(self):
    """
    受け取った絶対エントロピーをログファイルに記録
    """
    # void
    pass


  def close_log_file(self):
    """
    ログファイルのクローズ
    """
    # void
    pass
