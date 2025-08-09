from fastapi import Response, Request, APIRouter
from fastapi.routing import APIRoute
from typing import Callable
import time
from datetime import datetime
import logging, os
from lib.logging import iac_logger

file_path = os.path.dirname(__file__)
file_variable = file_path.rsplit(os.sep, 1)[1].upper() + "_" + os.path.basename(__file__).split(".")[0].upper()
logger = iac_logger.get_logger(name=file_variable)


class RequestRecord(APIRoute):

    def get_router(name) -> APIRouter:
        router = None
        request_record_variable = "ENABLE_REQUEST_RECORD_" + name
        if (os.getenv("ENABLE_REQUEST_RECORD") == "True" or os.getenv(request_record_variable) == "True"):
            router = APIRouter(route_class=RequestRecord)
            logger.info(f"Request recording enabled for {name}")
        else:
            router = APIRouter()
            logger.info(f"Request recording disabled for {name}")
        return router


    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            before = time.time()
            logger.debug(msg=f"Waiting for response")
            response: Response = await original_route_handler(request)
            logger.debug(msg=f"Waiting for request body")
            await request.body()
            request_headers = {}
            response_headers = {}
            logger.debug(msg=f"Setting dictionary for request headers")
            for key, value in request.headers._list:
                request_headers[key.decode("UTF-8")] = value.decode("UTF-8")
            logger.debug(msg=f"Setting dictionary for response headers")
            for key, value in response.headers._list:
                response_headers[key.decode("UTF-8")] = value.decode("UTF-8")
            logger.debug(msg=f"Creating log dictionary")
            request_record = {
                "time" : datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3],
                "execution_time_ms" : "{0:.2f}".format((time.time() - before)*1000),
                "response_body" : response.body.decode("UTF-8"),
                "response_headers" : response_headers,
                "response_status" : response.status_code,
                "path" : request.url.path,
                "method" : request.method,
                "request_headers" : request_headers,
                "request_body" : request._json if hasattr(request,"_json") else None,
                "client_host" : request.client.host
            }
            logger.debug(msg=f"{request_record}")
            return response
        return custom_route_handler