import pytest

from zimitfrontend.constants import ApiConfiguration
from zimitfrontend.tracker import (
    AddTaskStatus,
    ClientInfo,
    Tracker,
    generate_unique_id,
    is_valid_unique_id,
)

CLIENT_1_IP = "172.16.1.1"
CLIENT_1_ID = (
    "cf068243341e4e979c35fd4fb82cea5d|"
    "7abc6ca76820e0d693d8a22ef0bf002f2f25e5c9f937a84998572c67e097e301"
)

CLIENT_2_IP = "172.16.1.2"
CLIENT_2_INVALID_ID = "id1"  # this is not a valid ID
CLIENT_2_VALID_ID = (
    "c047287b89854bf9b64aa7a1caf359f8|"
    "8b6dbcad94abf2e872d5a066575241127eee3636bd9d7f25f8b68bb22e34c4d1"
)  # this is a valid ID

CLIENT_3_IP = "172.16.1.3"
CLIENT_3_ID = (
    "751e636176714d45add32deea6f8931c|"
    "90ced10358a341684e7fb2fb46ce52702e9ac32ed497b20c05c9db913e025ad0"
)

CLIENT_4_IP = "172.16.1.4"
CLIENT_4_ID1 = (
    "989536ffae664d0d9df62701424bedfc|"
    "cf6134ae38f74ab595880c1e9c1442df2a24edc2e24c045cde884c8ed72a0ea8"
)
CLIENT_4_ID2 = (
    "d7c3ff46bc314ecfbc7268b452f24a32|"
    "d0a21077e88fd58ccaa40a489b9221f2af4468273525e7736677f5f903ab0cef"
)

CLIENT_5_IP1 = "172.16.1.5"
CLIENT_5_IP2 = "172.16.1.6"
CLIENT_5_ID = (
    "634ecae47311413c9fd90725e08593e1|"
    "c31f98c5bd633785b77b2706a6eee35037bcc1356c75cddbe6478e6afe0f8023"
)

TASK_ID1 = "task_id1"
TASK_ID2 = "task_id2"
TASK_ID3 = "task_id3"
TASK_ID4 = "task_id4"
TASK_ID5 = "task_id5"
TASK_ID6 = "task_id6"
TASK_ID7 = "task_id7"
TASK_ID8 = "task_id8"


@pytest.fixture()
def tracker() -> Tracker:
    tracker = Tracker()
    # known digest key for tests
    ApiConfiguration.digest_key = bytes.fromhex("723a207d91341918")
    # test initial status
    tracker.known_clients = [
        ClientInfo(
            ip_address=CLIENT_1_IP,
            unique_id=CLIENT_1_ID,
            ongoing_tasks=[TASK_ID4, TASK_ID1],
        ),
        ClientInfo(
            ip_address=CLIENT_3_IP, unique_id=CLIENT_3_ID, ongoing_tasks=[TASK_ID2]
        ),
        ClientInfo(
            ip_address=CLIENT_4_IP, unique_id=CLIENT_4_ID1, ongoing_tasks=[TASK_ID5]
        ),
        ClientInfo(  # two unique IDs for one IP, this is a bug
            ip_address=CLIENT_4_IP, unique_id=CLIENT_4_ID2, ongoing_tasks=[TASK_ID6]
        ),
        ClientInfo(
            ip_address=CLIENT_5_IP1, unique_id=CLIENT_5_ID, ongoing_tasks=[TASK_ID7]
        ),
        ClientInfo(  # two client IPs for one unique ID, this is a bug
            ip_address=CLIENT_5_IP1, unique_id=CLIENT_5_ID, ongoing_tasks=[TASK_ID8]
        ),
    ]

    # test logic to get which ongoing task has already finished
    def custom_ongoing_task_has_finished(task_id: str):
        return task_id in [
            TASK_ID1,
            TASK_ID4,
        ]

    tracker.ongoing_task_has_finished = custom_ongoing_task_has_finished
    return tracker


