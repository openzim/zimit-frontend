from typing import Annotated

from fastapi import APIRouter, Query

from zimitfrontend.constants import logger
from zimitfrontend.routes.schemas import HookStatus, ZimfarmTask
from zimitfrontend.routes.utils import SUCCESS, convert_hook_to_mail
from zimitfrontend.utils import send_email_via_mailgun

router = APIRouter(
    prefix="/hook",
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

    result = convert_hook_to_mail(token, target, lang, task)
    if result.status == SUCCESS and result.target and result.subject and result.body:
        try:
            resp = send_email_via_mailgun(result.target, result.subject, result.body)
            if resp:
                logger.info(f"Mailgun notif sent: {resp}")
        except Exception as exc:
            logger.error(f"Failed to send mailgun notif: {exc}", exc_info=exc)
    return result.status
