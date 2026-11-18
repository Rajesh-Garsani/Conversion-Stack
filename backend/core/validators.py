from pathlib import Path
from django.core.exceptions import ValidationError

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
ALLOWED_VIDEO_EXTENSIONS = {".mp4", ".webm"}
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif", "video/mp4", "video/webm"}

def validate_media_file(value):
    if not value:
        return
    extension = Path(value.name).suffix.lower()
    if extension not in ALLOWED_IMAGE_EXTENSIONS | ALLOWED_VIDEO_EXTENSIONS:
        raise ValidationError("Unsupported file type. Use JPG, PNG, WebP, GIF, MP4, or WebM.")
    content_type = getattr(value, "content_type", None)
    if content_type and content_type.lower() not in ALLOWED_CONTENT_TYPES:
        raise ValidationError("The uploaded file content type is not allowed.")
    if value.size > 10 * 1024 * 1024:
        raise ValidationError("Files must be 10 MB or smaller.")

def validate_video_file(value):
    if not value:
        return
    extension = Path(value.name).suffix.lower()
    if extension not in ALLOWED_VIDEO_EXTENSIONS:
        raise ValidationError("Unsupported video type. Use MP4 or WebM.")
    content_type = getattr(value, "content_type", None)
    if content_type and content_type.lower() not in {"video/mp4", "video/webm"}:
        raise ValidationError("The uploaded video content type is not allowed.")
    if value.size > 60 * 1024 * 1024:
        raise ValidationError("Carousel videos must be 60 MB or smaller.")
