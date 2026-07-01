"""Base class definition for Korean pronunciation rules."""

from abc import ABC, abstractmethod
from typing import List
from korean_pronunciation.state import PronunciationState


class BaseRule(ABC):
    """Abstract base class for all pronunciation rules.

    Each rule is responsible for:
    - Determining if it is applicable to the current state.
    - Implementing the specific phonetic transformation.
    - Returning a list of all possible output states (allowing branching).
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """User-friendly name of the rule."""
        pass

    @property
    @abstractmethod
    def article(self) -> str:
        """The article number of the Korean Standard Pronunciation Rules (e.g., '제8항')."""
        pass

    @abstractmethod
    def apply(self, state: PronunciationState) -> List[PronunciationState]:
        """Apply this rule to the pronunciation state.

        Returns:
            A list of new PronunciationState instances.
            For non-branching (deterministic) rules, this list contains exactly 1 element.
            For optional/branching rules, it contains multiple elements.
        """
        pass
