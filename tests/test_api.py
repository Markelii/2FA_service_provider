from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from service_provider.app.main import app


@pytest.fixture
def test_client():
    return TestClient(app)


def test_verify_request(test_client, mocker):
    mock_post = MagicMock()
    mock_post.return_value.__aenter__.return_value.status = 202
    mock_post.return_value.__aenter__.return_value.json.return_value = {
        "request_id": "abcd",
        "check_url": "https://example.com/",
    }
    mocker.patch("aiohttp.ClientSession.post", mock_post)
    response = test_client.post("/2FA_request")
    assert response.status_code == 202
    assert response.json()["request_id"] == "abcd"
    assert response.json()["check_url"] == "https://example.com/"


def test_check_code(test_client, mocker):
    mock_post = MagicMock()
    mock_post.return_value.__aenter__.return_value.status = 200
    mock_post.return_value.__aenter__.return_value.json.return_value = {
        "request_id": "abcd",
        "status": "completed",
    }
    mocker.patch("aiohttp.ClientSession.post", mock_post)
    response = test_client.post("/check_code/abcd", json={"code": "1234"})
    assert response.status_code == 200
    assert response.json()["request_id"] == "abcd"
    assert response.json()["status"] == "completed"
