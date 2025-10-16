import urllib.parse
import uuid
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Request

from zimitfrontend.constants import ApiConfiguration, blacklist, logger
from zimitfrontend.routes.schemas import (
    TaskCancelRequest,
    TaskCreateRequest,
    TaskCreateResponse,
    TaskInfo,
)
from zimitfrontend.routes.utils import get_task_info
from zimitfrontend.tracker import AddTaskStatus, tracker
from zimitfrontend.utils import normalize_hostname
from zimitfrontend.zimfarm import query_api

router = APIRouter(
    prefix="/requests",
    tags=["all"],
)


@router.get(
    "/{task_id}",
    status_code=HTTPStatus.OK,
    responses={
        HTTPStatus.OK: {
            "description": "Returns the details about a given task",
        },
    },
)
def task_info(
    task_id: Annotated[str, Path()],
) -> TaskInfo:
    # first try to find the task
    _, status, task = query_api("GET", f"/tasks/{task_id}")
    if status == HTTPStatus.NOT_FOUND:
        # if it fails, try to find the requested task
        _, status, task = query_api("GET", f"/requested-tasks/{task_id}")
    if status != HTTPStatus.OK:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail={
                "error": f"Failed to find task on Zimfarm with HTTP {status}",
                "zimfarm_message": task,
            },
        )
    return get_task_info(task)


@router.post(
    "",
    status_code=HTTPStatus.CREATED,
    responses={
        HTTPStatus.CREATED: {
            "description": "Requests a Zimit task on the Zimfarm.",
        },
    },
)
def create_task(
    request: TaskCreateRequest, http_request: Request
) -> TaskCreateResponse:
    if not http_request.client:
        raise HTTPException(
            HTTPStatus.INTERNAL_SERVER_ERROR, detail="http_request.client is missing"
        )

    # check that client can start a task
    add_task = tracker.add_task(
        http_request.client.host,
        request.unique_id,
        None,
    )
    if add_task.status != AddTaskStatus.CAN_ADD_TASK:
        raise HTTPException(
            status_code=HTTPStatus.TOO_MANY_REQUESTS,
            detail={
                "message": "Too many requests already ongoing for your user",
                "reason": add_task.status.value,
                "ongoing_tasks": add_task.ongoing_tasks,
            },
        )

    url = urllib.parse.urlparse(request.url)

    matching_blacklist_entries = [
        blacklist_entry
        for blacklist_entry in blacklist
        if blacklist_entry["host"].lower() in url.geturl().lower()
    ]
    matching_blacklist_entry = (
        matching_blacklist_entries[0] if matching_blacklist_entries else None
    )
    if matching_blacklist_entry:
        raise HTTPException(
            HTTPStatus.BAD_REQUEST,
            detail={"error": "blacklisted", "blacklist": matching_blacklist_entry},
        )

    # generate schedule name
    ident = str(uuid.uuid4())[:8]
    schedule_name = f"{url.hostname}_{ident}"

    # build zimit config
    flags = request.flags
    flags["seeds"] = normalize_hostname(request.url)
    flags["name"] = flags.get("name", schedule_name)
    flags["zim-file"] = flags.get("zim-file", url.hostname) + f"_{ident}.zim"
    flags["userAgentSuffix"] = "zimit.kiwix.org+"
    flags["failOnFailedSeed"] = True
    flags["failOnInvalidStatus"] = True
    flags["content-header-bytes-length"] = 2048

    # remove flags we don't want to overwrite
    for flag in ("adminEmail", "output", "zimit-progress-file"):
        if flag in flags:
            del flags[flag]

    # make sure we cap requests to ZIMIT_LIMIT at most
    def _cap_limit(user_limit: int, zimit_limit: int) -> int:
        if user_limit <= 0:  # case where someone is trying to trick the limit
            return zimit_limit
        if user_limit < zimit_limit:
            return user_limit
        return zimit_limit  # case where someone is trying to trick as well

    try:
        size_limit = int(flags.get("sizeSoftLimit", ApiConfiguration.zimit_size_limit))
    except Exception:
        size_limit = ApiConfiguration.zimit_size_limit
    flags["sizeSoftLimit"] = str(
        _cap_limit(size_limit, ApiConfiguration.zimit_size_limit)
    )
    try:
        time_limit = int(flags.get("timeSoftLimit", ApiConfiguration.zimit_time_limit))
    except Exception:
        time_limit = ApiConfiguration.zimit_time_limit
    flags["timeSoftLimit"] = _cap_limit(time_limit, ApiConfiguration.zimit_time_limit)

    config = {
        "warehouse_path": "/other",
        "image": {
            "name": ApiConfiguration.zimit_image.split(":")[0],
            "tag": ApiConfiguration.zimit_image.split(":")[1],
        },
        "resources": {
            "cpu": ApiConfiguration.task_cpu,
            "memory": ApiConfiguration.task_memory,
            "disk": ApiConfiguration.task_disk,
            "shm": ApiConfiguration.task_memory,
            "cap_add": ["SYS_ADMIN", "NET_ADMIN"],
        },
        "platform": None,
        "monitor": False,
        "offliner": {"offliner_id": "zimit", **flags},
    }

    # create schedule payload
    payload = {  # pyright: ignore[reportUnknownVariableType]
        "name": schedule_name,
        "language": "eng",
        "category": "other",
        "periodicity": "manually",
        "tags": [],
        "enabled": True,
        "config": config,
        "version": ApiConfiguration.zimit_definition_version,
    }

    # add notification callback if email supplied
    if request.email:
        webhook_url = (
            f"{ApiConfiguration.callback_base_url}?"
            f"token={ApiConfiguration.hook_token}"
            f"&target={request.email}"
            f"&lang={request.lang}"
        )
        payload.update(  # pyright: ignore[reportUnknownMemberType]
            {
                "notification": {
                    "requested": {"webhook": [webhook_url]},
                    "ended": {"webhook": [webhook_url]},
                }
            }
        )

    # create a unique schedule for that request on the zimfarm
    success, status, resp = query_api(
        "POST",
        "/schedules",
        payload=payload,  # pyright: ignore[reportUnknownArgumentType]
    )
    if not success:
        logger.error(f"Unable to create schedule via HTTP {status}: {resp}")
        message = f"Unable to create schedule via HTTP {status}: {resp}"
        if status in [HTTPStatus.BAD_REQUEST, HTTPStatus.UNPROCESSABLE_ENTITY]:
            # if Zimfarm replied this is a bad request, then this is most probably
            # a bad request due to user input so we can track it like a bad request
            raise HTTPException(status_code=status, detail=message)
        else:
            # otherwise, this is most probably an internal problem in our systems
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=message
            )

    # request a task for that newly created schedule
    success, status, resp = query_api(
        "POST",
        "/requested-tasks",
        payload={
            "schedule_names": [schedule_name],
            "worker": ApiConfiguration.task_worker,
        },
    )
    if not success:
        logger.error(f"Unable to request {schedule_name} via HTTP {status}: {resp}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Unable to request schedule via HTTP {status}): {resp}",
        )

    try:
        task_id = resp.get("requested").pop()
        if not task_id:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="task_id is False"
            )
    except Exception as exc:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Couldn't retrieve requested task id: {exc}",
        ) from exc

    # remove newly created schedule (not needed anymore)
    success, status, resp = query_api("DELETE", f"/schedules/{schedule_name}")
    if not success:
        logger.error(
            f"Unable to remove schedule {schedule_name} via HTTP {status}: {resp}"
        )

    add_task = tracker.add_task(
        http_request.client.host,
        request.unique_id,
        task_id,
    )
    if add_task.status != AddTaskStatus.TASK_ADDED:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Failed to store task in tracker: {add_task.status }",
        )

    return TaskCreateResponse(id=task_id, new_unique_id=add_task.new_unique_id)


