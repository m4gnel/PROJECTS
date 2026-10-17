import logging
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

try:
    import feedparser
except ImportError:
    feedparser = None

KERALA_CROPS = [
    "coconut", "rice", "banana", "rubber", "tapioca",
    "pepper", "cardamom", "ginger", "turmeric", "arecanut"
]


@dataclass
class PestAlertContext:
    alerts: List[Dict[str, Any]]
    highest_severity: str  # HIGH | MEDIUM | LOW | NONE


# In-memory store for active pest alerts
_PEST_ALERTS_DB: List[Dict[str, Any]] = [
    {
        "title": "Rugose Spiraling Whitefly Alert on Coconut in Ernakulam",
        "description": "High incidence of rugose spiraling whitefly reported on coconut palms across Ernakulam district.",
        "severity": "HIGH",
        "affected_crops": ["coconut"],
        "pub_date": "2026-10-01"
    }
]


class PestService:
    def classify_severity(self, text: str) -> str:
        t = text.lower()
        if any(w in t for w in ["outbreak", "severe", "emergency", "epidemic"]):
            return "HIGH"
        if any(w in t for w in ["alert", "warning", "caution", "incidence"]):
            return "MEDIUM"
        return "LOW"

    def extract_affected_crops(self, text: str) -> List[str]:
        t = text.lower()
        return [c for c in KERALA_CROPS if c in t]

    async def fetch_rss_alerts(self) -> List[Dict[str, Any]]:
        if feedparser is None:
            logger.warning("pest_service_feedparser_missing")
            return _PEST_ALERTS_DB

        url = "https://nbair.res.in/PestAlerts/rassFeed.php"
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                title = getattr(entry, "title", "")
                desc = getattr(entry, "description", "")
                full_text = f"{title} {desc}"
                severity = self.classify_severity(full_text)
                crops = self.extract_affected_crops(full_text)
                if crops:
                    _PEST_ALERTS_DB.append({
                        "title": title,
                        "description": desc,
                        "severity": severity,
                        "affected_crops": crops,
                        "pub_date": getattr(entry, "published", "")
                    })
        except Exception as e:
            logger.warning("pest_service_fetch_error", error=str(e))

        return _PEST_ALERTS_DB

    async def get_alerts_for_district_and_crop(
        self,
        district: str = "Ernakulam",
        crop: Optional[str] = None
    ) -> PestAlertContext:
        crop_lower = crop.lower() if crop else None
        district_lower = district.lower()

        matching = []
        for alert in _PEST_ALERTS_DB:
            alert_text = f"{alert.get('title', '')} {alert.get('description', '')}".lower()
            crops = alert.get("affected_crops", [])

            # Check crop match if crop specified
            crop_match = (not crop_lower) or (crop_lower in crops) or (crop_lower in alert_text)
            if crop_match:
                matching.append(alert)

        highest = "NONE"
        if any(a["severity"] == "HIGH" for a in matching):
            highest = "HIGH"
        elif any(a["severity"] == "MEDIUM" for a in matching):
            highest = "MEDIUM"
        elif matching:
            highest = "LOW"

        return PestAlertContext(alerts=matching, highest_severity=highest)


pest_service = PestService()
