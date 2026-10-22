from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from zimitfrontend.main import Main


@pytest.fixture
def client() -> TestClient:
    return TestClient(Main().create_app())


@pytest.mark.parametrize(
    "method, path",
    [
        ("POST", "/api/v1/requests/"),
        ("GET", "/api/v1/offliner-definition/"),
    ],
)
def test_no_trailing_slash_redirection(client: TestClient, method: str, path: str):
    """Verify that routes with trailing slashes return 404 rather than 307."""
    response = client.request(method, path)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_valid_route_without_trailing_slash(client: TestClient):
    """Verify that valid routes without trailing slash are reached directly."""
    response = client.post("/api/v1/requests")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