@pytest.mark.parametrize(
    "ip_address, unique_id, task_id, expected_status, expected_ongoing_tasks,"
    " new_unique_id_is_set",
    [
        pytest.param(
            CLIENT_1_IP,
            CLIENT_1_ID,
            None,
            AddTaskStatus.CAN_ADD_TASK,
            None,
            False,
            id="client_1_uniqueid_notask",
        ),
        pytest.param(
            CLIENT_1_IP,
            None,
            None,
            AddTaskStatus.CAN_ADD_TASK,
            None,
            False,
            id="client_1_nouniqueid_notask",
        ),
        pytest.param(
            CLIENT_2_IP,
            CLIENT_2_INVALID_ID,
            None,
            AddTaskStatus.INVALID_UNIQUE_ID,
            None,
            False,
            id="client_2_invalidid_notask",
        ),
        pytest.param(
            CLIENT_2_IP,
            CLIENT_2_VALID_ID,
            None,
            AddTaskStatus.CAN_ADD_TASK,
            None,
            False,
            id="client_2_validid_notask",
        ),
        pytest.param(
            CLIENT_2_IP,
            None,
            None,
            AddTaskStatus.CAN_ADD_TASK,
            None,
            False,
            id="client_2_nouniqueid_notask",
        ),
        pytest.param(
            CLIENT_3_IP,
            CLIENT_3_ID,
            None,
            AddTaskStatus.TOO_MANY_TASKS_FOR_UNIQUE_ID,
            [TASK_ID2],
            False,
            id="client_3_uniqueid_notask",
        ),
        pytest.param(
            CLIENT_3_IP,
            None,
            None,
            AddTaskStatus.TOO_MANY_TASKS_FOR_IP_ADDRESS,
            None,
            False,
            id="client_3_nouniqueid_notask",
        ),
        pytest.param(
            CLIENT_1_IP,
            CLIENT_1_ID,
            TASK_ID3,
            AddTaskStatus.TASK_ADDED,
            None,
            False,
            id="client_1_uniqueid_task",
        ),
        pytest.param(
            CLIENT_1_IP,
            None,
            TASK_ID3,
            AddTaskStatus.TASK_ADDED,
            None,
            True,
            id="client_1_nouniqueid_task",
        ),
        pytest.param(
            CLIENT_2_IP,
            CLIENT_2_VALID_ID,
            TASK_ID3,
            AddTaskStatus.TASK_ADDED,
            None,
            False,
            id="client_2_validid_task",
        ),
        pytest.param(
            CLIENT_2_IP,
            None,
            TASK_ID3,
            AddTaskStatus.TASK_ADDED,
            None,
            True,
            id="client_2_nouniqueid_task",
        ),
    ],
)
def test_add_task(
    tracker: Tracker,
    ip_address: str,
    unique_id: str,
    task_id: str,
    expected_status: AddTaskStatus,
    expected_ongoing_tasks: list[str] | None,
    *,
    new_unique_id_is_set: bool,
):
    result = tracker.add_task(ip_address, unique_id, task_id)
    assert result.status == expected_status
    assert result.ongoing_tasks == expected_ongoing_tasks
    assert (not new_unique_id_is_set) or (
        result.new_unique_id and len(result.new_unique_id) > 0
    )


def test_duplicate_ip(tracker: Tracker):
    with pytest.raises(Exception, match="Too many data for one single ip address"):
        tracker.add_task(CLIENT_5_IP1, None, None)


def test_duplicate_unique_id(tracker: Tracker):
    with pytest.raises(Exception, match="Too many data for one single unique id"):
        tracker.add_task(CLIENT_5_IP1, CLIENT_5_ID, None)


def test_custom_max_tasks(tracker: Tracker):
    result = tracker.add_task(CLIENT_3_IP, CLIENT_3_ID, None)
    assert result.status == AddTaskStatus.TOO_MANY_TASKS_FOR_UNIQUE_ID
    assert result.ongoing_tasks == [TASK_ID2]
    assert result.new_unique_id is None

    def fake_has_reached_maximum_tasks(client_info: ClientInfo) -> bool:
        return len(client_info.ongoing_tasks) > 1  # allow up to two tasks

    tracker.has_reached_maximum_tasks = fake_has_reached_maximum_tasks

    result = tracker.add_task(CLIENT_3_IP, CLIENT_3_ID, TASK_ID8)
    assert result.status == AddTaskStatus.TASK_ADDED
    assert result.ongoing_tasks is None
    assert result.new_unique_id is None


def test_generate_validate_id():
    assert is_valid_unique_id(generate_unique_id())


@pytest.mark.parametrize("prefix, suffix", [("", "a"), ("a", ""), ("a|", "")])
def test_validate_bad_id(prefix: str, suffix: str):
    assert not is_valid_unique_id(prefix + generate_unique_id() + suffix)


@pytest.mark.parametrize(
    "identifier, is_valid",
    [
        (
            "6e794ce5c6ab4fb18fec35e4845913ec|094055182b0fa885947ed61ae81268a1e09d6071561b3f7417035863f0515559",
            True,
        ),
        (
            "6e794ce5c6ab4fb18fec35e4845913eb|094055182b0fa885947ed61ae81268a1e09d6071561b3f7417035863f0515559",
            False,
        ),
        (
            "6e794ce5c6ab4fb18fec35e4845913ec|094055182b0fa885947ed61ae81268a1e09d6071561b3f7417035863f0515558",
            False,
        ),
        (
            "6e794ce5c6ab4fb18fec35e4845913ec|094055182b0fa885947ed61ae81268a1",
            False,
        ),
        (
            "6e794ce5c6ab4fb18fec35e4845913ec094055182b0fa885947ed61ae81268a1e09d6071561b3f7417035863f0515559",
            False,
        ),
        (
            "6e794ce5c6ab4fb18fec35e4845913ec||094055182b0fa885947ed61ae81268a1e09d6071561b3f7417035863f0515559",
            False,
        ),
    ],
)
def test_validate_known_ids(identifier: str, *, is_valid: bool):
    assert is_valid_unique_id(identifier) == is_valid
