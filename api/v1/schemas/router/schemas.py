from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Monitoring_HealthCheck(BaseModel):
    status: str = Field(..., description="Health check for api")

class Monitoring_Message_Response(BaseModel):
    message: str = Field(..., description="Just a simple message")

class Monitoring_Message_Request(BaseModel):
    reqbody: str = Field(..., description="Health check for db", example="sample req body")
    cnsn: str = Field(..., description="Health check for ceph", example="cnsnSampleData" )
    deneme: str = Field(..., description="Health check for ceph", example="haydaaa")
    