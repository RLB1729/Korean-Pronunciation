"""ㅎ Rule (제12항).

Handles all 'ㅎ' 받침 rules, including:
1. 거센소리되기 (Aspiration): ㅎ + ㄱ,ㄷ,ㅈ -> ㅋ,ㅌ,ㅊ; and ㄱ,ㄷ,ㅂ,ㅈ + ㅎ -> ㅋ,ㅌ,ㅍ,ㅊ.
2. 된소리되기 (Fortition): ㅎ + ㅅ -> ㅆ.
3. ㄴ 소리 첨가 (Nasalization): ㅎ + ㄴ -> ㄴ; and ㄶ,ㅀ + ㄴ -> ㄴ/ㄹ.
4. ㅎ 탈락 (Deletion): ㅎ before grammatical vowel -> silent.
"""

from typing import List
from korean_pronunciation.state import PronunciationState, Syllable
from korean_pronunciation.rules.base import BaseRule


class HRule(BaseRule):
    """Applies all ㅎ-related rules per article 12 of Korean Standard Pronunciation."""

    @property
    def name(self) -> str:
        return "HRule"

    @property
    def article(self) -> str:
        return "제12항"

    def apply(self, state: PronunciationState) -> List[PronunciationState]:
        new_syllables = list(state.syllables)
        changed = False
        n = len(new_syllables)

        i = 0
        while i < n:
            curr_syl = new_syllables[i]
            
            # Check if current syllable has ㅎ, ㄶ, ㅀ coda
            if curr_syl.is_hangul and curr_syl.jongseong in ("ㅎ", "ㄶ", "ㅀ"):
                coda = curr_syl.jongseong
                
                # Check next syllable for interactions
                if i + 1 < n:
                    next_syl = new_syllables[i + 1]
                    if next_syl.is_hangul:
                        onset = next_syl.choseong
                        
                        # 1. Aspiration (거센소리되기): ㅎ + ㄱ, ㄷ, ㅈ -> ㅋ, ㅌ, ㅊ
                        if onset in ("ㄱ", "ㄷ", "ㅈ"):
                            aspiration_map = {"ㄱ": "ㅋ", "ㄷ": "ㅌ", "ㅈ": "ㅊ"}
                            target_onset = aspiration_map[onset]
                            
                            # Clear/adjust current coda
                            new_coda = ""
                            if coda == "ㄶ":
                                new_coda = "ㄴ"
                            elif coda == "ㅀ":
                                new_coda = "ㄹ"
                                
                            new_syllables[i] = curr_syl.copy(jongseong=new_coda)
                            new_syllables[i + 1] = next_syl.copy(choseong=target_onset)
                            changed = True
                            i += 2
                            continue
                            
                        # 2. Fortition: ㅎ + ㅅ -> ㅆ
                        elif onset == "ㅅ":
                            new_coda = ""
                            if coda == "ㄶ":
                                new_coda = "ㄴ"
                            elif coda == "ㅀ":
                                new_coda = "ㄹ"
                                
                            new_syllables[i] = curr_syl.copy(jongseong=new_coda)
                            new_syllables[i + 1] = next_syl.copy(choseong="ㅆ")
                            changed = True
                            i += 2
                            continue
                            
                        # 3. Nasalization: ㅎ + ㄴ -> ㄴ; ㄶ,ㅀ + ㄴ -> ㄴ/ㄹ
                        elif onset == "ㄴ":
                            if coda == "ㅎ":
                                new_coda = "ㄴ"
                            elif coda == "ㄶ":
                                new_coda = "ㄴ"
                            elif coda == "ㅀ":
                                new_coda = "ㄹ"
                                
                            new_syllables[i] = curr_syl.copy(jongseong=new_coda)
                            changed = True
                            i += 1
                            continue
                            
                        # 4. ㅎ-Deletion: ㅎ before grammatical vowel -> silent
                        elif onset == "ㅇ" and next_syl.is_grammatical:
                            new_coda = ""
                            if coda == "ㄶ":
                                new_coda = "ㄴ"
                            elif coda == "ㅀ":
                                new_coda = "ㄹ"
                                
                            new_syllables[i] = curr_syl.copy(jongseong=new_coda)
                            changed = True
                            i += 1
                            continue

            # Check for the reverse aspiration: plosive + ㅎ -> aspirated (제12항 붙임 1 & 2)
            if (curr_syl.is_hangul and curr_syl.jongseong and 
                    i + 1 < n and new_syllables[i + 1].is_hangul and new_syllables[i + 1].choseong == "ㅎ"):
                coda = curr_syl.jongseong
                next_syl = new_syllables[i + 1]
                
                # Check if coda is a plosive or neutralizes to a plosive (ㄱ, ㄷ, ㅂ, ㅈ)
                # Single/double codas triggering aspiration:
                # - ㄱ, ㄺ -> ㅋ
                # - ㄷ, ㅅ, ㅆ, ㅈ, ㅊ, ㅌ -> ㅌ
                # - ㅂ, ㄼ, ㄿ -> ㅍ
                # - ㄵ -> ㅊ
                
                asp_onset = ""
                new_coda = ""
                
                if coda in ("ㄱ", "ㄺ"):
                    asp_onset = "ㅋ"
                    new_coda = "ㄹ" if coda == "ㄺ" else ""
                elif coda in ("ㄷ", "ㅅ", "ㅆ", "ㅌ"):
                    asp_onset = "ㅌ"
                    new_coda = ""
                elif coda in ("ㅂ", "ㄼ", "ㄿ"):
                    asp_onset = "ㅍ"
                    new_coda = "ㄹ" if coda == "ㄼ" else ""
                elif coda in ("ㅈ", "ㅊ"):
                    asp_onset = "ㅊ"
                    new_coda = ""
                elif coda == "ㄵ":
                    asp_onset = "ㅊ"
                    new_coda = "ㄴ"
                    
                if asp_onset:
                    new_syllables[i] = curr_syl.copy(jongseong=new_coda)
                    new_syllables[i + 1] = next_syl.copy(choseong=asp_onset)
                    changed = True
                    i += 2
                    continue

            i += 1

        if changed:
            return [PronunciationState(syllables=tuple(new_syllables), applied_rules=state.applied_rules + (self.name,))]
        return [state]
