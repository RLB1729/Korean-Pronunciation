"""Unit tests for individual Korean pronunciation rules."""

from korean_pronunciation.state import PronunciationState
from korean_pronunciation.tokenizer import tokenize
from korean_pronunciation.analyzers.simple_analyzer import SimpleAnalyzer
from korean_pronunciation.rules.coda_neutralization import CodaNeutralizationRule
from korean_pronunciation.rules.double_coda import DoubleCodaRule
from korean_pronunciation.rules.liaison import LiaisonRule
from korean_pronunciation.rules.nasalization import NasalizationRule
from korean_pronunciation.rules.fortition import FortitionRule
from korean_pronunciation.rules.vowel_rules import VowelRule
from korean_pronunciation.rules.h_rule import HRule
from korean_pronunciation.rules.palatalization import PalatalizationRule
from korean_pronunciation.rules.liquidization import LiquidizationRule

analyzer = SimpleAnalyzer()


def _get_state(text: str) -> PronunciationState:
    return tokenize(text, analyzer)


def test_coda_neutralization():
    rule = CodaNeutralizationRule()
    
    # 깎 (ㄲ -> ㄱ)
    s = _get_state("깎")
    res = rule.apply(s)
    assert res[0].canonical_key() == "깍"
    
    # 옷 (ㅅ -> ㄷ)
    s = _get_state("옷")
    res = rule.apply(s)
    assert res[0].canonical_key() == "옫"
    
    # 앞 (ㅍ -> ㅂ)
    s = _get_state("앞")
    res = rule.apply(s)
    assert res[0].canonical_key() == "압"


def test_double_coda():
    rule = DoubleCodaRule()
    
    # 넋 (ㄳ -> ㄱ)
    s = _get_state("넋")
    assert rule.apply(s)[0].canonical_key() == "넉"
    
    # 값 (ㅄ -> ㅂ)
    s = _get_state("값")
    assert rule.apply(s)[0].canonical_key() == "갑"
    
    # 닭 (ㄺ -> ㄱ)
    s = _get_state("닭")
    assert rule.apply(s)[0].canonical_key() == "닥"
    
    # 맑게 (ㄺ -> ㄹ exception)
    s = _get_state("맑게")
    syls = list(s.syllables)
    syls[0] = syls[0].copy(morpheme_tag="VV")
    s = PronunciationState(syllables=tuple(syls))
    assert rule.apply(s)[0].canonical_key() == "말게"


def test_liaison():
    rule = LiaisonRule()
    
    # 옷이 (grammatical liaison: single coda moves directly)
    s = _get_state("옷이")
    assert rule.apply(s)[0].canonical_key() == "오시"
    
    # 값이 (grammatical liaison: double coda, 'ㅅ' moves as 'ㅆ')
    s = _get_state("값이")
    assert rule.apply(s)[0].canonical_key() == "갑씨"
    
    # 밭 아래 (lexical liaison: neutralize 'ㅌ' -> 'ㄷ' then move)
    s = _get_state("밭 아래")
    assert rule.apply(s)[0].canonical_key() == "바 다래"


def test_nasalization():
    rule = NasalizationRule()
    
    # 국물 (ㄱ -> ㅇ before ㅁ)
    s = _get_state("국물")
    assert rule.apply(s)[0].canonical_key() == "궁물"
    
    # 닫는 (ㄷ -> ㄴ before ㄴ)
    s = _get_state("닫는")
    assert rule.apply(s)[0].canonical_key() == "단는"
    
    # 침략 (ㄹ -> ㄴ after ㅁ)
    s = _get_state("침략")
    assert rule.apply(s)[0].canonical_key() == "침냑"


def test_fortition():
    rule = FortitionRule()
    
    # 국밥 (ㅂ -> ㅃ after ㄱ)
    s = _get_state("국밥")
    assert rule.apply(s)[0].canonical_key() == "국빱"
    
    # 옷고름 (ㄱ -> ㄲ after ㅅ)
    s = _get_state("옷고름")
    assert rule.apply(s)[0].canonical_key() == "옷꼬름"
    
    # 신고 (verb stem '신' + ending '고' -> [신꼬])
    # For testing, we mock that the verb stem tag VV is used
    s = _get_state("신고")
    # Let's set first syllable tag to VV
    syls = list(s.syllables)
    syls[0] = syls[0].copy(morpheme_tag="VV")
    s = PronunciationState(syllables=tuple(syls))
    assert rule.apply(s)[0].canonical_key() == "신꼬"
    
    # 갈등 (Sino-Korean 'ㄹ' + 'ㄷ' -> [갈뜽])
    s = _get_state("갈등")
    assert rule.apply(s)[0].canonical_key() == "갈뜽"


