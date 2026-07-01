"""Fortition rule (제23-27항).

Handles tensification (경음화) of plain/lenis consonants (ㄱ, ㄷ, ㅂ, ㅅ, ㅈ) under:
- 제23항: After plosive/obstruent codas (ㄱ, ㄷ, ㅂ).
- 제24항: After verb stems ending in ㄴ(ㄵ), ㅁ(ㄻ) followed by grammatical endings (except '-기-').
- 제25항: After verb stems ending in ㄼ, ㄾ followed by grammatical endings.
- 제26항: In Sino-Korean words after 'ㄹ' coda (excluding reduplications).
- 제27항: After adnominal ending '-(으)ㄹ'.
"""

from typing import List
from korean_pronunciation.state import PronunciationState, Syllable
from korean_pronunciation.rules.base import BaseRule
from korean_pronunciation.jamo_constants import FORTITION_MAP


class FortitionRule(BaseRule):
    """Applies Fortition (경음화) per articles 23 to 27."""

    @property
    def name(self) -> str:
        return "Fortition"

    @property
    def article(self) -> str:
        return "제23-27항"

    def apply(self, state: PronunciationState) -> List[PronunciationState]:
        new_syllables = list(state.syllables)
        changed = False
        n = len(new_syllables)

        i = 0
        while i < n - 1:
            curr_syl = new_syllables[i]
            next_syl = new_syllables[i + 1]

            if not curr_syl.is_hangul:
                i += 1
                continue

            coda = curr_syl.jongseong

            # --- Rule 23: Post-Obstruent Fortition ---
            # Obstruent codas: ㄱ, ㄷ, ㅂ, ㄲ, ㅋ, ㅅ, ㅆ, ㅈ, ㅊ, ㅌ, ㅍ, ㄳ, ㅄ, ㄺ, ㄼ, ㄿ
            is_obstruent = coda in (
                "ㄱ", "ㄷ", "ㅂ", "ㄲ", "ㅋ", "ㅅ", "ㅆ", "ㅈ", "ㅊ", "ㅌ", "ㅍ",
                "ㄳ", "ㅄ", "ㄺ", "ㄼ", "ㄿ"
            )
            if is_obstruent and next_syl.is_hangul and next_syl.choseong in FORTITION_MAP:
                tense_onset = FORTITION_MAP[next_syl.choseong]
                new_syllables[i + 1] = next_syl.copy(choseong=tense_onset)
                changed = True
                i += 1
                continue

            # --- Rule 24: Verb stem ㄴ(ㄵ), ㅁ(ㄻ) + endings ---
            # e.g. 신고 -> [신꼬], 앉고 -> [안꼬], 닮고 -> [담꼬]
            is_verb_stem = curr_syl.morpheme_tag in ("VV", "VA", "VX")
            if is_verb_stem and coda in ("ㄴ", "ㄵ", "ㅁ", "ㄻ") and next_syl.is_hangul:
                # Exclude passive/causative suffix '-기-'
                is_causative_gi = next_syl.original == "기" and next_syl.morpheme_tag.startswith("XS")
                if next_syl.choseong in ("ㄱ", "ㄷ", "ㅅ", "ㅈ") and next_syl.is_grammatical and not is_causative_gi:
                    tense_onset = FORTITION_MAP[next_syl.choseong]
                    new_syllables[i + 1] = next_syl.copy(choseong=tense_onset)
                    changed = True
                    i += 1
                    continue

            # --- Rule 25: Verb stem ㄼ, ㄾ + endings ---
            # e.g. 넓게 -> [널께], 핥다 -> [할따]
            if is_verb_stem and coda in ("ㄼ", "ㄾ") and next_syl.is_hangul:
                if next_syl.choseong in ("ㄱ", "ㄷ", "ㅅ", "ㅈ") and next_syl.is_grammatical:
                    tense_onset = FORTITION_MAP[next_syl.choseong]
                    new_syllables[i + 1] = next_syl.copy(choseong=tense_onset)
                    changed = True
                    i += 1
                    continue

            # --- Rule 26: Sino-Korean 'ㄹ' + ㄷ, ㅅ, ㅈ ---
            # e.g. 갈등 -> [갈뜽], 물질 -> [물찔]
            is_noun_like = curr_syl.morpheme_tag not in ("VV", "VA", "VX")
            if is_noun_like and coda == "ㄹ" and next_syl.is_hangul:
                if next_syl.choseong in ("ㄷ", "ㅅ", "ㅈ"):
                    # Check for reduplication (e.g. 허허실실, 절절하다)
                    is_reduplication = False
                    if i > 0 and i + 2 < n:
                        # Simple check if current syllable and next syllable form a repeating character
                        if curr_syl.original == new_syllables[i + 1].original:
                            is_reduplication = True
                    
                    if not is_reduplication:
                        tense_onset = FORTITION_MAP[next_syl.choseong]
                        new_syllables[i + 1] = next_syl.copy(choseong=tense_onset)
                        changed = True
                        i += 1
                        continue

            # --- Rule 27: Adnominal modifier '-(으)ㄹ' + word boundary ---
            # e.g. 할 것을 -> [할꺼슬], 갈 데가 -> [갈떼가]
            if coda == "ㄹ" and (curr_syl.morpheme_tag == "ETM" or curr_syl.morpheme_tag.startswith("V")) and i + 2 < n:
                # Expecting a space/punctuation in between, then a word
                space_syl = new_syllables[i + 1]
                target_syl = new_syllables[i + 2]
                if not space_syl.is_hangul and space_syl.original == " " and target_syl.is_hangul:
                    if target_syl.choseong in FORTITION_MAP:
                        tense_onset = FORTITION_MAP[target_syl.choseong]
                        new_syllables[i + 2] = target_syl.copy(choseong=tense_onset)
                        changed = True
                        i += 2
                        continue

            i += 1

        if changed:
            return [PronunciationState(syllables=tuple(new_syllables), applied_rules=state.applied_rules + (self.name,))]
        return [state]
