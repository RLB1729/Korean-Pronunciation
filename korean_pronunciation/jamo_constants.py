"""Constants for Korean Hangul processing.

This module defines the lists of Choseong (initial consonants),
Jungseong (vowels), and Jongseong (final consonants) in their compatibility
Jamo forms to facilitate readable and clear rule representations.
It also includes phonological classifications.
"""

# Choseong (초성): 19 characters
CHOSEONG = (
    "ㄱ", "ㄲ", "ㄴ", "ㄷ", "ㄸ", "ㄹ", "ㅁ", "ㅂ", "ㅃ",
    "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅉ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"
)

# Jungseong (중성): 21 characters
JUNGSEONG = (
    "ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅗ", "ㅘ",
    "ㅙ", "ㅚ", "요", "ㅜ", "ㅝ", "ㅞ", "ㅟ", "ㅠ", "ㅡ", "ㅢ", "ㅣ"
)

# Jongseong (종성): 28 slots (index 0 is empty/none)
JONGSEONG = (
    "", "ㄱ", "ㄲ", "ㄳ", "ㄴ", "ㄵ", "ㄶ", "ㄷ", "ㄹ", "ㄺ",
    "ㄻ", "ㄼ", "ㄽ", "ㄾ", "ㄿ", "ㅀ", "ㅁ", "ㅂ", "ㅄ", "ㅅ",
    "ㅆ", "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"
)

# Reverse index mappings for fast lookup
CHOSEONG_MAP = {char: idx for idx, char in enumerate(CHOSEONG)}
JUNGSEONG_MAP = {char: idx for idx, char in enumerate(JUNGSEONG)}
JONGSEONG_MAP = {char: idx for idx, char in enumerate(JONGSEONG)}

# Double coda decomposition (for double batchim simplification)
DOUBLE_CODA_MAP = {
    "ㄳ": ("ㄱ", "ㅅ"),
    "ㄵ": ("ㄴ", "ㅈ"),
    "ㄶ": ("ㄴ", "ㅎ"),
    "ㄺ": ("ㄹ", "ㄱ"),
    "ㄻ": ("ㄹ", "ㅁ"),
    "ㄼ": ("ㄹ", "ㅂ"),
    "ㄽ": ("ㄹ", "ㅅ"),
    "ㄾ": ("ㄹ", "ㅌ"),
    "ㄿ": ("ㄹ", "ㅍ"),
    "ㅀ": ("ㄹ", "ㅎ"),
    "ㅄ": ("ㅂ", "ㅅ"),
}

# Coda neutralization map (representing primary representative sounds per 제8-9항)
CODA_NEUTRALIZATION_MAP = {
    # 홑받침/쌍받침 neutralization
    "ㄱ": "ㄱ", "ㄲ": "ㄱ", "ㅋ": "ㄱ",
    "ㄴ": "ㄴ",
    "ㄷ": "ㄷ", "ㅅ": "ㄷ", "ㅆ": "ㄷ", "ㅈ": "ㄷ", "ㅊ": "ㄷ", "ㅌ": "ㄷ", "ㅎ": "ㄷ",
    "ㄹ": "ㄹ",
    "ㅁ": "ㅁ",
    "ㅂ": "ㅂ", "ㅍ": "ㅂ",
    "ㅇ": "ㅇ",
    # 겹받침 primary representations (when simplified as single coda)
    "ㄳ": "ㄱ", "ㄵ": "ㄴ", "ㄶ": "ㄴ",
    "ㄺ": "ㄱ", "ㄻ": "ㅁ", "ㄼ": "ㄹ", "ㄽ": "ㄹ", "ㄾ": "ㄹ", "ㄿ": "ㅂ", "ㅀ": "ㄹ",
    "ㅄ": "ㅂ",
}

# Phonological groups of consonants (represented in compatibility Jamo)
PLOSIVES = {"ㄱ", "ㄲ", "ㅋ", "ㄷ", "ㄸ", "ㅌ", "ㅂ", "ㅃ", "ㅍ"}
NASALS = {"ㄴ", "ㅁ", "ㅇ"}
LIQUIDS = {"ㄹ"}
ASPIRATED = {"ㅋ", "ㅌ", "ㅍ", "ㅊ"}
FORTIS = {"ㄲ", "ㄸ", "ㅃ", "ㅆ", "ㅉ"}
LENIS = {"ㄱ", "ㄷ", "ㅂ", "ㅅ", "ㅈ"} # Plain/weak consonants that can undergo fortition

# Mapping from plain/lenis consonants to their fortis (tense) counterparts
FORTITION_MAP = {
    "ㄱ": "ㄲ",
    "ㄷ": "ㄸ",
    "ㅂ": "ㅃ",
    "ㅅ": "ㅆ",
    "ㅈ": "ㅉ"
}

# Mapping for aspiration (거센소리되기)
ASPIRATION_MAP = {
    ("ㄱ", "ㅎ"): "ㅋ",
    ("ㅎ", "ㄱ"): "ㅋ",
    ("ㄷ", "ㅎ"): "ㅌ",
    ("ㅎ", "ㄷ"): "ㅌ",
    ("ㅂ", "ㅎ"): "ㅍ",
    ("ㅎ", "ㅂ"): "ㅍ",
    ("ㅈ", "ㅎ"): "ㅊ",
    ("ㅎ", "ㅈ"): "ㅊ",
}
