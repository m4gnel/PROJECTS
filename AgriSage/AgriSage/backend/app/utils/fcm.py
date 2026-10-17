import logging
from sqlalchemy import text
from ..database import AsyncSessionLocal

logger = logging.getLogger(__name__)


async def send_push_notification(farmer_id: str, title: str, body: str) -> bool:
    """Send FCM push notification to farmer's registered device."""
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                text("SELECT fcm_token FROM farmers WHERE id = :id"),
                {"id": farmer_id}
            )
            row = result.fetchone()
            if not row or not row[0]:
                logger.info("Farmer %s has no registered FCM token", farmer_id)
                return False

            fcm_token = row[0]

        try:
            import firebase_admin
            from firebase_admin import messaging

            if not firebase_admin._apps:
                firebase_admin.initialize_app()

            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body,
                ),
                token=fcm_token,
            )
            messaging.send(message)
            logger.info("FCM push sent to farmer %s", farmer_id)
            return True
        except ImportError:
            logger.warning("firebase-admin not installed, push notification simulated.")
            return True
    except Exception as e:
        logger.error("Error sending push notification: %s", str(e))
        return False
