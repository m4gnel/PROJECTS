from .state import AgriState
from ..utils.gemini import ask_gemini
from datetime import datetime, timezone, timedelta
import uuid


async def alert_node(state: AgriState) -> dict:
    """
    Generates structured alerts from pest_alerts + agent_findings.
    Also synthesizes advisory_text using Gemini.
    Returns: {"alerts_generated": [...], "advisory_text": "...", "confidence_score": float, "agents_completed": ["alert"]}
    """
    try:
        findings = state.get("agent_findings", [])
        pest_alerts = state.get("pest_alerts", [])
        query = state.get("query", "")
        language = state.get("language", "en")

        alerts_generated = []
        tz = timezone(timedelta(hours=5, minutes=30))

        # Generate alerts from pest alerts
        for pest in pest_alerts[:3]:
            alerts_generated.append({
                "id": str(uuid.uuid4()),
                "severity": "WARNING",
                "title": "Pest/Disease Alert",
                "message": pest[:500],
                "timestamp": datetime.now(tz).isoformat(),
            })

        # Synthesize advisory text from all findings
        all_context = "\n".join(findings)
        if pest_alerts:
            all_context += "\nPest alerts: " + "; ".join(pest_alerts[:2])

        prompt = (
            f"Farmer's question: {query}\n\n"
            f"Data collected by AI agents:\n{all_context}\n\n"
            f"Generate a practical, actionable advisory for a Kerala smallholder farmer. "
            f"Be specific with quantities and timing. Keep it under 200 words in English."
        )

        advisory = await ask_gemini(
            prompt,
            "You are Agri-SAGE, an expert agricultural advisor for Kerala smallholder farmers."
        )

        confidence = min(0.95, 0.5 + len(findings) * 0.08)

        return {
            "alerts_generated": alerts_generated,
            "advisory_text": advisory,
            "confidence_score": confidence,
            "agents_completed": ["alert"],
        }
    except Exception as e:
        return {
            "advisory_text": "Unable to generate advisory at this time. Please try again.",
            "confidence_score": 0.0,
            "error_messages": [f"alert: {str(e)}"],
            "agents_completed": ["alert"],
        }
