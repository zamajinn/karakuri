# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 概要

karakuri は [build123d](https://github.com/gumyr/build123d) をベースに、インボリュート
歯車の3Dモデルを生成する Python ライブラリ。2つの関心事に分かれている:

- **歯車生成** (`spur_gear.py`) — 歯車パラメータから歯車ソリッドを生成する。
- **機械加工フィーチャ** (`features.py`) — `Part -> Part` の変換（軸穴・キー溝）。
  歯車に限らず円盤状の部品に適用できる。

公開関数はすべて `build123d.Part` を返す/受け取る。STL 出力や可視化はラップしておらず、
呼び出し側が build123d を直接使う（例: `export_stl`）。

## コマンド

```bash
# 開発ツール込みの editable インストール（pytest, ruff）
pip install -e .[dev]

# テスト
pytest                                              # 全件
pytest tests/test_spur_gear.py::test_return_part    # 単体

# Lint / format（ruff）
ruff check .            # lint
ruff check --fix .      # lint + 自動修正（import 順 I001 など）
ruff format .           # 整形
ruff format --check .   # 整形チェックのみ（CI で使用）

# 平歯車 CLI の実行（console エントリポイントは未定義）
python src/karakuri/spur_gear.py --teeth 20 --module 2 --thickness 8
```

CI (`.github/workflows/ci.yml`) は `main` への push と全 PR で `ruff check`・
`ruff format --check`・`pytest` を実行する。

## アーキテクチャ

- **src レイアウト**: パッケージは `src/karakuri/` にある。テストと examples は
  インストール済みパッケージを import する（`from karakuri import ...`）ため、
  解決には editable インストールが必要。
- **公開 API** は `src/karakuri/__init__.py` の `__all__` で管理
  (`make_spur_gear`, `add_bore`, `add_keyway`)。ここで re-export することで、内部の
  モジュール構成を変えても `from karakuri import ...` を壊さずに済む。
- **`examples/`** は学習用スクリプト（直接実行し、`from karakuri import ...` を使う）。
  wheel に同梱しないよう `src/karakuri/` には置かない。

### 平歯車の構築 (`make_spur_gear`)

2D で組んでから押し出す:

1. 1個の歯を閉じたスケッチとして描く: +y 側フランクを上るインボリュートスプライン、
   歯先円半径での先端円弧、鏡像のフランクを下る経路、歯底円に沿う短い円弧。
2. その歯を `PolarLocations` で `z` 個複製し、ベースの `Circle(rf)`（歯底円ディスク）に
   合成する。
3. 合成したスケッチを `thickness` ぶん押し出す。

`tooth_height_factor`（デフォルト 2.25）は標準の 1.0 : 1.25 比で歯末たけ(1.0)と
歯元たけ(1.25)に分割される。歯底円が基礎円の内側にある場合（`rf < rb`、歯数が少ない時など）、
各フランクを歯底まで放射状の線で延長する。

## build123d のハマりどころ（実際に詰まった点）

- **`Vector` の成分は大文字のみ**: `bbox.max.Z` であって `.z` ではない（小文字は
  `AttributeError`）。`.X` / `.Y` も同様。
- **スケッチの巡回向きが重要**: `make_face` はワイヤの向きで内側を塗りつぶす。歯のワイヤは
  上フランク → 先端 → 下フランク → 歯底 の順に描いて面が正の向きになる。逆順だと歯が穴になり
  歯車が反転する。
- **インボリュートの符号は対**: `_involute_xy` は CW スパイラルのパラメータ化
  (`y = rb*(t*cos t - sin t)`) で、`flank_rot = pi/(2z) + inv(alpha)` と対になっている。
  y の符号と `flank_rot` の符号は同時に変えないと、歯の先細りが逆転する（先端が太くなる）。

## 規約

- **コミット**: Conventional Commits（`feat`, `fix`, `docs`, `ci`, `chore`, `refactor`,
  `test`）。例: `feat(features): add bore and keyway machining functions`。
- **ruff**: line length 100、target py310、ルール `E` / `F` / `I`。
- **バリデーション**: 公開関数は不正入力に対して `ValueError` を送出する
  （例: `teeth < 4`、非正の `module`/`diameter`）。
