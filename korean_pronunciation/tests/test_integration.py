"""Integration tests for the Korean Pronunciation Engine."""

from korean_pronunciation import get_pronunciations, get_pronunciation


def test_seonui():
    # 선의 -> [서늬, 서니] (by vowel rule branching + liaison)
    res = get_pronunciations("선의")
    prons = [r["pronunciation"] for r in res]
    assert "서늬" in prons
    assert "서니" in prons
    assert len(res) == 2


def test_jui():
    # 주의 (non-initial '의' of noun -> [주의, 주이])
    res = get_pronunciations("주의")
    prons = [r["pronunciation"] for r in res]
    assert "주의" in prons
    assert "주이" in prons
    assert len(res) == 2


def test_uri_ui():
    # 우리의 (genitive particle '의' -> [우리의, 우리에])
    res = get_pronunciations("우리의")
    prons = [r["pronunciation"] for r in res]
    assert "우리의" in prons
    assert "우리에" in prons
    assert len(res) == 2


def test_gukmul():
    # 국물 -> [궁물] (nasalization)
    assert get_pronunciation("국물") == "궁물"


def test_ikda():
    # 읽다 -> [익따] (double coda + fortition)
    assert get_pronunciation("읽다") == "익따"


def test_malge():
    # 맑게 -> [말께] (double coda exception + fortition)
    assert get_pronunciation("맑게") == "말께"


def test_osi():
    # 옷이 -> [오시] (liaison)
    assert get_pronunciation("옷이") == "오시"


def test_gapsi():
    # 값이 -> [갑씨] (double coda liaison)
    assert get_pronunciation("값이") == "갑씨"


def test_bat_arae():
    # 밭 아래 -> [바 다래] (neutralization + liaison across spaces)
    assert get_pronunciation("밭 아래") == "바 다래"


def test_h_rule_integration():
    # 놓고 -> [노코] (aspiration)
    assert get_pronunciation("놓고") == "노코"
    
    # 낳은 -> [나은] (deletion)
    assert get_pronunciation("낳은") == "나은"
    
    # 닳소 -> [달쏘] (fortition of ㅅ)
    assert get_pronunciation("닳소") == "달쏘"
    
    # 각하 -> [가카] (reverse aspiration)
    assert get_pronunciation("각하") == "가카"


def test_palatalization_integration():
    # 굳이 -> [구지] (palatalization)
    assert get_pronunciation("굳이") == "구지"
    
    # 같이 -> [가치] (palatalization)
    assert get_pronunciation("같이") == "가치"
    
    # 굳히다 -> [구치다] (aspiration -> palatalization)
    assert get_pronunciation("굳히다") == "구치다"


def test_liquidization_integration():
    # 신라 -> [실라] (liquidization)
    assert get_pronunciation("신라") == "실라"
    
    # 칼날 -> [칼랄] (liquidization)
    assert get_pronunciation("칼날") == "칼랄"
    
    # 의견란 -> [의견난] (liquidization exception)
    assert get_pronunciation("의견란") == "의견난"


def test_extended_fortition_integration():
    # 닮고 -> [담꼬] (verb stem fortition)
    assert get_pronunciation("닮고") == "담꼬"
    
    # 갈등 -> [갈뜽] (Sino-Korean 'ㄹ' fortition)
    assert get_pronunciation("갈등") == "갈뜽"
    
    # 할 것을 -> [할꺼슬] (adnominal fortition)
    assert get_pronunciation("할 것을") == "할 꺼슬"


def test_sound_addition_integration():
    # 솜이불 -> [솜니불] (ㄴ-addition)
    assert get_pronunciation("솜이불") == "솜니불"
    
    # 서울역 -> [서울력] (ㄴ-addition + liquidization)
    assert get_pronunciation("서울역") == "서울력"
    
    # 냇가 -> [내까, 낻까] (saisiot branching)
    res = get_pronunciations("냇가")
    prons = [r["pronunciation"] for r in res]
    assert "내까" in prons
    assert "낻까" in prons
    assert len(res) == 2
    
    # 깻잎 -> [깬닙] (saisiot + ㄴ-addition + neutralization + nasalization)
    assert get_pronunciation("깻잎") == "깬닙"


def test_vowel_rules_additional():
    # 다쳐 -> [다처] (제5항 다만 1)
    assert get_pronunciation("다쳐") == "다처"
    assert get_pronunciation("가져") == "가저"


def test_liaison_exceptions():
    # 맛있다 -> [마딛따, 마싣따]
    res = get_pronunciations("맛있다")
    prons = [r["pronunciation"] for r in res]
    assert "마딛따" in prons
    assert "마싣따" in prons
    assert len(res) == 2


def test_negative_cases():
    # Noun 신고 should NOT be 신꼬
    assert get_pronunciation("신고") == "신고"
    
    # Noun 닭과 should be 닥과 -> 닥꽈, NOT 달꽈
    assert get_pronunciation("닭과") == "닥꽈"


def test_sound_addition_no_bleeding():
    # 물약을 먹은 야옹이 should NOT have ㄴ-addition on 야옹이
    res = get_pronunciations("물약을 먹은 야옹이")
    prons = [r["pronunciation"] for r in res]
    assert "물랴글 머근 야옹이" in prons

