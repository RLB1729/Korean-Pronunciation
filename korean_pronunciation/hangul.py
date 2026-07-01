"""Hangul decomposition and composition utility functions.

Supports decomposing syllables into Choseong, Jungseong, and Jongseong,
and composing them back into syllable characters.
"""

from typing import Tuple
from korean_pronunciation.jamo_constants import (
    CHOSEONG, JUNGSEONG, JONGSEONG,
    CHOSEONG_MAP, JUNGSEONG_MAP, JONGSEONG_MAP
)

S_BASE = 0xAC00
L_BASE = 0x1100
V_BASE = 0x1161
T_BASE = 0x11A7
L_COUNT = 19
V_COUNT = 21
T_COUNT = 28
N_COUNT = V_COUNT * T_COUNT  # 588
S_COUNT = L_COUNT * N_COUNT  # 11172


def is_hangul_syllable(char: str) -> bool:
    """Check if a character is a precomposed Hangul syllable (U+AC00 - U+D7AF)."""
    if len(char) != 1:
        return False
    code = ord(char)
    return S_BASE <= code < S_BASE + S_COUNT


def decompose(char: str) -> Tuple[str, str, str]:
    """Decompose a precomposed Hangul syllable into its Choseong, Jungseong, and Jongseong components.

    If the character is not a Hangul syllable, returns it as (char, "", "").
    """
    if not is_hangul_syllable(char):
        return char, "", ""

    code = ord(char)
    s_index = code - S_BASE
    
    l_index = s_index // N_COUNT
    v_index = (s_index % N_COUNT) // T_COUNT
    t_index = s_index % T_COUNT
    
    return CHOSEONG[l_index], JUNGSEONG[v_index], JONGSEONG[t_index]


def compose(choseong: str, jungseong: str, jongseong: str = "") -> str:
    """Compose Choseong, Jungseong, and Jongseong back into a precomposed Hangul syllable.

    If composition is not possible or inputs are invalid, returns empty string.
    """
    if choseong not in CHOSEONG_MAP or jungseong not in JUNGSEONG_MAP:
        return ""
        
    l_index = CHOSEONG_MAP[choseong]
    v_index = JUNGSEONG_MAP[jungseong]
    t_index = JONGSEONG_MAP.get(jongseong, 0)
    
    code = S_BASE + (l_index * N_COUNT) + (v_index * T_COUNT) + t_index
    return chr(code)


def has_jongseong(char: str) -> bool:
    """Return True if the given syllable has a final consonant (jongseong)."""
    if not is_hangul_syllable(char):
        return False
    _, _, jong = decompose(char)
    return jong != ""
