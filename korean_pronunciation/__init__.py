"""Korean Pronunciation Engine.

A high-quality library that converts Korean text into all valid pronunciations
according to the Korean Standard Pronunciation Rules (표준 발음법).
"""

from typing import List
from korean_pronunciation.engine import PronunciationEngine
from korean_pronunciation.pipeline import create_standard_pipeline
from korean_pronunciation.analyzers import get_analyzer

__version__ = "0.1.0"


def get_pronunciations(text: str) -> List[dict]:
    """Convert input Korean text into all valid standard pronunciations.

    Args:
        text: The Korean input word or sentence.

    Returns:
        A list of dicts representing all valid pronunciations with applied rules metadata.
    """
    pipeline = create_standard_pipeline()
    engine = PronunciationEngine(pipeline=pipeline)
    return engine.get_pronunciations(text)


def get_pronunciation(text: str) -> str:
    """Convert input Korean text into its primary standard pronunciation.

    Args:
        text: The Korean input word or sentence.

    Returns:
        A string representing the primary standard pronunciation.
    """
    results = get_pronunciations(text)
    if not results:
        return ""
    # Return the first result's pronunciation string
    return results[0]["pronunciation"]
