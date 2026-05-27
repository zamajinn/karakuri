import pytest

from karakuri import add_bore, add_keyway, make_spur_gear

# --- 正常系 ---


def test_bore_reduces_volume():
    """
    ボア加工によってギアの体積が減少することを検証するテスト。

    ボア（中心穴）の加工前後でギアの体積を比較し、
    ボア加工後のギアの体積が元のギアより小さくなることを確認する。

    テスト手順:
    1. 20歯、モジュール2.0、厚さ8.0のスパーギアを作成
    2. 直径10のボア加工を施す
    3. ボア加工後の体積が元のギアより小さいことを確認
    """
    gear = make_spur_gear(teeth=20, module=2.0, thickness=8.0)
    bored = add_bore(gear, diameter=10)
    assert bored.volume < gear.volume


def test_keyway_reduces_volume():
    """
    キーウェイ加工によってギアの体積が減少することを検証するテスト。
    キーウェイ（鍵溝）の加工前後でギアの体積を比較し、
    キーウェイ加工後のギアの体積がボア加工後のギアより小さくなることを確認する。
    テスト手順:
    1. 20歯、モジュール2.0、厚さ8.0のスパーギアを作成
    2. 直径10のボア加工を施す
    3. ボア加工されたギアに対して、幅3、深さ1.8のキーウェイ加工を施す
    4. キーウェイ加工後の体積がボア加工後の体積より小さいことを確認
    """

    bored = add_bore(make_spur_gear(teeth=20, module=2.0, thickness=8.0), diameter=10)
    keyed = add_keyway(bored, bore_diameter=10, width=3, depth=1.8)
    assert keyed.volume < bored.volume


# --- 異常系 ---
def test_invalid_bore_raises():
    gear = make_spur_gear(teeth=20, module=2.0, thickness=8.0)
    with pytest.raises(ValueError):
        add_bore(gear, diameter=0)


def test_invalid_keyway_raises():
    bored = add_bore(make_spur_gear(teeth=20, module=2.0, thickness=8.0), diameter=10)
    with pytest.raises(ValueError):
        add_keyway(bored, bore_diameter=10, width=0, depth=0)
