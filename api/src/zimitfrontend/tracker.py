import hmac
from enum import Enum
from http import HTTPStatus
from uuid import uuid4

from pydantic import BaseModel

from zimitfrontend.constants import ApiConfiguration, logger
from zimitfrontend.zimfarm import query_api


class ClientInfo(BaseModel):
    # Last known address of the client (will be updated for a given client_id)
    ip_address: str
    # Unique identifier of the client
    unique_id: str
    # List of client tasks known to not yet have completed
    ongoing_tasks: list[str]


class AddTaskStatus(Enum):
    TASK_ADDED = "task_added"
    CAN_ADD_TASK = "can_add_task"
    TOO_MANY_TASKS_FOR_UNIQUE_ID = "too_many_tasks_for_unique_id"
    TOO_MANY_TASKS_FOR_IP_ADDRESS = "too_many_tasks_for_ip_address"
    INVALID_UNIQUE_ID = "invalid_unique_id"


class AddTaskResponse(BaseModel):
    status: AddTaskStatus
    # ongoing_tasks is populated only when status is TOO_MANY_TASKS_FOR_UNIQUE_ID
    # since otherwise this is confidential information
    ongoing_tasks: list[str] | None = None
    # new_unique_id is populated only when status is TASK_ADDED and unique_id was
    # not already set
    new_unique_id: str | None = None


def generate_unique_id() -> str:
    identifier = uuid4().hex
    digest = hmac.new(
        ApiConfiguration.digest_key, identifier.encode(), "sha256"
    ).hexdigest()
    return f"{identifier}|{digest}"


def is_valid_unique_id(unique_id: str) -> bool:
    try:
        identifier, digest = unique_id.split("|", 1)
    except Exception:
        return False
    expected_digest = hmac.new(
        ApiConfiguration.digest_key, identifier.encode(), "sha256"
    ).hexdigest()
    return hmac.compare_digest(digest, expected_digest)


class Tracker:
    def __init__(self):
        self.known_clients: list[ClientInfo] = []
        self.ongoing_task_has_finished = self._ongoing_task_has_finished
        self.has_reached_maximum_tasks = self._has_reached_maximum_tasks

    def _refresh_ongoing_tasks(self, ip_address: str, unique_id: str | None):
        clients_to_refresh = filter(
            lambda client: client.ip_address == ip_address
            or (unique_id and client.unique_id == unique_id),
            self.known_clients,
        )
        completed_clients: list[ClientInfo] = []
        for client in clients_to_refresh:
            completed_tasks: list[str] = []
            for task in client.ongoing_tasks:
                if self.ongoing_task_has_finished(task):
                    completed_tasks.append(task)
            for task in completed_tasks:
                client.ongoing_tasks.remove(task)
                if len(client.ongoing_tasks) == 0:
                    completed_clients.append(client)
        for client in completed_clients:
            self.known_clients.remove(client)

    def _has_reached_maximum_tasks(self, client_info: ClientInfo) -> bool:
        return len(client_info.ongoing_tasks) > 0

    def _ongoing_task_has_finished(self, task_id: str) -> bool:
        # first try to find the requested task
        success, status, task = query_api("GET", f"/requested-tasks/{task_id}")
        if status == HTTPStatus.NOT_FOUND:
            # if it fails, try to find the task
            success, status, task = query_api("GET", f"/tasks/{task_id}")
        if not success:
            logger.warning(
                f"Unable to find ongoing task {task_id} status via HTTP {status}: "
                f"{task}"
            )
            # failsafe to `True` to clean the situation, might be that we manually
            # cancelled the requested task which is then simply deleted from DB
            return True
        return task["status"] not in [
            "requested",
            "cancel_requested",
            "reserved",
            "scraper_running",
            "scraper_started",
            "started",
        ]

    def add_task(
        self, ip_address: str, unique_id: str | None, task_id: str | None
    ) -> AddTaskResponse:

        if unique_id and not is_valid_unique_id(unique_id):
            return AddTaskResponse(
                status=AddTaskStatus.INVALID_UNIQUE_ID,
            )

        self._refresh_ongoing_tasks(ip_address, unique_id)

        if unique_id:
            if clients_info_by_unique_id := [
                client for client in self.known_clients if client.unique_id == unique_id
            ]:
                if len(clients_info_by_unique_id) > 1:
                    raise Exception(
                        f"Too many data for one single unique id: {unique_id}"
                    )
                client_info = clients_info_by_unique_id[0]
                if self.has_reached_maximum_tasks(client_info):
                    return AddTaskResponse(
                        status=AddTaskStatus.TOO_MANY_TASKS_FOR_UNIQUE_ID,
                        ongoing_tasks=client_info.ongoing_tasks,
                    )
        elif clients_info_by_ip_address := [
            client for client in self.known_clients if client.ip_address == ip_address
        ]:
            if len(clients_info_by_ip_address) > 1:
                raise Exception(
                    f"Too many data for one single ip address: {ip_address}"
                )
            return AddTaskResponse(
                status=AddTaskStatus.TOO_MANY_TASKS_FOR_IP_ADDRESS,
                ongoing_tasks=None,  # Confidential information
            )

        # when we've reached this point, there is no ongoing task pending for this
        # client

        if not task_id:
            # simply inform that we are ok to add task
            return AddTaskResponse(
                status=AddTaskStatus.CAN_ADD_TASK,
                ongoing_tasks=None,
            )

        if not unique_id:
            new_unique_id = generate_unique_id()  # generate a new unique ID
            self.known_clients.append(
                ClientInfo(
                    ip_address=ip_address,
                    unique_id=new_unique_id,
                    ongoing_tasks=[task_id],
                )
            )
            return AddTaskResponse(
                status=AddTaskStatus.TASK_ADDED,
                ongoing_tasks=None,
                new_unique_id=new_unique_id,
            )

        if clients_info_by_unique_id := [
            client for client in self.known_clients if client.unique_id == unique_id
        ]:
            client_info = clients_info_by_unique_id[0]
            client_info.ongoing_tasks.append(task_id)
        else:
            self.known_clients.append(
                ClientInfo(
                    ip_address=ip_address, unique_id=unique_id, ongoing_tasks=[task_id]
                )
            )

        return AddTaskResponse(
            status=AddTaskStatus.TASK_ADDED,
            ongoing_tasks=None,
            new_unique_id=None,
        )


tracker = Tracker()
