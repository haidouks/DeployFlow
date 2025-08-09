from workflows.celery_worker import celery_app
from celery.utils.log import get_task_logger
import os

logger = get_task_logger(__name__)
max_content_size = int(os.getenv("MAX_CONTENT_SIZE", 1024 * 1024))  # 1 MB

@celery_app.task(bind=True, acks_late=True)
def validate_content_size(self, filename: str, content: str) -> bool:
    try:
        content_bytes = content.encode("utf-8")
    except Exception as e:
        raise Exception(f"Unable to encode {filename} content: {str(e)}")
    if len(content_bytes) > max_content_size:
        raise Exception(f"Content for {filename} exceeds max size ({max_content_size} bytes).")
    return True