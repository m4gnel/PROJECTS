import io
from PIL import Image
import magic

MAX_SIZE_BYTES = 5 * 1024 * 1024
ALLOWED_MIMES = {"image/jpeg", "image/png", "image/webp"}


def process_uploaded_image(file_bytes: bytes) -> bytes:
    """
    Sanitize, validate, strip EXIF metadata, and compress uploaded crop images.
    Returns clean JPEG byte buffer.
    """
    # 1. Check size
    if len(file_bytes) > MAX_SIZE_BYTES:
        raise ValueError("Too large")

    # 2. Check MIME from content
    try:
        mime = magic.from_buffer(file_bytes, mime=True)
    except Exception:
        # Fallback MIME check using PIL header inspection
        try:
            temp_img = Image.open(io.BytesIO(file_bytes))
            mime = Image.MIME.get(temp_img.format, "unknown")
        except Exception:
            raise ValueError("Not allowed: unknown format")

    if mime not in ALLOWED_MIMES:
        raise ValueError(f"Not allowed: {mime}")

    # 3. Open with Pillow and verify integrity
    try:
        img = Image.open(io.BytesIO(file_bytes))
        img.verify()
        # Re-open image after verify() as verify alters image internal state
        img = Image.open(io.BytesIO(file_bytes))
    except Exception as e:
        raise ValueError(f"Corrupt or invalid image data: {str(e)}")

    # 4. Strip EXIF metadata by recreating clean image
    clean = Image.new(img.mode, img.size)
    clean.putdata(list(img.getdata()))

    # Convert RGBA/P mode to RGB before JPEG saving
    if clean.mode in ("RGBA", "P", "LA"):
        clean = clean.convert("RGB")

    # 5. Resize if > 1200px on any dimension
    if clean.width > 1200 or clean.height > 1200:
        clean.thumbnail((1200, 1200), Image.Resampling.LANCZOS)

    # 6. Save as JPEG quality=85, optimize=True
    output = io.BytesIO()
    clean.save(output, format="JPEG", quality=85, optimize=True)
    return output.getvalue()
