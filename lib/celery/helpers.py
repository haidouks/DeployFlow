from celery.result import AsyncResult
import json
from celery import states
import os
from lib.logging import iac_logger
import requests

file_variable = os.path.dirname(__file__).rsplit(os.sep, 1)[1].upper() + "_" + os.path.basename(__file__).split(".")[0].upper()

def get_celery_task(task_id: str, file_variable: str = file_variable):
    logger = iac_logger.get_logger(name=file_variable)
    try:
        logger.debug(f"Getting task result for {task_id} from Celery")
        task_result = AsyncResult(task_id)
        status, retval = task_result.state, task_result.result
        end_date = task_result.date_done

        # Ensure retval is a dictionary or None
        #if not isinstance(retval, (dict, type(None))):
        #    logger.warning(f"Unexpected result type for task {task_id}: {type(retval)}")
        #    retval = None

        data = {
            'task_id': task_id, 
            'status': status, 
            'result': retval,
            'request_end_date': end_date,
            "error_summary": ""
            }
        logger.debug(f"Created data for {task_id}: {data}")
        if status in states.EXCEPTION_STATES:
            logger.debug(f"Task {task_id} has an exceptional state: {status}")
            data["error_summary"] = task_result.traceback
        logger.debug(f"Returning data for {task_id}: {data}")
        return data
    except BaseException as e:
        logger.error(msg=f"Exception:{e}", exc_info=True)
        return {
            'task_id': task_id,
            'status': 'FAILURE',
            'result': None,
            'request_end_date': None,
            "error_summary": str(e)
        }

def get_celery_task_from_flower(task_id: str, file_variable: str = file_variable):
    logger = iac_logger.get_logger(name=file_variable)
    url = f"{os.getenv('FLOWER_URL')}/api/task/info/{task_id}"
    logger.debug(msg=f"Getting task details from {url}")
    headers = {
        "Content-Type": "application/json"
    }
    response_flower = requests.get(
        url=url,
        verify=False,
        headers=headers
    )
    logger.debug(msg=f"Received response for {task_id}: {response_flower}")
    if response_flower.ok:
        return response_flower.json() 
    elif response_flower.status_code == 404:
        return None
    else:
       logger.warning(msg=f"{task_id} - Status code is not healthy: {response_flower.status_code}")
       http_exception = response_flower.json() if response_flower.status_code else f"Unable to reach {url}"
       raise Exception(http_exception)

def reset_celery_task(task_id: str, file_variable: str = file_variable):
    """
    Resets  a Celery task based on the action provided.
    :param task_id: The ID of the task to reset.
    :param file_variable: Logger name, defaults to the module's file_variable.
    """
    logger = iac_logger.get_logger(name=file_variable)
    try:
        logger.debug(f"Performing reset action on task {task_id}")
        task_result = AsyncResult(task_id)
        task_result.forget()
        logger.info(f"Task {task_id} state and result have been reset.")

    except BaseException as e:
        logger.error(msg=f"Failed to perform reset on task {task_id}. Exception: {e}", exc_info=True)

def revoke_celery_task(task_id: str, file_variable: str = file_variable):
    """
    Revokes a Celery task based on the action provided.
    
    :param task_id: The ID of the task to revoke.
    :param file_variable: Logger name, defaults to the module's file_variable.
    """
    logger = iac_logger.get_logger(name=file_variable)
    try:
        logger.debug(f"Performing revoke action on task {task_id}")
        task_result = AsyncResult(task_id)
        task_result.revoke(terminate=True)
        logger.info(f"Task {task_id} has been revoked and terminated.")
    except BaseException as e:
        logger.error(msg=f"Failed to perform revoke on task {task_id}. Exception: {e}", exc_info=True)
