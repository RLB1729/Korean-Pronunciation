"""Tokenizer for mapping text characters to decorated Syllables."""

from typing import List, Tuple
from korean_pronunciation import hangul
from korean_pronunciation.state import Syllable, PronunciationState
from korean_pronunciation.analyzers.base import BaseMorphAnalyzer


def tokenize(text: str, analyzer: BaseMorphAnalyzer) -> PronunciationState:
    """Tokenize the input text using a morphological analyzer.

    Maps each character to a Syllable object with associated morphological info.
    Returns a PronunciationState ready for rule application.
    """
    tokens = analyzer.analyze(text)
    syllables: List[Syllable] = []
    
    for idx, char in enumerate(text):
        # 1. Hangul decomposition
        is_hangul = hangul.is_hangul_syllable(char)
        if is_hangul:
            cho, jung, jong = hangul.decompose(char)
        else:
            cho, jung, jong = char, "", ""
            
        # 2. Find morphological metadata by character index
        morpheme_tag = "UNKNOWN"
        is_grammatical = False
        has_boundary_before = False
        
        for token in tokens:
            if token.start <= idx < token.end:
                morpheme_tag = token.tag
                is_grammatical = token.is_grammatical
                has_boundary_before = (idx == token.start)
                break
        
        # If no token matched, treat spaces/punctuation as boundary-bearing and grammatical
        if morpheme_tag == "UNKNOWN":
            has_boundary_before = not char.isalnum()
            is_grammatical = True
            morpheme_tag = "SP" if char == " " else "SF"
            
        syllables.append(Syllable(
            choseong=cho,
            jungseong=jung,
            jongseong=jong,
            is_hangul=is_hangul,
            original=char,
            morpheme_tag=morpheme_tag,
            is_grammatical=is_grammatical,
            has_boundary_before=has_boundary_before
        ))
        
    return PronunciationState(syllables=tuple(syllables))
