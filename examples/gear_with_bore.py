"""
スパーギア生成と加工の使用例

このモジュールは、karakuriライブラリを使用してスパーギアを生成し、
複数の加工処理を行う基本的な使用例を示します。

処理フロー:
    1. 歯数20、モジュール2.0、厚さ8.0mmのスパーギアを生成
    2. ギアの中心に直径10mmのボアホール（穴）を追加
    3. ボアホールにキーウェイ（キー溝）を追加
       - 幅: 3mm
       - 深さ: 1.8mm
    4. 最終的な3DモデルをSTL形式でエクスポート

出力ファイル:
    gear_with_bore_and_keyway.stl: ボアとキーウェイが加工されたギアの3Dモデル

使用ライブラリ:
    - karakuri: ギア生成と加工機能
    - build123d: 3Dモデルのエクスポート機能
"""

from build123d import export_stl

from karakuri import add_bore, add_keyway, make_spur_gear

gear = make_spur_gear(teeth=20, module=2.0, thickness=8.0)
bored = add_bore(gear, diameter=10)
keyed = add_keyway(bored, bore_diameter=10, width=3, depth=1.8)

export_stl(keyed, "gear_with_bore_and_keyway.stl")
