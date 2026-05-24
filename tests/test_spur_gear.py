import pytest

from karakuri import make_spur_gear


def test_return_part():
    """
    スパーギアの生成機能をテストする。

    このテストは、make_spur_gear関数が正常に機能しているか確認する。
    具体的には以下の3点を検証している：
    1. 関数が実際にギアオブジェクトを返すこと（Noneでないこと）
    2. 生成されたギアの体積が正の値であること（有効な3D形状であることの確認）

    テストパラメータ：
        - teeth: 20 (歯数)
        - module: 2.0 (モジュール - 歯のサイズを決定)
        - thickness: 10.0 (ギアの厚さ)

    Returns:
        None: このテストのアサーション結果がテストフレームワークに返される
    """
    gear = make_spur_gear(teeth=20, module=2.0, thickness=10.0)
    assert gear is not None
    assert gear.volume > 0


def test_volume_in_expected_range():
    """
    スパーギアの体積が想定範囲内であることをテストする。

    このテストは、歯数20、モジュール2.0、厚さ8.0のスパーギアの体積が
    ベース円とギアの外形円の間の範囲内にあることを確認する。

    体積はmm³で測定され、9000 < volume < 110000 の範囲内であることを検証。

    Raises:
        AssertionError: 体積が期待範囲（9000 < volume < 110000）内にない場合
    """
    gear = make_spur_gear(teeth=20, module=2.0, thickness=8.0)
    assert 9000 < gear.volume < 110000


def test_too_few_teeth_raises():
    """
    Test that creating a spur gear with too few teeth raises a ValueError.
    このテストは、歯数が少なすぎるスパーギアを作成しようとした場合に、
    ValueErrorが発生することを確認します。
    Tests that make_spur_gear() raises ValueError when teeth parameter is
    set to an insufficient value (2 teeth in this case).
    """

    with pytest.raises(ValueError):
        make_spur_gear(teeth=2, module=2)


def test_zero_module_raises():
    """
    スパーギアのモジュールが0の場合にValueErrorが発生することをテストする。
    このテストは、スパーギアを生成する際にモジュール値が0に設定されている場合、
    適切にValueErrorが発生することを確認する。
    モジュールは歯車の基本的な設計パラメータであり、0は無効な値である。
    テスト対象:
        make_spur_gear関数のバリデーション
    期待される動作:
        make_spur_gear(teeth=20, module=0)を呼び出すと、
        ValueErrorが発生する。
    Raises:
        ValueError: モジュールが0の場合に発生
    """

    with pytest.raises(ValueError):
        make_spur_gear(teeth=20, module=0)


def test_zero_thickness_raises():
    """
    スプールギアの厚さがゼロの場合、ValueErrorが発生することをテストする。
    このテストは、make_spur_gear関数に厚さ0を指定した場合、
    適切なバリデーションエラーが発生することを確認する。
    テスト対象: make_spur_gear関数のバリデーション
    条件: teeth=20, module=2, thickness=0
    期待結果: ValueErrorが発生すること
    """

    with pytest.raises(ValueError):
        make_spur_gear(teeth=20, module=2, thickness=0)
