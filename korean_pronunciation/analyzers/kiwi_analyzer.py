"""Kiwi morphological analyzer wrapper.

Provides accurate part-of-speech tagging and morpheme boundary detection
using the kiwipiepy library.
"""

from typing import List
from korean_pronunciation.analyzers.base import BaseMorphAnalyzer, MorphToken

try:
    from kiwipiepy import Kiwi
    _KIWI_AVAILABLE = True
except ImportError:
    _KIWI_AVAILABLE = False


class KiwiAnalyzer(BaseMorphAnalyzer):
    """Morphological analyzer utilizing Kiwi (kiwipiepy)."""

    def __init__(self):
        if not _KIWI_AVAILABLE:
            raise ImportError(
                "kiwipiepy is not installed. Please install it using "
                "`pip install kiwipiepy` or use SimpleAnalyzer instead."
            )
        self.kiwi = Kiwi()

    def analyze(self, text: str) -> List[MorphToken]:
        tokens: List[MorphToken] = []
        
        # Analyze using Kiwi
        kiwi_tokens = self.kiwi.tokenize(text)
        
        for token in kiwi_tokens:
            # Determine if grammatical morpheme (형식 형태소: 조사, 어미, 접미사)
            # - J: 조사 (JKS, JKC, JKG, JKO, JKB, JKV, JKQ, JX, JC)
            # - E: 어미 (EP, EF, EC, ETN, ETM)
            # - XS: 접미사 (XSN, XSV, XSA)
            is_grammatical = (
                token.tag.startswith("J") or 
                token.tag.startswith("E") or 
                token.tag.startswith("XS") or
                token.tag.startswith("VC")
            )
            
            tokens.append(MorphToken(
                surface=token.form,
                tag=token.tag,
                start=token.start,
                end=token.start + token.len,
                is_grammatical=is_grammatical
            ))
            
        return tokens
