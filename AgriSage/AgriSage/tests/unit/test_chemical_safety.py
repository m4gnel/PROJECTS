import pytest
from backend.safety.chemical_check import ChemicalSafetyCheck
from backend.safety.hallucination_check import HallucinationCheck


def test_chemical_safety_check_approved():
    checker = ChemicalSafetyCheck()
    is_safe, issues = checker.validate_pesticide("Tricyclazole 75 WP", "rice", dosage=0.5)
    assert is_safe is True
    assert len([i for i in issues if "BLOCK" in i]) == 0


def test_chemical_safety_check_prohibited():
    checker = ChemicalSafetyCheck()
    is_safe, issues = checker.validate_pesticide("Monocrotophos 36 SL", "rice", dosage=1.0)
    assert is_safe is False
    assert any("BLOCK" in issue for issue in issues)


def test_chemical_safety_check_wrong_crop():
    checker = ChemicalSafetyCheck()
    is_safe, issues = checker.validate_pesticide("Tricyclazole 75 WP", "banana", dosage=0.5)
    assert is_safe is False
    assert any("not approved for 'banana'" in issue for issue in issues)


def test_hallucination_check_grounding():
    checker = HallucinationCheck()
    advisory = {
        "citations": [{"doc_id": "icar_paddy_blast_2025"}]
    }
    knowledge = [
        {"id": "icar_paddy_blast_2025", "title": "ICAR Paddy Blast Advisory"}
    ]
    is_grounded, score, issues = checker.verify_grounding(advisory, knowledge)
    assert is_grounded is True
    assert score == 1.0