def test_vowel_rules():
    rule = VowelRule()
    
    # 희망 (ㅢ after consonant -> ㅣ)
    s = _get_state("희망")
    assert rule.apply(s)[0].canonical_key() == "히망"
    
    # 주의 (ㅢ in non-initial -> [주의, 주이])
    s = _get_state("주의")
    # Manually ensure '의' is not treated as grammatical particle for this unit test
    syls = list(s.syllables)
    syls[1] = syls[1].copy(morpheme_tag="NNG", is_grammatical=False)
    s = PronunciationState(syllables=tuple(syls))
    outputs = [st.canonical_key() for st in rule.apply(s)]
    assert "주의" in outputs
    assert "주이" in outputs
    assert len(outputs) == 2
    
    # 우리의 (genitive '의' -> [우리의, 우리에])
    s = _get_state("우리의")
    outputs = [st.canonical_key() for st in rule.apply(s)]
    assert "우리의" in outputs
    assert "우리에" in outputs
    assert len(outputs) == 2


def test_h_rule():
    rule = HRule()
    
    # 놓고 (ㅎ + ㄱ -> ㅋ)
    s = _get_state("놓고")
    assert rule.apply(s)[0].canonical_key() == "노코"
    
    # 쌓은 (ㅎ + grammatical vowel -> silent)
    s = _get_state("쌓은")
    assert rule.apply(s)[0].canonical_key() == "싸은"
    
    # 각하 (ㄱ + ㅎ -> ㅋ)
    s = _get_state("각하")
    assert rule.apply(s)[0].canonical_key() == "가카"


def test_palatalization():
    rule = PalatalizationRule()
    
    # 굳이 (ㄷ + 이 -> [지] - after liaison it becomes '구디' with grammatical/boundary flags)
    # We mock the post-liaison state
    s = _get_state("구디")
    syls = list(s.syllables)
    syls[1] = syls[1].copy(is_grammatical=True, has_boundary_before=True, original="이")
    s = PronunciationState(syllables=tuple(syls))
    assert rule.apply(s)[0].canonical_key() == "구지"


def test_liquidization():
    rule = LiquidizationRule()
    
    # 신라 (ㄴ + ㄹ -> ㄹㄹ)
    s = _get_state("신라")
    assert rule.apply(s)[0].canonical_key() == "실라"
    
    # 칼날 (ㄹ + ㄴ -> ㄹㄹ)
    s = _get_state("칼날")
    assert rule.apply(s)[0].canonical_key() == "칼랄"
    
    # 의견란 (exception: ㄴ + ㄹ -> ㄴㄴ)
    s = _get_state("의견란")
    assert rule.apply(s)[0].canonical_key() == "의견난"


def test_sound_addition():
    from korean_pronunciation.rules.sound_addition import SoundAdditionRule
    rule = SoundAdditionRule()
    
    # 솜이불 (consonant + 이 -> insert ㄴ)
    s = _get_state("솜이불")
    # Mock morpheme boundary flag
    syls = list(s.syllables)
    syls[1] = syls[1].copy(has_boundary_before=True)
    s = PronunciationState(syllables=tuple(syls))
    assert rule.apply(s)[0].canonical_key() == "솜니불"
    
    # 냇가 (saisiot branching -> [내까, 냇까])
    s = _get_state("냇가")
    outputs = [st.canonical_key() for st in rule.apply(s)]
    assert "내까" in outputs
    assert "냇까" in outputs
    assert len(outputs) == 2


def test_h_rule_aspiration_direct():
    rule = HRule()
    # ㅈ + ㅎ should directly map to ㅊ
    s = _get_state("맞히")
    res = rule.apply(s)[0]
    assert res.canonical_key() == "마치"


def test_vowel_rules_additional_unit():
    rule = VowelRule()
    s = _get_state("다쳐")
    assert rule.apply(s)[0].canonical_key() == "다처"


def test_liaison_exceptions_unit():
    rule = LiaisonRule()
    s = _get_state("맛있다")
    res = rule.apply(s)
    outputs = [st.canonical_key() for st in res]
    assert "마딨다" in outputs
    assert "마싰다" in outputs
    assert len(outputs) == 2

