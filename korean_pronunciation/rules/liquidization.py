"""Liquidization rule (제20항).

Handles lateralization/liquidization of 'ㄴ' to 'ㄹ' before or after 'ㄹ' (신라 -> [실라], 칼날 -> [칼랄]).
Includes the official '다만' exceptions where 'ㄹ' becomes 'ㄴ' instead (의견란 -> [의견난], 생산량 -> [생산냥]).
"""

from typing import List
from korean_pronunciation.state import PronunciationState, Syllable
from korean_pronunciation.rules.base import BaseRule

# Official exceptions where ㄴ + ㄹ is pronounced as [ㄴ + ㄴ] instead of [ㄹ + ㄹ] (제20항 다만)
LIQUIDIZATION_EXCEPTIONS = {
    "의견란", "임진란", "생산량", "결단력", "공권력", "이원론", "입원료", 
    "동원령", "상견례", "횡단로", "구도난", "광한루"
}


class LiquidizationRule(BaseRule):
    """Applies Liquidization (유음화) per article 20, including '다만' exceptions."""

    @property
    def name(self) -> str:
        return "Liquidization"

    @property
    def article(self) -> str:
        return "제20항"

    def apply(self, state: PronunciationState) -> List[PronunciationState]:
        new_syllables = list(state.syllables)
        changed = False
        n = len(new_syllables)
        
        # Compose the current text to check for exceptions
        full_text = state.canonical_key()
        
        # Helper to check if a specific index boundary falls within a known exception word
        def is_exception_boundary(idx: int) -> bool:
            orig_text = "".join(s.original for s in new_syllables)
            char_idx = 0
            for s_i in range(idx):
                char_idx += len(new_syllables[s_i].original)
            
            for exc in LIQUIDIZATION_EXCEPTIONS:
                start = 0
                while True:
                    start_pos = orig_text.find(exc, start)
                    if start_pos == -1:
                        break
                    boundary_char_pos = char_idx + len(new_syllables[idx].original) - 1
                    if start_pos <= boundary_char_pos < start_pos + len(exc) - 1:
                        return True
                    start = start_pos + 1
            return False

        # Apply Rule 20
        for i in range(n - 1):
            curr_syl = new_syllables[i]
            next_syl = new_syllables[i + 1]

            if curr_syl.is_hangul and next_syl.is_hangul:
                # Case 1: ㄴ + ㄹ
                if curr_syl.jongseong == "ㄴ" and next_syl.choseong == "ㄹ":
                    if is_exception_boundary(i):
                        # Exception: ㄹ becomes ㄴ (의견란 -> 의견난)
                        new_syllables[i + 1] = next_syl.copy(choseong="ㄴ")
                        changed = True
                    else:
                        # Standard: ㄴ becomes ㄹ (신라 -> 실라)
                        new_syllables[i] = curr_syl.copy(jongseong="ㄹ")
                        changed = True
                        
                # Case 2: ㄹ + ㄴ
                elif curr_syl.jongseong == "ㄹ" and next_syl.choseong == "ㄴ":
                    # Standard: ㄴ becomes ㄹ (칼날 -> 칼랄)
                    new_syllables[i + 1] = next_syl.copy(choseong="ㄹ")
                    changed = True

        if changed:
            return [PronunciationState(syllables=tuple(new_syllables), applied_rules=state.applied_rules + (self.name,))]
        return [state]
