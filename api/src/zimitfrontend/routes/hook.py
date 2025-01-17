from typing import Annotated

from fastapi import APIRouter, Query

from zimitfrontend.constants import logger
from zimitfrontend.routes.schemas import HookStatus, ZimfarmTask
from zimitfrontend.routes.utils import SUCCESS, process_zimfarm_hook_call
from zimitfrontend.utils import send_email_via_mailgun

router = APIRouter(
    prefix="/requests/hook",
    tags=["all"],
)


@router.post(
    "",
    status_code=200,
    responses={
        200: {
            "description": "Webhook intended to be called by Zimfarm once task is done",
        },
    },
)
def webhook(
    token: Annotated[str | None, Query()] = None,
    target: Annotated[str | None, Query()] = None,
    lang: Annotated[str, Query()] = "en",
    task: ZimfarmTask | None = None,
) -> HookStatus:

    result = process_zimfarm_hook_call(token, target, lang, task)
    if (
        result.hook_response_status == SUCCESS
        and result.mail_target
        and result.mail_subject
        and result.mail_body
    ):
        try:
            resp = send_email_via_mailgun(
                result.mail_target, result.mail_subject, result.mail_body
            )
            if resp:
                logger.info(f"Mailgun notif sent: {resp}")
        except Exception as exc:
            logger.error(f"Failed to send mailgun notif: {exc}", exc_info=exc)
    return result.hook_response_status
