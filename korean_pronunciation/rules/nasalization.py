"""Nasalization rule (제18-19항).

Handles nasalization of plosives before nasal consonants (국물 -> [궁물])
and nasalization of 'ㄹ' after non-plosive consonants or other nasals (침략 -> [침냑], 협력 -> [혐녁]).
"""

from typing import List
from korean_pronunciation.state import PronunciationState, Syllable
from korean_pronunciation.rules.base import BaseRule


class NasalizationRule(BaseRule):
    """Applies Nasalization (비음화) per articles 18 and 19."""

    @property
    def name(self) -> str:
        return "Nasalization"

    @property
    def article(self) -> str:
        return "제18-19항"

    def apply(self, state: PronunciationState) -> List[PronunciationState]:
        new_syllables = list(state.syllables)
        changed = False
        n = len(new_syllables)

        # Step 1: Article 19 (ㄹ -> ㄴ after certain consonants)
        for i in range(n - 1):
            curr_syl = new_syllables[i]
            next_syl = new_syllables[i + 1]

            if (curr_syl.is_hangul and curr_syl.jongseong and
                    next_syl.is_hangul and next_syl.choseong == "ㄹ"):
                
                coda = curr_syl.jongseong
                # ㄹ becomes ㄴ after ㅁ, ㅇ, ㄱ, ㅂ, ㄷ, etc.
                if coda in ("ㅁ", "ㅇ", "ㄱ", "ㅂ", "ㄷ", "ㄲ", "ㅋ", "ㅌ", "ㅍ", "ㅅ", "ㅆ", "ㅈ", "ㅊ"):
                    new_syllables[i + 1] = next_syl.copy(choseong="ㄴ")
                    changed = True

        # Step 2: Article 18 (ㄱ, ㄷ, ㅂ -> ㅇ, ㄴ, ㅁ before ㄴ, ㅁ)
        for i in range(n - 1):
            curr_syl = new_syllables[i]
            next_syl = new_syllables[i + 1]

            if (curr_syl.is_hangul and curr_syl.jongseong and
                    next_syl.is_hangul and next_syl.choseong in ("ㄴ", "ㅁ")):
                
                coda = curr_syl.jongseong
                new_coda = coda

                # Plosives (after neutralization, they are ㄱ, ㄷ, ㅂ)
                if coda in ("ㄱ", "ㄲ", "ㅋ"):
                    new_coda = "ㅇ"
                elif coda in ("ㄷ", "ㅅ", "ㅆ", "ㅈ", "ㅊ", "ㅌ", "ㅎ"):
                    new_coda = "ㄴ"
                elif coda in ("ㅂ", "ㅍ"):
                    new_coda = "ㅁ"

                if new_coda != coda:
                    new_syllables[i] = curr_syl.copy(jongseong=new_coda)
                    changed = True

        if changed:
            return [PronunciationState(syllables=tuple(new_syllables), applied_rules=state.applied_rules + (self.name,))]
        return [state]
