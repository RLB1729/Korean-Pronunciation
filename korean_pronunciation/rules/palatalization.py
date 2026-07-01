"""Palatalization rule (제17항).

Handles palatalization of 'ㄷ', 'ㅌ' to 'ㅈ', 'ㅊ' before 'ㅣ' or 'y'-vowels
at grammatical morpheme boundaries (굳이 -> [구지], 같이 -> [가치], 굳히다 -> [구치다]).
"""

from typing import List
from korean_pronunciation.state import PronunciationState, Syllable
from korean_pronunciation.rules.base import BaseRule
from korean_pronunciation import hangul


class PalatalizationRule(BaseRule):
    """Applies Palatalization (구개음화) per article 17, including the '붙임' case."""

    @property
    def name(self) -> str:
        return "Palatalization"

    @property
    def article(self) -> str:
        return "제17항"

    def apply(self, state: PronunciationState) -> List[PronunciationState]:
        new_syllables = list(state.syllables)
        changed = False
        n = len(new_syllables)

        # Palatalization occurs when 'ㄷ' or 'ㅌ' onset is combined with 'ㅣ' or 'y'-vowels
        # ('ㅕ', 'ㅑ', 'ㅛ', 'ㅠ', 'ㅒ', 'ㅖ') at a grammatical morpheme boundary.
        # Thanks to liaison/aspiration running first, the 'ㄷ' or 'ㅌ' has already moved
        # to the onset of the grammatical syllable.
        for idx in range(n):
            syl = new_syllables[idx]
            
            # Check if this syllable was originally vowel-initial (starting with ㅇ or ㅎ)
            # which indicates it was liaisoned or aspirated from a preceding coda.
            is_originally_vowel_or_h = False
            if syl.original and hangul.is_hangul_syllable(syl.original):
                orig_cho, _, _ = hangul.decompose(syl.original)
                is_originally_vowel_or_h = orig_cho in ("ㅇ", "ㅎ")

            # Condition: must match onset & vowel, and must be either:
            # - Grammatical boundary (from analyzer)
            # - Originally starting with ㅇ or ㅎ (which guarantees it was liaisoned/aspirated across a boundary)
            if (syl.is_hangul and 
                    syl.choseong in ("ㄷ", "ㅌ") and 
                    syl.jungseong in ("ㅣ", "ㅕ", "야", "요", "유", "ㅒ", "ㅖ") and
                    is_originally_vowel_or_h and
                    (syl.is_grammatical or (not syl.has_boundary_before and not syl.jongseong))):
                
                target_onset = "ㅈ" if syl.choseong == "ㄷ" else "ㅊ"
                new_syllables[idx] = syl.copy(choseong=target_onset)
                changed = True

        if changed:
            return [PronunciationState(syllables=tuple(new_syllables), applied_rules=state.applied_rules + (self.name,))]
        return [state]
