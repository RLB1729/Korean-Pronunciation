"""Vowel rules (제4-5항).

Handles standard and optional/alternative pronunciations for vowels:
- 'ㅖ' pronounced as 'ㅔ' (계집 -> [계집/게집])
- 'ㅢ' with consonant pronounced as 'ㅣ' (희망 -> [히망])
- Non-initial 'ㅢ' pronounced as '이' (주의 -> [주의/주이])
- Genitive particle '의' pronounced as '에' (우리의 -> [우리의/우리에])
"""

from typing import List, Set
from korean_pronunciation.state import PronunciationState, Syllable
from korean_pronunciation.rules.base import BaseRule


class VowelRule(BaseRule):
    """Applies vowel pronunciation rules per article 4 and 5 (supporting branching)."""

    @property
    def name(self) -> str:
        return "VowelRule"

    @property
    def article(self) -> str:
        return "제4-5항"

    def apply(self, state: PronunciationState) -> List[PronunciationState]:
        # Since this rule can branch (generate multiple states), we collect all resulting states.
        current_states = [state]
        n = len(state.syllables)

        for idx in range(n):
            next_states: List[PronunciationState] = []
            
            for s in current_states:
                syl = s.syllables[idx]
                if not syl.is_hangul:
                    next_states.append(s)
                    continue

                # Rule 5, Exception 1: '져, 쪄, 쳐' in verb conjugations must be pronounced as [저, 쩌, 처]
                if syl.jungseong == "ㅕ" and syl.choseong in ("ㅈ", "ㅉ", "ㅊ"):
                    changed_syl = syl.copy(jungseong="ㅓ")
                    next_states.append(s.copy_with_syllable(idx, changed_syl, self.name))
                    continue

                # Rule 5, Exception 2: 'ㅖ' pronounced as 'ㅔ' (except '예', '례')
                if syl.jungseong == "ㅖ" and syl.choseong not in ("ㅇ", "ㄹ"):
                    # Branch 1: keep 'ㅖ'
                    # Branch 2: convert to 'ㅔ'
                    next_states.append(s)
                    
                    changed_syl = syl.copy(jungseong="ㅔ")
                    next_states.append(s.copy_with_syllable(idx, changed_syl, self.name))
                    continue

                # Rule 5, Exception 3: 'ㅢ' with a consonant (not 'ㅇ') must be pronounced as 'ㅣ'
                if syl.jungseong == "ㅢ" and syl.choseong != "ㅇ":
                    changed_syl = syl.copy(jungseong="ㅣ")
                    next_states.append(s.copy_with_syllable(idx, changed_syl, self.name))
                    continue

                # Rule 5, Exception 4: 'ㅢ' with 'ㅇ' onset
                if syl.jungseong == "ㅢ" and syl.choseong == "ㅇ":
                    # Determine if it's the first syllable of a word (word-initial).
                    # A syllable is word-initial if it's at index 0, or if the preceding character
                    # is non-alphanumeric (like a space or punctuation).
                    is_word_initial = (idx == 0)
                    if idx > 0:
                        prev_syl = s.syllables[idx - 1]
                        is_word_initial = not prev_syl.is_hangul or prev_syl.original == " "

                    if is_word_initial:
                        # Word-initial '의' must be '의' (no change)
                        next_states.append(s)
                    else:
                        # Non-initial '의'
                        # Check if it is the genitive particle '의'
                        is_genitive_particle = (
                            syl.morpheme_tag in ("JKG", "JXT") or 
                            (syl.is_grammatical and syl.original == "의")
                        )
                        
                        if is_genitive_particle:
                            # Branch 1: keep '의'
                            # Branch 2: convert to '에'
                            next_states.append(s)
                            
                            changed_syl = syl.copy(jungseong="ㅔ")
                            next_states.append(s.copy_with_syllable(idx, changed_syl, self.name))
                        else:
                            # Branch 1: keep '의'
                            # Branch 2: convert to '이'
                            next_states.append(s)
                            
                            changed_syl = syl.copy(jungseong="ㅣ")
                            next_states.append(s.copy_with_syllable(idx, changed_syl, self.name))
                    continue

                # No vowel changes for this syllable
                next_states.append(s)

            current_states = next_states

        # Deduplicate states before returning
        seen: Set[str] = set()
        dedup_states: List[PronunciationState] = []
        for s in current_states:
            key = s.canonical_key()
            if key not in seen:
                seen.add(key)
                dedup_states.append(s)
                
        return dedup_states
