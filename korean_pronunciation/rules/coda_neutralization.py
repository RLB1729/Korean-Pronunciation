"""Coda Neutralization rule (제8-9항).

Neutralizes single and double-slot codas (e.g. ㄲ, ㅋ -> ㄱ; ㅅ, ㅆ, ㅈ, ㅊ, ㅌ -> ㄷ; ㅍ -> ㅂ)
to one of the 7 standard representative codas: ㄱ, ㄴ, ㄷ, ㄹ, ㅁ, ㅂ, ㅇ.
"""

from typing import List
from korean_pronunciation.state import PronunciationState, Syllable
from korean_pronunciation.rules.base import BaseRule
from korean_pronunciation.jamo_constants import CODA_NEUTRALIZATION_MAP


class CodaNeutralizationRule(BaseRule):
    """Applies Coda Neutralization (음절의 끝소리 규칙) per articles 8 and 9."""

    @property
    def name(self) -> str:
        return "CodaNeutralization"

    @property
    def article(self) -> str:
        return "제8-9항"

    def apply(self, state: PronunciationState) -> List[PronunciationState]:
        new_syllables = list(state.syllables)
        changed = False

        for idx, syl in enumerate(new_syllables):
            if not syl.is_hangul or not syl.jongseong:
                continue

            # Check if there is an upcoming vowel-initial grammatical morpheme.
            # In that case, neutralization is skipped because Grammatical Liaison will/has applied.
            if idx + 1 < len(new_syllables):
                next_syl = new_syllables[idx + 1]
                if next_syl.is_hangul and next_syl.choseong == "ㅇ" and next_syl.is_grammatical:
                    # Skip neutralization; this will be/has been liaisoned directly.
                    continue

            coda = syl.jongseong
            # We only neutralize single codas or double codas that match the standard mappings.
            # Double codas are simplified by DoubleCodaRule, but for robustness we support mapping them here too.
            if coda in CODA_NEUTRALIZATION_MAP:
                rep_coda = CODA_NEUTRALIZATION_MAP[coda]
                if rep_coda != coda:
                    new_syllables[idx] = syl.copy(jongseong=rep_coda)
                    changed = True

        if changed:
            return [PronunciationState(syllables=tuple(new_syllables), applied_rules=state.applied_rules + (self.name,))]
        return [state]
