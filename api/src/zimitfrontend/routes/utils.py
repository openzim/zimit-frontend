from typing import Any

from zimitfrontend.constants import ApiConfiguration, logger
from zimitfrontend.i18n import change_locale
from zimitfrontend.routes.schemas import (
    HookProcessingResult,
    HookStatus,
    TaskInfo,
    TaskInfoFlag,
    ZimfarmTask,
)
from zimitfrontend.utils import jinja_env

FAILED = HookStatus(status="failed")
SUCCESS = HookStatus(status="success")


def get_task_info(task: Any) -> TaskInfo:
    """Transforms a task object(dict) returned by Zimfarm API

    The final object is ready to be consumed by the frontend, with most checks for
    consistency and complex computation already done.
    """

    # parse object (dict) as pydantic object
    zimfarm_task = ZimfarmTask.model_validate(task)

    # compute download link for the ZIM
    if zimfarm_task.files is None:
        download_link = None
    else:
        # should we have multiple files, we select the first one (by creation date) as
        # download link
        files = [
            {"name": key, "created_timestamp": value.created_timestamp}
            for key, value in zimfarm_task.files.items()
        ]
        download_link = (
            None
            if len(files) == 0
            else ApiConfiguration.zim_download_url
            + zimfarm_task.config.warehouse_path
            + "/"
            + sorted(files, key=lambda file: file["created_timestamp"])[0]["name"]
        )

    # transform into object ready to be returned by the BFF
    return TaskInfo(
        id=zimfarm_task.id,
        download_link=download_link,
        has_email=bool(
            zimfarm_task.notification
            and zimfarm_task.notification.ended
            and zimfarm_task.notification.ended.webhook
        ),
        partial_zim=bool(
            zimfarm_task.container
            and zimfarm_task.container.progress
            and zimfarm_task.container.progress.partial_zim
        ),
        status=zimfarm_task.status,
        flags=(
            sorted(
                [
                    TaskInfoFlag(name=key, value=value)
                    for (key, value) in zimfarm_task.config.flags.items()
                ],
                key=lambda flag: flag.name,
            )
        ),
        progress=(
            int(zimfarm_task.container.progress.overall)
            if (
                zimfarm_task.container
                and zimfarm_task.container.progress
                and zimfarm_task.container.progress.overall
            )
            else 0
        ),
        rank=zimfarm_task.rank,
    )


def process_zimfarm_hook_call(
    token: str | None, target: str | None, lang: str, task: ZimfarmTask | None
) -> HookProcessingResult:
    """Transforms message received from Zimfarm via hook to mail info

    Returned object is ready to be sent (or contains information that failure occured)
    """

    # we require a `token` arg equal to a setting string so we can ensure
    # hook requests are from know senders.
    # otherwises exposes us to spam abuse
    if token != ApiConfiguration.hook_token:
        logger.error(f"Incorrect token value received in POST /hook: {token}")
        return HookProcessingResult(hook_response_status=FAILED)

    # without a `target` arg, we have nowhere to send the notification to
    if not target:
        logger.error(f"Incorrect target received in POST /hook: {target}")
        return HookProcessingResult(hook_response_status=FAILED)

    if not task:
        logger.error("No task received in POST /hook body")
        return HookProcessingResult(hook_response_status=FAILED)

    # discard hooks registered for events we don't plan on sending email for
    # hook_response_status is still SUCCESS because hook call is valid
    if task.status not in ("requested", "succeeded", "failed", "canceled"):
        return HookProcessingResult(hook_response_status=SUCCESS)

    # force task fail status, see https://github.com/openzim/zimit-frontend/issues/90
    if task.status != "requested" and (task.files is None or len(task.files) == 0):
        task.status = "failed"

    context = {
        "base_url": ApiConfiguration.public_url,
        "download_url": ApiConfiguration.zim_download_url,
        "size_limit": ApiConfiguration.zimit_size_limit,
        "time_limit": ApiConfiguration.zimit_time_limit,
        "contact_us_url": ApiConfiguration.contact_us_url,
        "task": task.model_dump(),
        "rtl": lang in ApiConfiguration.rtl_language_codes,
        "lang": lang,
    }

    logger.info(f"Translating to {lang}")
    change_locale(lang)
    subject = (
        jinja_env.get_template("email_subject.txt").render(**context).replace("\n", "")
    )
    body = jinja_env.get_template("email_body.html").render(**context)
    return HookProcessingResult(
        hook_response_status=SUCCESS,
        mail_target=target,
        mail_subject=subject,
        mail_body=body,
    )
