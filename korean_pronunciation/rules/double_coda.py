"""Double Coda Simplification rule (제10-11항).

Simplifies double codas (e.g. ㄳ, ㄵ, ㄼ, ㄽ, ㄾ, ㅄ, ㄺ, ㄻ, ㄿ) to single codas
under standard rules and handles official exceptions (e.g. 밟다 -> [밥따], 맑게 -> [말께]).
"""

from typing import List
from korean_pronunciation.state import PronunciationState, Syllable
from korean_pronunciation.rules.base import BaseRule


class DoubleCodaRule(BaseRule):
    """Applies Double Coda Simplification per articles 10 and 11, including exceptions."""

    @property
    def name(self) -> str:
        return "DoubleCoda"

    @property
    def article(self) -> str:
        return "제10-11항"

    def apply(self, state: PronunciationState) -> List[PronunciationState]:
        new_syllables = list(state.syllables)
        changed = False

        for idx, syl in enumerate(new_syllables):
            if not syl.is_hangul or not syl.jongseong:
                continue

            coda = syl.jongseong
            # We only process actual double codas
            if len(coda) < 2 and coda not in ("ㄳ", "ㄵ", "ㄶ", "ㄺ", "ㄻ", "ㄼ", "ㄽ", "ㄾ", "ㄿ", "ㅀ", "ㅄ"):
                continue

            # Skip if followed by a vowel-initial grammatical morpheme (handled by liaison)
            if idx + 1 < len(new_syllables):
                next_syl = new_syllables[idx + 1]
                if next_syl.is_hangul and next_syl.choseong == "ㅇ" and next_syl.is_grammatical:
                    continue

            # Standard and exception rules for double codas
            simplified = coda

            if coda == "ㄼ":
                # Exception 1: '밟-' is pronounced [ㅂ] before a consonant (제10항 다만)
                if syl.original == "밟":
                    simplified = "ㅂ"
                # Exception 2: '넓-' in '넓죽하다', '넓둥글다' is pronounced [넙] (제10항 다만)
                elif syl.original == "넓" and idx + 1 < len(new_syllables):
                    # Check next character(s)
                    next_chars = "".join(s.original for s in new_syllables[idx+1:idx+3])
                    if next_chars.startswith("죽") or next_chars.startswith("둥"):
                        simplified = "ㅂ"
                    else:
                        simplified = "ㄹ"
                else:
                    simplified = "ㄹ"

            elif coda == "ㄺ":
                # Exception: 용언 어간 'ㄺ' is [ㄹ] before a grammatical ending starting with 'ㄱ' (제11항 다만)
                is_yongon = syl.morpheme_tag in ("VV", "VA", "VX")
                if is_yongon and idx + 1 < len(new_syllables):
                    next_syl = new_syllables[idx + 1]
                    # Check if next syllable starts with 'ㄱ' and is grammatical (ending)
                    if next_syl.is_hangul and next_syl.choseong in ("ㄱ", "ㄲ") and next_syl.is_grammatical:
                        simplified = "ㄹ"
                    else:
                        simplified = "ㄱ"
                else:
                    simplified = "ㄱ"

            # Standard simplifications
            elif coda == "ㄳ":
                simplified = "ㄱ"
            elif coda == "ㄵ":
                simplified = "ㄴ"
            elif coda == "ㄶ":
                simplified = "ㄴ"  # Note: ㅎ will be handled by HRule, but fallback to ㄴ
            elif coda == "ㄽ":
                simplified = "ㄹ"
            elif coda == "ㄾ":
                simplified = "ㄹ"
            elif coda == "ㅀ":
                simplified = "ㄹ"  # Note: ㅎ will be handled by HRule
            elif coda == "ㅄ":
                simplified = "ㅂ"
            elif coda == "ㄻ":
                simplified = "ㅁ"
            elif coda == "ㄿ":
                simplified = "ㅂ"  # ㄿ represents ㅂ sound (neutralized from ㅍ)

            if simplified != coda:
                new_syllables[idx] = syl.copy(jongseong=simplified)
                changed = True

        if changed:
            return [PronunciationState(syllables=tuple(new_syllables), applied_rules=state.applied_rules + (self.name,))]
        return [state]
