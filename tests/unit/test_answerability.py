from src.mcg.answerability import assess_answerability
from src.mrec.ir import RankedUDV


def udv(identifier: str, content: str) -> RankedUDV:
    return RankedUDV(
        id=identifier,
        content=content,
        source_doc=f"doc-{identifier}",
        source_type="public-poc",
        icd=0.85,
        similarity=0.7,
        ir=0.6,
        metadata={},
    )


def test_answerability_accepts_documented_design_question():
    result = assess_answerability(
        "Who designed Palacio Cousino?",
        [
            udv(
                "1",
                "Palacio Cousino was designed by French architect Paul Lathoud."
            )
        ],
    )

    assert result.sufficient is True
    assert "designed" in result.matched_terms
    assert "palacio" in result.matched_terms


def test_answerability_accepts_lota_role_question():
    result = assess_answerability(
        "What was Isidora Goyenechea's role in Lota?",
        [
            udv(
                "1",
                "Isidora Goyenechea assumed direction of the industrial "
                "organization of Lota."
            )
        ],
    )

    assert result.sufficient is True
    assert "lota" in result.matched_terms


def test_answerability_rejects_favorite_color():
    result = assess_answerability(
        "What was Isidora Goyenechea's favorite color?",
        [
            udv(
                "1",
                "Isidora Goyenechea developed and enriched Parque de Lota."
            )
        ],
    )

    assert result.sufficient is False
    assert result.matched_terms == ()


def test_answerability_rejects_private_political_opinion():
    result = assess_answerability(
        "What private opinion did Isidora Goyenechea have about modern politics?",
        [
            udv(
                "1",
                "Isidora Goyenechea was involved in the development of Lota."
            )
        ],
    )

    assert result.sufficient is False
