from typing import Dict, Any, Optional
try:
    import structlog
    logger = structlog.get_logger(__name__)
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

from backend.config import settings

try:
    import firebase_admin
    from firebase_admin import credentials, messaging
except ImportError:
    firebase_admin = None
    messaging = None


class FCMNotificationService:
    def __init__(self):
        if firebase_admin and settings.FCM_KEY and not firebase_admin._apps:
            try:
                cred = credentials.Certificate(settings.FCM_KEY)
                firebase_admin.initialize_app(cred)
            except Exception as e:
                logger.warning("fcm_init_warning", error=str(e))

    async def send(self, fcm_token: Optional[str], title: str, body: str, data: Optional[Dict[str, str]] = None) -> bool:
        """Send FCM push notification. Returns True on success, False on failure."""
        if not fcm_token or not messaging:
            logger.info("fcm_send_skipped", reason="No FCM token or SDK missing", title=title)
            return False

        try:
            msg = messaging.Message(
                notification=messaging.Notification(title=title, body=body),
                data=data or {},
                token=fcm_token
            )
            messaging.send(msg)
            return True
        except Exception as e:
            logger.error("fcm_send_failed", error=str(e))
            return False


notification_service = FCMNotificationService()
