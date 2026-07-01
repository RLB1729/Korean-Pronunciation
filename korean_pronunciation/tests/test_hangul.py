"""Unit tests for Hangul decomposition and composition."""

from korean_pronunciation.hangul import decompose, compose, is_hangul_syllable, has_jongseong


def test_is_hangul_syllable():
    assert is_hangul_syllable("한") is True
    assert is_hangul_syllable("글") is True
    assert is_hangul_syllable("a") is False
    assert is_hangul_syllable("1") is False
    assert is_hangul_syllable(" ") is False
    assert is_hangul_syllable("ㄱ") is False  # Standalone Jamo is not a syllable


def test_decompose():
    assert decompose("한") == ("ㅎ", "ㅏ", "ㄴ")
    assert decompose("글") == ("ㄱ", "ㅡ", "ㄹ")
    assert decompose("아") == ("ㅇ", "ㅏ", "")
    assert decompose("값") == ("ㄱ", "ㅏ", "ㅄ")
    assert decompose("a") == ("a", "", "")


def test_compose():
    assert compose("ㅎ", "ㅏ", "ㄴ") == "한"
    assert compose("ㄱ", "ㅡ", "ㄹ") == "글"
    assert compose("ㅇ", "ㅏ", "") == "아"
    assert compose("ㄱ", "ㅏ", "ㅄ") == "값"


def test_has_jongseong():
    assert has_jongseong("한") is True
    assert has_jongseong("아") is False
    assert has_jongseong("a") is False
