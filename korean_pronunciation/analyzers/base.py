"""Base definition for Korean Morphological Analyzers."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class MorphToken:
    """Represents a single morpheme token from an analyzer."""
    surface: str       # The substring (e.g. "선", "의")
    tag: str           # The Part-of-Speech tag (e.g. "NNG", "JKG")
    start: int         # Start character index in the original text
    end: int           # End character index in the original text
    is_grammatical: bool  # True if it's a grammatical morpheme (형식 형태소)


class BaseMorphAnalyzer(ABC):
    """Abstract base class for morphological analyzers."""

    @abstractmethod
    def analyze(self, text: str) -> List[MorphToken]:
        """Analyze the input text and return a list of MorphToken objects."""
        pass
