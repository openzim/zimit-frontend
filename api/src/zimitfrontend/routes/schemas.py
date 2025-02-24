from typing import Any

from humps import camelize
from pydantic import BaseModel, ConfigDict, Field


class CamelModel(BaseModel):
    """Model which transforms Python snake_case into JSON camelCase (two-way)"""

    model_config = ConfigDict(alias_generator=camelize, populate_by_name=True)


class TaskInfoFlag(BaseModel):
    name: str
    value: Any


class TaskInfo(CamelModel):
    id: str
    download_link: str | None
    has_email: bool
    partial_zim: bool
    status: str
    flags: list[TaskInfoFlag]
    progress: int | None
    rank: int


class TaskCreateRequest(CamelModel):
    url: str
    lang: str
    email: str | None = None
    flags: dict[str, Any]


class TaskCreateResponse(CamelModel):
    id: str


class ZimfarmTaskConfig(BaseModel):
    warehouse_path: str
    flags: dict[str, Any]


class ZimfarmTaskFile(BaseModel):
    created_timestamp: str
    size: int
    name: str


class ZimfarmTaskNotificationConfig(BaseModel):
    webhook: list[str] | None = None


class ZimfarmTaskNotification(BaseModel):
    ended: ZimfarmTaskNotificationConfig | None = None


class ZimfarmTaskContainerProgress(CamelModel):
    partial_zim: bool | None = None
    overall: int | None = None


class ZimfarmTaskContainer(BaseModel):
    progress: ZimfarmTaskContainerProgress | None = None


class ZimfarmTask(BaseModel):
    id: str = Field(alias="_id")
    status: str
    config: ZimfarmTaskConfig
    files: dict[str, ZimfarmTaskFile] | None = None
    notification: ZimfarmTaskNotification | None = None
    container: ZimfarmTaskContainer | None = None
    rank: int


class HookStatus(BaseModel):
    status: str


class HookProcessingResult(BaseModel):
    hook_response_status: HookStatus
    mail_target: str | None = None
    mail_subject: str | None = None
    mail_body: str | None = None
