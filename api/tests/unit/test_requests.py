import os
from http import HTTPStatus
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from zimitfrontend.main import Main
from zimitfrontend.tracker import tracker


@pytest.fixture(scope="module")
def client():
    os.environ["LOCALES_LOCATION"] = "locales"
    app = Main().create_app()
    return TestClient(app, raise_server_exceptions=False)


@pytest.fixture(autouse=True)
def clean_tracker():
    tracker.known_clients.clear()
    yield
    tracker.known_clients.clear()


@pytest.mark.parametrize(
    "invalid_url",
    [
        "www.kiwix.org",
        "example.com",
        "example.com/path",
        "https://",
        "http://",
        "ftp://example.com",
        "javascript:alert(1)",
    ],
)
def test_create_task_invalid_url(client: TestClient, invalid_url: str):
    response = client.post(
        "/api/v1/requests",
        json={
            "url": invalid_url,
            "lang": "en",
            "flags": {},
            "uniqueId": None,
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {
        "detail": {
            "error": "invalid_url",
            "message": "A valid HTTP or HTTPS URL with a hostname is required",
        }
    }


def test_create_task_zim_file_fallback_when_none(client: TestClient):
    with patch("zimitfrontend.routes.requests.query_api") as mock_query_api:
        mock_query_api.side_effect = [
            (True, HTTPStatus.CREATED, {"_id": "recipe123"}),
            (True, HTTPStatus.CREATED, {"requested": ["task123"]}),
            (True, HTTPStatus.OK, {}),
        ]
        response = client.post(
            "/api/v1/requests",
            json={
                "url": "https://www.example.com/page",
                "lang": "en",
                "flags": {"zim-file": None},
                "uniqueId": None,
            },
        )
        assert response.status_code == HTTPStatus.CREATED
        assert response.json()["id"] == "task123"

        # Verify recipe payload has correct fallback zim-file
        recipe_call = mock_query_api.call_args_list[0]
        recipe_payload = recipe_call.kwargs["payload"]
        zim_file = recipe_payload["config"]["offliner"]["zim-file"]
        assert zim_file.startswith("www.example.com_")
        assert zim_file.endswith(".zim")


def test_create_task_zim_file_fallback_when_missing(client: TestClient):
    with patch("zimitfrontend.routes.requests.query_api") as mock_query_api:
        mock_query_api.side_effect = [
            (True, HTTPStatus.CREATED, {"_id": "recipe123"}),
            (True, HTTPStatus.CREATED, {"requested": ["task123"]}),
            (True, HTTPStatus.OK, {}),
        ]
        response = client.post(
            "/api/v1/requests",
            json={
                "url": "https://www.example.com/page",
                "lang": "en",
                "flags": {},
                "uniqueId": None,
            },
        )
        assert response.status_code == HTTPStatus.CREATED
        assert response.json()["id"] == "task123"

        recipe_call = mock_query_api.call_args_list[0]
        recipe_payload = recipe_call.kwargs["payload"]
        zim_file = recipe_payload["config"]["offliner"]["zim-file"]
        assert zim_file.startswith("www.example.com_")
        assert zim_file.endswith(".zim")


def test_create_task_custom_zim_file(client: TestClient):
    with patch("zimitfrontend.routes.requests.query_api") as mock_query_api:
        mock_query_api.side_effect = [
            (True, HTTPStatus.CREATED, {"_id": "recipe123"}),
            (True, HTTPStatus.CREATED, {"requested": ["task123"]}),
            (True, HTTPStatus.OK, {}),
        ]
        response = client.post(
            "/api/v1/requests",
            json={
                "url": "https://www.example.com/page",
                "lang": "en",
                "flags": {"zim-file": "custom_name"},
                "uniqueId": None,
            },
        )
        assert response.status_code == HTTPStatus.CREATED

        recipe_call = mock_query_api.call_args_list[0]
        recipe_payload = recipe_call.kwargs["payload"]
        zim_file = recipe_payload["config"]["offliner"]["zim-file"]
        assert zim_file.startswith("custom_name_")
        assert zim_file.endswith(".zim")
