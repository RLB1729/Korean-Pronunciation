"""Simple morphological analyzer fallback implementation.

Does not require any external dependencies. Splits text by space and uses simple
heuristics to identify common grammatical particles (형식 형태소) like '이', '을', '의'.
"""

from typing import List
from korean_pronunciation.analyzers.base import BaseMorphAnalyzer, MorphToken

# Common Korean grammatical particles (조사) that start with a vowel
# or are otherwise very common for rule testing.
VOWEL_PARTICLES = {
    "이", "가", "을", "를", "은", "는", "의", "에", "도", "와", "과", "로", "으로"
}

# Common verb/adjective endings
COMMON_ENDINGS = {
    "다", "고", "어", "아", "며", "니", "은", "을", "게", "지", "소", "네"
}


class SimpleAnalyzer(BaseMorphAnalyzer):
    """Fallback morphological analyzer using simple heuristics."""

    def analyze(self, text: str) -> List[MorphToken]:
        tokens: List[MorphToken] = []
        i = 0
        n = len(text)
        
        while i < n:
            # Handle non-alphanumeric characters (spaces, punctuation)
            if not text[i].isalnum():
                start = i
                while i < n and not text[i].isalnum():
                    i += 1
                surface = text[start:i]
                tokens.append(MorphToken(
                    surface=surface,
                    tag="SF" if any(c in ".?!," for c in surface) else "SP",
                    start=start,
                    end=i,
                    is_grammatical=True
                ))
                continue
                
            # Read a word (sequence of alphanumeric characters)
            start = i
            while i < n and text[i].isalnum():
                i += 1
            word = text[start:i]
            
            # Simple heuristic to split particles or endings
            split_idx = -1
            
            # Check for trailing particles (e.g. "밭-이", "우리의", "꽃-을")
            if len(word) > 1:
                # 1-char particles
                if word[-1] in VOWEL_PARTICLES or word[-1] in COMMON_ENDINGS:
                    split_idx = len(word) - 1
                # 2-char particles (e.g., "으로")
                elif len(word) > 2 and word[-2:] in VOWEL_PARTICLES:
                    split_idx = len(word) - 2

            if split_idx != -1:
                stem = word[:split_idx]
                particle = word[split_idx:]
                
                stem_tag = "VV" if particle in COMMON_ENDINGS else "NNG"
                # Add stem (lexical)
                tokens.append(MorphToken(
                    surface=stem,
                    tag=stem_tag, # VV if ending, NNG fallback
                    start=start,
                    end=start + split_idx,
                    is_grammatical=False
                ))
                # Add particle/ending (grammatical)
                tokens.append(MorphToken(
                    surface=particle,
                    tag="JXT" if particle in VOWEL_PARTICLES else "EF",
                    start=start + split_idx,
                    end=i,
                    is_grammatical=True
                ))
            else:
                # No split - treat whole word as lexical
                tokens.append(MorphToken(
                    surface=word,
                    tag="NNG",
                    start=start,
                    end=i,
                    is_grammatical=False
                ))
                
        return tokens