@router.post(
    "/{task_id}/cancel",
    responses={
        HTTPStatus.OK: {
            "description": "Task cancelled succesfully",
        },
    },
)
def cancel_task(
    task_id: Annotated[str, Path()],
    task_cancel_request: TaskCancelRequest,
    http_request: Request,
) -> None:
    if not http_request.client:
        raise HTTPException(
            HTTPStatus.INTERNAL_SERVER_ERROR, detail="http_request.client is missing"
        )

    status = tracker.add_task(
        http_request.client.host,
        task_cancel_request.unique_id,
        None,
    )
    if not status.ongoing_tasks or task_id not in status.ongoing_tasks:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=f"task_id {task_id} is not associated with you",
        )

    # search as requested task
    _, status, task = query_api("GET", f"/requested-tasks/{task_id}")
    if status == HTTPStatus.OK:
        _, status, task = query_api("DELETE", f"/requested-tasks/{task_id}")
        if status != HTTPStatus.OK:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail={
                    "error": "Failed to delete requested task on Zimfarm with HTTP "
                    "{status}",
                    "zimfarm_message": task,
                },
            )
        return
    elif status != HTTPStatus.NOT_FOUND:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail={
                "error": "Failed to search for requested task on Zimfarm with HTTP "
                "{status}",
                "zimfarm_message": task,
            },
        )

    # search as running task
    _, status, task = query_api("GET", f"/tasks/{task_id}")
    if status == HTTPStatus.OK:
        if task["status"] not in [
            "reserved",
            "scraper_running",
            "scraper_started",
            "started",
        ]:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail={
                    "error": f"Cannot cancel task in '{task['status']}' status",
                },
            )
        _, status, task = query_api("POST", f"/tasks/{task_id}/cancel")
        if status != HTTPStatus.NO_CONTENT:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail={
                    "error": f"Failed to delete task on Zimfarm with HTTP {status}",
                    "zimfarm_message": task,
                },
            )
        return
    else:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail={
                "error": f"Failed to search for task on Zimfarm with HTTP {status}",
                "zimfarm_message": task,
            },
        )
