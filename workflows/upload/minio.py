from workflows.celery_worker import celery_app
from celery.utils.log import get_task_logger
import os
import io
from minio import Minio

logger = get_task_logger(__name__)

@celery_app.task(bind=True, acks_late=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 5, 'countdown': 10})
def upload_file_to_minio(self, filename: str, content: dict, bucket_name: str, content_type: str = "application/json") -> bool:
    minio_client = Minio(
        endpoint=os.getenv("MINIO_ENDPOINT", "minio:9000"),
        access_key=os.getenv("MINIO_ACCESS_KEY", "minioadmin"),
        secret_key=os.getenv("MINIO_SECRET_KEY", "minioadmin"),
        secure=False,
    )
    if not minio_client.bucket_exists(bucket_name):
        logger.info(msg=f"Bucket {bucket_name} does not exist, creating it.")
        minio_client.make_bucket(bucket_name)
    data = content.encode("utf-8")
    minio_client.put_object(
        bucket_name,
        filename,
        data=io.BytesIO(data),
        length=len(data),
        content_type=content_type
    )
    logger.debug(msg=f"You can download object: {minio_client.presigned_get_object(bucket_name, filename)}")
    return True