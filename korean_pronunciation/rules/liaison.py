"""Liaison rule (제13-16항).

Handles linking of final consonants (coda) to the next syllable's empty initial consonant (onset 'ㅇ').
Supports grammatical liaison (옷이 -> [오시], 값이 -> [갑쓸]) and lexical liaison
after neutralization (밭 아래 -> [바다래], 닭 아래 -> [다가래]).
"""

from typing import List, Tuple
from korean_pronunciation.state import PronunciationState, Syllable
from korean_pronunciation.rules.base import BaseRule
from korean_pronunciation.jamo_constants import (
    DOUBLE_CODA_MAP, CODA_NEUTRALIZATION_MAP
)


class LiaisonRule(BaseRule):
    """Applies Liaison (연음 법칙) per articles 13 to 16."""

    @property
    def name(self) -> str:
        return "Liaison"

    @property
    def article(self) -> str:
        return "제13-16항"

    def apply(self, state: PronunciationState) -> List[PronunciationState]:
        new_syllables = list(state.syllables)
        current_branches = [new_syllables]
        changed = False
        i = 0
        n = len(new_syllables)

        while i < n - 1:
            next_branches: List[List[Syllable]] = []
            
            for branch in current_branches:
                curr_syl = branch[i]
                next_syl = branch[i + 1]

                # Case A: Coda + empty onset directly adjacent (excluding 'ㅇ' coda which never liaisons)
                if (curr_syl.is_hangul and curr_syl.jongseong and curr_syl.jongseong != "ㅇ" and
                        next_syl.is_hangul and next_syl.choseong == "ㅇ"):
                    
                    coda = curr_syl.jongseong
                    
                    # Check for 제15항 다만 exceptions (맛있다, 멋있다)
                    is_mat_meot_it = curr_syl.original in ("맛", "멋") and next_syl.original == "있"
                    
                    if is_mat_meot_it:
                        # Branch 1: Lexical Liaison (Standard) -> [마디-]
                        rep_coda = CODA_NEUTRALIZATION_MAP.get(coda, coda)
                        branch_a = list(branch)
                        branch_a[i] = curr_syl.copy(jongseong="")
                        branch_a[i + 1] = next_syl.copy(choseong=rep_coda)
                        
                        # Branch 2: Grammatical Liaison (Allowed Exception) -> [마시-]
                        branch_b = list(branch)
                        branch_b[i] = curr_syl.copy(jongseong="")
                        branch_b[i + 1] = next_syl.copy(choseong=coda)
                        
                        next_branches.extend([branch_a, branch_b])
                        changed = True
                        continue

                    # Otherwise standard logic
                    is_grammatical = next_syl.is_grammatical
                    
                    # Linguistic override: ㄷ/ㅌ/ㄾ followed by '이' or 'y'-vowel is always grammatical liaison (enabling palatalization)
                    if coda in ("ㄷ", "ㅌ", "ㄾ") and next_syl.jungseong in ("ㅣ", "ㅕ", "야", "요", "유", "ㅒ", "ㅖ"):
                        is_grammatical = True

                    copied_branch = list(branch)
                    if is_grammatical:
                        # Grammatical Liaison (제13-14항)
                        if coda not in DOUBLE_CODA_MAP:
                            # Single coda moves directly
                            copied_branch[i] = curr_syl.copy(jongseong="")
                            copied_branch[i + 1] = next_syl.copy(choseong=coda)
                        else:
                            # Double coda: second consonant moves, first stays
                            first_cons, second_cons = DOUBLE_CODA_MAP[coda]
                            if second_cons == "ㅅ":
                                second_cons = "ㅆ"
                            
                            copied_branch[i] = curr_syl.copy(jongseong=first_cons)
                            copied_branch[i + 1] = next_syl.copy(choseong=second_cons)
                    else:
                        # Lexical Liaison (제15항): Neutralize first, then move
                        rep_coda = CODA_NEUTRALIZATION_MAP.get(coda, coda)
                        copied_branch[i] = curr_syl.copy(jongseong="")
                        copied_branch[i + 1] = next_syl.copy(choseong=rep_coda)
                        
                    next_branches.append(copied_branch)
                    changed = True
                    continue

                # Case B: Coda + space + empty onset (Liaison across word boundary - always Lexical Liaison, excluding 'ㅇ' coda and y-vowels/ㅣ which undergo sound addition)
                elif (curr_syl.is_hangul and curr_syl.jongseong and curr_syl.jongseong != "ㅇ" and
                      not next_syl.is_hangul and next_syl.original == " " and
                      i + 2 < n and branch[i + 2].is_hangul and branch[i + 2].choseong == "ㅇ" and
                      branch[i + 2].jungseong not in ("ㅣ", "ㅑ", "ㅕ", "ㅛ", "ㅠ")):
                    
                    coda = curr_syl.jongseong
                    target_syl = branch[i + 2]
                    
                    # Lexical Liaison: Neutralize first, then move
                    rep_coda = CODA_NEUTRALIZATION_MAP.get(coda, coda)
                    copied_branch = list(branch)
                    copied_branch[i] = curr_syl.copy(jongseong="")
                    copied_branch[i + 2] = target_syl.copy(choseong=rep_coda)
                    next_branches.append(copied_branch)
                    changed = True
                    continue
                
                next_branches.append(branch)
                
            current_branches = next_branches
            i += 1

        if changed:
            seen = set()
            states = []
            for b in current_branches:
                st = PronunciationState(syllables=tuple(b), applied_rules=state.applied_rules + (self.name,))
                key = st.canonical_key()
                if key not in seen:
                    seen.add(key)
                    states.append(st)
            return states
        return [state]
