try:
    import structlog
    logger = structlog.get_logger(__name__)
except ImportError:
    import logging
    logger = logging.getLogger(__name__)


class R2StorageService:
    def __init__(self):
        self.bucket = settings.R2_BUCKET
        self.account_id = settings.R2_ACCOUNT_ID
        self.access_key = settings.R2_ACCESS_KEY
        self.secret_key = settings.R2_SECRET_KEY
        self.endpoint_url = f"https://{self.account_id}.r2.cloudflarestorage.com" if self.account_id else None

        if self.access_key and self.secret_key and self.endpoint_url:
            self.client = boto3.client(
                "s3",
                endpoint_url=self.endpoint_url,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                config=Config(signature_version="s3v4"),
                region_name="auto"
            )
        else:
            self.client = None

    async def upload_image(self, file_bytes: bytes, object_key: str) -> str:
        """Upload image bytes to R2 bucket and return public or key URL."""
        if not self.client:
            logger.warning("R2 storage client not configured. Returning key fallback.", object_key=object_key)
            return f"local://{object_key}"

        self.client.put_object(
            Bucket=self.bucket,
            Key=object_key,
            Body=file_bytes,
            ContentType="image/jpeg"
        )
        return f"https://{self.bucket}.r2.cloudflarestorage.com/{object_key}"

    async def delete_image(self, object_key: str):
        """Delete object from R2 bucket."""
        if not self.client:
            return
        self.client.delete_object(Bucket=self.bucket, Key=object_key)

    async def generate_signed_url(self, object_key: str, expires_seconds: int = 3600) -> str:
        """Generate a presigned GET URL for object key."""
        if not self.client:
            return f"http://localhost:8000/media/{object_key}"

        return self.client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket, "Key": object_key},
            ExpiresIn=expires_seconds
        )


r2_storage = R2StorageService()
