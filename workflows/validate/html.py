from workflows.celery_worker import celery_app
from celery.utils.log import get_task_logger
import html5lib
from io import StringIO

logger = get_task_logger(__name__)

@celery_app.task(bind=True, acks_late=True)
def validate_content_html(self, filename: str, content: str) -> bool:
    try:
        html5_parser = html5lib.HTMLParser(strict=True)
        html5_parser.parse(StringIO(content))
    except Exception as e:
        raise Exception(f"HTML validation failed for file {filename}: {str(e)}")
    return True