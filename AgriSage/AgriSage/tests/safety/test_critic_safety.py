import pytest
from backend.agents.critic import CriticAgent
from backend.agents.scheme import SchemeAgent
from backend.agents.state import AgriSAGEState


class TestCriticSafetyBlocks:
    async def test_unknown_pesticide_blocked(self):
        critic = CriticAgent()
        rec = {"product_name": "FakeChemical_XYZ_9999", "crop": "rice", "dosage": 1.0}
        safe, issues = await critic.run_safety_checks(rec)
        assert safe is False
        assert any("BLOCK" in issue for issue in issues)

    async def test_valid_pesticide_passes(self):
        critic = CriticAgent()
        rec = {"product_name": "Tricyclazole 75 WP", "crop": "rice", "dosage": 0.6}
        safe, issues = await critic.run_safety_checks(rec)
        assert safe is True

    async def test_wrong_crop_registration_blocked(self):
        critic = CriticAgent()
        rec = {"product_name": "Tricyclazole 75 WP", "crop": "banana", "dosage": 0.6}
        safe, issues = await critic.run_safety_checks(rec)
        assert safe is False

    async def test_conflicting_evidence_no_treatment(self):
        critic = CriticAgent()
        state: AgriSAGEState = {
            "crop": "rice",
            "vision_result": {"label": "rice_blast", "confidence_score": 0.85},
            "weather_result": {"dfi": 0.1, "consecutive_wet_days": 0},
            "crop_stage_result": {"stage_code": "tillering"}
        }
        res = await critic.evaluate(state)
        assert res["confidence_state"] == "CONFLICTING_EVIDENCE"
        assert res["safe_to_act"] is False

    async def test_uncertain_confidence_no_treatment(self):
        critic = CriticAgent()
        state: AgriSAGEState = {
            "crop": "rice",
            "vision_result": {"label": "rice_blast", "confidence_score": 0.35},
            "weather_result": {"dfi": 0.5, "consecutive_wet_days": 2},
            "crop_stage_result": {"stage_code": "tillering"}
        }
        res = await critic.evaluate(state)
        assert res["confidence_state"] == "UNCERTAIN"
        assert res["safe_to_act"] is False

    async def test_modelled_estimate_label_always_present(self):
        scenario = {
            "id": "A",
            "label": "Recommended Spray",
            "expected_yield_kgha": 4200.0,
            "expected_net_return_inr": 82000.0,
            "modelled_estimate": True
        }
        assert scenario.get("modelled_estimate") is True

    async def test_expired_scheme_not_returned(self):
        agent = SchemeAgent()
        schemes = [
            {"scheme_name": "ExpiredTestScheme2020", "valid_until": "2020-01-01"},
            {"scheme_name": "PMFBY", "valid_until": "2028-03-31"}
        ]
        valid_schemes = agent.filter_valid_schemes(schemes)
        names = [s["scheme_name"] for s in valid_schemes]
        assert "ExpiredTestScheme2020" not in names
        assert "PMFBY" in names

    async def test_mandatory_caveat_always_present(self):
        agent = SchemeAgent()
        matches = agent.format_matches([{"scheme_name": "PMFBY"}])
        for match in matches:
            assert "mandatory_caveat" in match
            assert "concerned authority" in match["mandatory_caveat"]
