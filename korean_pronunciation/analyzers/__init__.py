"""Morphological analyzer package.

Provides morphological analyzers for boundary detection and grammatical vs lexical
categorization of Korean morphemes.
"""

from korean_pronunciation.analyzers.base import BaseMorphAnalyzer, MorphToken
from korean_pronunciation.analyzers.simple_analyzer import SimpleAnalyzer

try:
    from korean_pronunciation.analyzers.kiwi_analyzer import KiwiAnalyzer
    _KIWI_SUPPORTED = True
except ImportError:
    _KIWI_SUPPORTED = False
    KiwiAnalyzer = None  # type: ignore


def get_analyzer() -> BaseMorphAnalyzer:
    """Return the best available morphological analyzer.

    Attempts to return KiwiAnalyzer first, falling back to SimpleAnalyzer
    if kiwipiepy is not installed.
    """
    if _KIWI_SUPPORTED and KiwiAnalyzer is not None:
        try:
            return KiwiAnalyzer()
        except ImportError:
            pass
    return SimpleAnalyzer()
