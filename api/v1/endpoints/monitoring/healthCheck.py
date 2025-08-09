from typing import Any, List, Optional
from ...schemas.router import schemas as routerSchemas
from ...route_handlers import RequestRecord
from lib.logging import iac_logger
import os


file_variable = os.path.dirname(__file__).rsplit(os.sep, 1)[1].upper() + "_" + os.path.basename(__file__).split(".")[0].upper() #MONITORING_HEALTHCHECK
#To enable verbose logging for health check services set environment variable: LOG_LEVEL_MONITORING_HEALTHCHECK=10
logger = iac_logger.get_logger(name=file_variable)
#To enable request logging for health check services set environment variable: ENABLE_REQUEST_RECORD_MONITORING_HEALTHCHECK=10
router = RequestRecord.get_router(name=file_variable)


@router.get("/status", response_model=routerSchemas.Monitoring_HealthCheck)
def get_prometheus_metrics() -> Any:
    """
    This endpoint is used to check the health of the service.
    It returns a simple status message indicating that the service is running.
    """
    status = {
        "status" : "OK"
    }
    logger.debug(msg=f"This is a simple debug msg")
    return status

