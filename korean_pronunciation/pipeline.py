"""Standard pronunciation rule pipeline configuration."""

from typing import List
from korean_pronunciation.rules.base import BaseRule
from korean_pronunciation.rules.vowel_rules import VowelRule
from korean_pronunciation.rules.sound_addition import SoundAdditionRule
from korean_pronunciation.rules.h_rule import HRule
from korean_pronunciation.rules.liaison import LiaisonRule
from korean_pronunciation.rules.palatalization import PalatalizationRule
from korean_pronunciation.rules.fortition import FortitionRule
from korean_pronunciation.rules.double_coda import DoubleCodaRule
from korean_pronunciation.rules.coda_neutralization import CodaNeutralizationRule
from korean_pronunciation.rules.nasalization import NasalizationRule
from korean_pronunciation.rules.liquidization import LiquidizationRule


def create_standard_pipeline() -> List[BaseRule]:
    """Create the standard list of pronunciation rules in the correct priority order.

    Rule sequence:
    1. VowelRule (제4-5항) - Applies vowel changes and branches for alternatives early.
    2. SoundAdditionRule (제29-30항) - Inserts 'ㄴ' at compound boundaries early.
    3. HRule (제12항) - Handles 'ㅎ' aspiration, deletion, and nasalization.
    4. LiaisonRule (제13-16항) - Links codas to empty onsets of subsequent syllables.
    5. PalatalizationRule (제17항) - Handles palatalization (ㄷ/ㅌ + ㅣ -> ㅈ/ㅊ).
    6. FortitionRule (제23-27항) - Tensification after obstruents, verb stems, and adnominal modifiers.
    7. DoubleCodaRule (제10-11항) - Simplifies double codas.
    8. CodaNeutralizationRule (제8-9항) - Reduces remaining codas to representative sounds.
    9. NasalizationRule (제18-19항) - Handles sound assimilation near nasals.
    10. LiquidizationRule (제20항) - Handles lateralization/liquidization (ㄴ <-> ㄹ).
    """
    return [
        VowelRule(),
        SoundAdditionRule(),
        HRule(),
        LiaisonRule(),
        PalatalizationRule(),
        FortitionRule(),
        DoubleCodaRule(),
        CodaNeutralizationRule(),
        NasalizationRule(),
        LiquidizationRule(),
    ]
