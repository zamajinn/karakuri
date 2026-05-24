# karakuri

![CI](https://github.com/eng-kei-going/karakuri/actions/workflows/ci.yml/badge.svg)

Python library for generating involute gear 3D models with build123d.

build123d をベースに、インボリュート歯車の3Dモデルを生成する Python ライブラリです。

## 概要

歯数とモジュールを指定するだけで、平歯車の STL ファイルを出力できます。
圧力角・歯たけ係数・厚さも指定可能で、機械工学的に正しいインボリュート歯形を生成します。

## Installation

GitHub から直接インストール:

```bash
pip install git+https://github.com/eng-kei-going/karakuri.git
```

または clone してから editable install:

```bash
git clone https://github.com/eng-kei-going/karakuri.git
cd karakuri
pip install -e .
```

## Usage

```python
from karakuri import make_spur_gear
from build123d import export_stl

# 歯数 20、モジュール 2.0、厚さ 8 mm の平歯車を生成
gear = make_spur_gear(teeth=20, module=2.0, thickness=8)

# STL ファイルとして保存
export_stl(gear, "spur_gear.stl")
```

karakuri は `build123d.Part` オブジェクトを返します。STL 出力やさらなるモデル操作には build123d の関数をそのまま利用できます。

## API

| Function | Description |
|---|---|
| `make_spur_gear(teeth, module, ...)` | 平歯車（spur gear）を生成 |

詳細は各関数の docstring を参照してください。

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
