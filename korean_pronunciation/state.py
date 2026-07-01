"""State definition for the pronunciation engine.

This module defines the Syllable and PronunciationState classes,
which represent the immutable state flowing through the rule pipeline.
"""

from dataclasses import dataclass
from typing import Tuple, List, Optional
from korean_pronunciation import hangul


@dataclass(frozen=True)
class Syllable:
    """Represents a single syllable block, Hangul or non-Hangul.

    Contains the phonetic Jamo components (Choseong, Jungseong, Jongseong)
    along with morphological metadata that remains persistent through transformations.
    """
    choseong: str      # Initial consonant (e.g., "ㄱ", "ㅇ")
    jungseong: str     # Vowel (e.g., "ㅏ", "ㅢ")
    jongseong: str     # Final consonant (e.g., "", "ㄱ", "ㄳ")
    is_hangul: bool    # True if this is a Hangul syllable
    original: str      # The original character before any modifications
    
    # Morphological metadata
    morpheme_tag: str                  # POS tag from morphological analyzer (e.g. "NNG", "JKS", "EF")
    is_grammatical: bool               # True if grammatical morpheme (형식 형태소: 조사, 어미, 접미사)
    has_boundary_before: bool          # True if a morpheme boundary exists immediately before this syllable

    def compose(self) -> str:
        """Compose the syllable back to a single character string."""
        if not self.is_hangul:
            return self.original
        return hangul.compose(self.choseong, self.jungseong, self.jongseong)

    def copy(self, **changes) -> "Syllable":
        """Return a copy of the syllable with the specified changes."""
        # Using a direct dictionary update to speed up copying over dataclass replace
        vals = {
            "choseong": self.choseong,
            "jungseong": self.jungseong,
            "jongseong": self.jongseong,
            "is_hangul": self.is_hangul,
            "original": self.original,
            "morpheme_tag": self.morpheme_tag,
            "is_grammatical": self.is_grammatical,
            "has_boundary_before": self.has_boundary_before
        }
        vals.update(changes)
        return Syllable(**vals)


@dataclass(frozen=True)
class PronunciationState:
    """An immutable state representing a specific pronunciation branch.

    Includes the sequence of syllables, and a history of the rules applied
    to reach this state.
    """
    syllables: Tuple[Syllable, ...]
    applied_rules: Tuple[str, ...] = ()

    def copy_with_syllable(self, index: int, new_syllable: Syllable, rule_name: str) -> "PronunciationState":
        """Return a new state with a modified syllable at the specified index."""
        new_syllables = list(self.syllables)
        new_syllables[index] = new_syllable
        return PronunciationState(
            syllables=tuple(new_syllables),
            applied_rules=self.applied_rules + (rule_name,)
        )

    def copy_with_syllables(self, changes: List[Tuple[int, Syllable]], rule_name: str) -> "PronunciationState":
        """Return a new state with multiple modified syllables."""
        new_syllables = list(self.syllables)
        for idx, new_syllable in changes:
            new_syllables[idx] = new_syllable
        return PronunciationState(
            syllables=tuple(new_syllables),
            applied_rules=self.applied_rules + (rule_name,)
        )

    def copy_with_history(self, rule_name: str) -> "PronunciationState":
        """Return a new state with only the rule history updated."""
        return PronunciationState(
            syllables=self.syllables,
            applied_rules=self.applied_rules + (rule_name,)
        )

    def canonical_key(self) -> str:
        """Generate a canonical string representation for deduplication."""
        return "".join(s.compose() for s in self.syllables)

    def __str__(self) -> str:
        return self.canonical_key()
