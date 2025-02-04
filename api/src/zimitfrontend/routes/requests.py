import urllib.parse
import uuid
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, HTTPException, Path
from schedule import run_pending

from zimitfrontend.blacklist import blacklist_manager
from zimitfrontend.constants import ApiConfiguration, logger
from zimitfrontend.routes.schemas import TaskCreateRequest, TaskCreateResponse, TaskInfo
from zimitfrontend.routes.utils import get_task_info
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
    _, status, task = query_api("GET", f"/tasks/{task_id}?hide_secrets=")
    if status == HTTPStatus.NOT_FOUND:
        # if it fails, try to find the requested task
        _, status, task = query_api("GET", f"/requested-tasks/{task_id}?hide_secrets=")
    if status != HTTPStatus.OK:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail={
                "translationKey": "requestStatus.taskNotFoundSnack",
                "status": status,
                "zimfarmMessage": task,
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
def create_task(request: TaskCreateRequest) -> TaskCreateResponse:

    # trigger blacklist refresh (will only happen at configured interval)
    run_pending()

    url = urllib.parse.urlparse(request.url)

    if blacklist_reason := blacklist_manager.get_blacklist_reason(url.geturl()):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail={"translationKey": blacklist_reason},
        )

    # generate schedule name
    ident = str(uuid.uuid4())[:8]
    schedule_name = f"{url.hostname}_{ident}"

    # build zimit config
    flags = request.flags
    flags["url"] = url.geturl()
    flags["name"] = flags.get("name", schedule_name)
    flags["zim-file"] = flags.get("zim-file", url.hostname) + f"_{ident}.zim"
    flags["userAgentSuffix"] = "zimit.kiwix.org+"

    # remove flags we don't want to overwrite
    for flag in ("adminEmail", "output", "statsFilename"):
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
        size_limit = int(flags.get("sizeLimit", ApiConfiguration.zimit_size_limit))
    except Exception:
        size_limit = ApiConfiguration.zimit_size_limit
    flags["sizeLimit"] = str(_cap_limit(size_limit, ApiConfiguration.zimit_size_limit))
    try:
        time_limit = int(flags.get("timeLimit", ApiConfiguration.zimit_time_limit))
    except Exception:
        time_limit = ApiConfiguration.zimit_time_limit
    flags["timeLimit"] = _cap_limit(time_limit, ApiConfiguration.zimit_time_limit)

    config = {
        "task_name": "zimit",
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
        "flags": flags,
    }

    # create schedule payload
    payload = {  # pyright: ignore[reportUnknownVariableType]
        "name": schedule_name,
        "language": {"code": "eng", "name_en": "English", "name_native": "English"},
        "category": "other",
        "periodicity": "manually",
        "tags": [],
        "enabled": True,
        "config": config,
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
        "/schedules/",
        payload=payload,  # pyright: ignore[reportUnknownArgumentType]
    )
    if not success:
        logger.error(f"Unable to create schedule via HTTP {status}: {resp}")
        # if Zimfarm replied this is a bad request, then this is most probably
        # a bad request due to user input so we can track it like a bad request
        # otherwise, this is most probably an internal problem in our systems
        raise HTTPException(
            status_code=(
                HTTPStatus.BAD_REQUEST
                if status == HTTPStatus.BAD_REQUEST
                else HTTPStatus.INTERNAL_SERVER_ERROR
            ),
            detail={
                "translationKey": "newRequest.unableToCreateSchedule",
                "status": status,
                "zimfarmMessage": resp,
            },
        )

    # request a task for that newly created schedule
    success, status, resp = query_api(
        "POST",
        "/requested-tasks/",
        payload={
            "schedule_names": [schedule_name],
            "worker": ApiConfiguration.task_worker,
        },
    )
    if not success:
        logger.error(f"Unable to request {schedule_name} via HTTP {status}: {resp}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail={
                "translationKey": "newRequest.unableToRequestSchedule",
                "status": status,
                "zimfarmMessage": resp,
            },
        )

    try:
        task_id = resp.get("requested").pop()
        if not task_id:
            logger.error("Zimfarm returned an empty task ID")
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail={
                    "translationKey": "newRequest.missingTaskId",
                },
            )
    except Exception as exc:
        logger.error("Zimfarm did not returned the task ID as expected", exc_info=exc)
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail={
                "translationKey": "newRequest.failToGetTaskId",
            },
        ) from exc

    # remove newly created schedule (not needed anymore)
    success, status, resp = query_api("DELETE", f"/schedules/{schedule_name}")
    if not success:
        logger.error(
            f"Unable to remove schedule {schedule_name} via HTTP {status}: {resp}"
        )

    return TaskCreateResponse(id=task_id)
