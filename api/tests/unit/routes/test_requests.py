import json
from http import HTTPStatus
from unittest.mock import MagicMock, patch
import pytest

from fastapi import HTTPException
from zimitfrontend.routes.requests import create_task
from zimitfrontend.routes.schemas import TaskCreateRequest, TaskCreateResponse


def test_create_task_with_block_rules():
    mock_request = MagicMock()
    mock_request.client.host = "127.0.0.1"

    task_create_request = TaskCreateRequest(
        url="https://example.com",
        lang="en",
        email="test@example.com",
        flags={},
        unique_id="test-unique-id",
        block_rules=[
            {"url": "google-analytics\\.com", "type": "block"},
            {"url": "internal\\.ip", "type": "block"},
        ],
    )

    # Mock query_api to return success for schedule creation and task request
    with patch("zimitfrontend.routes.requests.query_api") as mock_query_api,
        patch("zimitfrontend.tracker.tracker.add_task") as mock_add_task:

        # Mock schedule creation
        mock_query_api.side_effect = [
            (True, HTTPStatus.CREATED, {}),  # For /schedules POST
            (True, HTTPStatus.CREATED, {"requested": ["task-id-123"]}),  # For /requested-tasks POST
            (True, HTTPStatus.OK, {}),  # For /schedules DELETE
        ]

        mock_add_task.return_value.status = "task_added"
        mock_add_task.return_value.new_unique_id = "new-unique-id"

        response = create_task(task_create_request, mock_request)

        assert response.id == "task-id-123"
        assert response.new_unique_id == "new-unique-id"

        # Verify that query_api was called with blockRules in the payload
        # First call is for schedule creation
        args, kwargs = mock_query_api.call_args_list[0]
        assert kwargs["payload"]["config"]["offliner"]["blockRules"] == [
            {"url": "google-analytics\\.com", "type": "block"},
            {"url": "internal\\.ip", "type": "block"},
        ]

        # Verify if an empty block_rules list is handled
    task_create_request_empty_rules = TaskCreateRequest(
        url="https://example.com",
        lang="en",
        email="test@example.com",
        flags={},
        unique_id="test-unique-id",
        block_rules=[],
    )

    with patch("zimitfrontend.routes.requests.query_api") as mock_query_api,
        patch("zimitfrontend.tracker.tracker.add_task") as mock_add_task:

        mock_query_api.side_effect = [
            (True, HTTPStatus.CREATED, {}),
            (True, HTTPStatus.CREATED, {"requested": ["task-id-456"]}),
            (True, HTTPStatus.OK, {}),
        ]

        mock_add_task.return_value.status = "task_added"
        mock_add_task.return_value.new_unique_id = "new-unique-id-empty"

        response_empty = create_task(task_create_request_empty_rules, mock_request)

        assert response_empty.id == "task-id-456"
        assert response_empty.new_unique_id == "new-unique-id-empty"

        args, kwargs = mock_query_api.call_args_list[0]
        assert "blockRules" not in kwargs["payload"]["config"]["offliner"]

