from typing import Any, List, Optional
from fastapi import APIRouter, HTTPException, Path, Query, Body, Request, Depends
from ...route_handlers import RequestRecord
from lib.logging import iac_logger
from lib.celery import helpers
from celery import chain
import os

from workflows.upload.minio import upload_file_to_minio
from workflows.validate.file import validate_content_size
from workflows.validate.html import validate_content_html
from ...schemas.router.upload import HtmlUploadRequest, HtmlUploadResponse


file_variable = os.path.dirname(__file__).rsplit(os.sep, 1)[1].upper() + "_" + os.path.basename(__file__).split(".")[0].upper() #UPLOADER_JSON
#To enable verbose logging for health check services set environment variable: LOG_LEVEL_UPLOADER_JSON=10
logger = iac_logger.get_logger(name=file_variable)
#To enable request logging for health check services set environment variable: ENABLE_REQUEST_RECORD_UPLOADER_JSON=10
router = RequestRecord.get_router(name=file_variable)


@router.post("/html", response_model=HtmlUploadResponse)
async def upload_content_html(request: HtmlUploadRequest):
    """
    Upload HTML content to MinIO after validations.
    This endpoint validates the content size and HTML structure before uploading it to MinIO.
    - **filename**: The name of the file to be uploaded.
    - **content**: The HTML content to be uploaded.
    - **bucket**: The name of the MinIO bucket where the file will be stored.
    - **content_type**: The MIME type of the content, defaults to "text/html".
    - **Returns**: A response containing the workflow ID for tracking the upload process.
    
    """
    try:
        workflow = chain(
            validate_content_size.si(filename=request.filename, content=request.content).set(queue='validations'),
            validate_content_html.si(filename=request.filename, content=request.content).set(queue='validations'),
            upload_file_to_minio.si(filename=request.filename, content=request.content, bucket_name=request.bucket, content_type="text/html").set(queue='uploads')
        ).apply_async()
        return HtmlUploadResponse(id=workflow.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start workflow tasks: {str(e)}")
    
@router.get("/task/{id}")
def get_task_status(id: str = Path(..., title="Tracking ID", example="67762a6e-9f6f-49c4-a04e-168422f22711")):
    """
    Get the status of a specific Celery task by its ID.
    - **id**: The ID of the Celery task to check.
    - **Returns**: The result of the Celery task, including its status and any output.
    """
    task_result = helpers.get_celery_task(
        task_id=id, 
        file_variable=file_variable
        )
    return task_result