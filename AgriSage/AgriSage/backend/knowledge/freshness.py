from datetime import datetime, timedelta
from typing import Dict, Any, List


class KnowledgeFreshnessTracker:
    """Tracks freshness, TTL, and re-indexing status of ICAR/KAU knowledge documents."""

    def __init__(self, default_ttl_days: int = 90):
        self.default_ttl_days = default_ttl_days

    def evaluate_freshness(self, document_metadata: Dict[str, Any]) -> Dict[str, Any]:
        last_updated_str = document_metadata.get("last_updated") or document_metadata.get("published_date")
        
        if not last_updated_str:
            return {"is_fresh": True, "age_days": 0, "needs_reindex": False, "status": "FRESH"}

        try:
            last_updated = datetime.strptime(last_updated_str[:10], "%Y-%m-%d")
            age_days = (datetime.utcnow() - last_updated).days
        except Exception:
            age_days = 0

        is_fresh = age_days <= self.default_ttl_days
        needs_reindex = age_days > (self.default_ttl_days * 0.8)

        return {
            "is_fresh": is_fresh,
            "age_days": age_days,
            "needs_reindex": needs_reindex,
            "status": "FRESH" if is_fresh else "STALE"
        }
