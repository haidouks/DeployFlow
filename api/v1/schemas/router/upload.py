from pydantic import BaseModel, Field
from typing import List, Optional, Any
from datetime import datetime

class HtmlUploadRequest(BaseModel):
    filename: str = Field(..., example="data.html", description="Name of the file to be uploaded")
    content: str = Field(...,  example="<!DOCTYPE html><html></html>", description="Content of the HTML file to be uploaded")
    bucket: Optional[str] = Field(default="source-bucket", example="source-bucket", description="Optional bucket name for storage")

class HtmlUploadResponse(BaseModel):
    id: str = Field(..., example="93195e60-9566-4a67-bd65-d4ec2b5bedbf", description="Tracking ID for the upload task")
