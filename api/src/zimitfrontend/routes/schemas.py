from typing import Any

from humps import camelize
from pydantic import BaseModel, ConfigDict


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
    rank: int | None
    offliner_definition_version: str


class TaskCreateRequest(CamelModel):
    url: str
    lang: str
    email: str | None = None
    flags: dict[str, Any]
    unique_id: str | None


class TaskCreateResponse(CamelModel):
    id: str
    new_unique_id: str | None


class TaskCancelRequest(CamelModel):
    unique_id: str | None


class TrackerStatusRequest(CamelModel):
    unique_id: str | None


class TrackerStatusResponse(CamelModel):
    status: str
    ongoing_tasks: list[str] | None


class ZimfarmTaskConfig(BaseModel):
    warehouse_path: str
    offliner: dict[str, Any]


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
    id: str
    status: str
    config: ZimfarmTaskConfig
    files: dict[str, ZimfarmTaskFile] | None = None
    notification: ZimfarmTaskNotification | None = None
    container: ZimfarmTaskContainer | None = None
    # rank is populated only on GET /requested_tasks/{id}, and not on any of
    # other endpoint and not on the webhook calls
    rank: int | None = None
    version: str


class HookStatus(BaseModel):
    status: str


class HookProcessingResult(BaseModel):
    hook_response_status: HookStatus
    mail_target: str | None = None
    mail_subject: str | None = None
    mail_body: str | None = None


class Choice(BaseModel):
    title: str
    value: str


class FlagSchema(BaseModel):
    data_key: str
    key: str
    type: str
    choices: list[Choice] | None = None
    label: str
    description: str
    required: bool = False
    secret: bool = False
    min: int | None = None
    max: int | None = None
    min_length: int | None = None
    max_length: int | None = None
    pattern: str | None = None


class OfflinerDefinitionSchema(BaseModel):
    help: str
    flags: list[FlagSchema]
