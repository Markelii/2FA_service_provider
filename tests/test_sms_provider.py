import base64
from unittest.mock import MagicMock

import pytest

from service_provider.app.api.sms_provider import VonageSMSProvider
from service_provider.app.schemas.schemas import (
    CodeSchemaRequest,
    ConflictSchemaResponse,
    InvalidCodeSchemaResponse,
    Successful2FAVerificationSchemaResponse,
    VerifyDataResponse,
)
from service_provider.app.settings import settings


class TestSMSProvider:
    def test_base64_auth_header(self):
        provider = VonageSMSProvider()
        auth_header = provider.base64_auth_header
        # pytest-dotenv overwrite env vars from .env with .test.env vars
        expected_credentials = f"{settings.API_KEY}:{settings.API_SECRET}".encode(
            "utf-8"
        )
        expected_base64_credentials = base64.b64encode(expected_credentials).decode(
            "utf-8"
        )
        expected_auth_header = f"Basic {expected_base64_credentials}"
        assert auth_header == expected_auth_header

    @pytest.mark.parametrize(
        "status_code, content",
        [
            (
                202,
                VerifyDataResponse(
                    request_id="abcd", check_url="https://example.com/"
                ).dict(),
            ),
            (
                409,
                ConflictSchemaResponse(
                    title="Conflict",
                    type="some_type",
                    detail="detail",
                    instance="instance",
                    request_id="eg45y2545c-t34",
                ).dict(),
            ),
        ],
    )
    @pytest.mark.asyncio
    async def test_verify_request(self, mocker, status_code, content):
        # Mock the ClientSession and response
        mock_post = MagicMock()
        mock_post.return_value.__aenter__.return_value.status = status_code
        mock_post.return_value.__aenter__.return_value.json.return_value = content
        mocker.patch("aiohttp.ClientSession.post", mock_post)
        provider = VonageSMSProvider()  # Instantiate your class
        status, data = await provider.verify_request()

        assert status == status_code
        assert data == content

    @pytest.mark.parametrize(
        "status_code, content",
        [
            (
                200,
                Successful2FAVerificationSchemaResponse(
                    request_id="abcd", status="completed"
                ).dict(),
            ),
            (
                400,
                InvalidCodeSchemaResponse(
                    title="Conflict",
                    type="some_type",
                    detail="detail",
                    instance="instance",
                ).dict(),
            ),
        ],
    )
    @pytest.mark.asyncio
    async def test_check_code(self, mocker, status_code, content):
        mock_post = MagicMock()
        mock_post.return_value.__aenter__.return_value.status = status_code
        mock_post.return_value.__aenter__.return_value.json.return_value = content
        mocker.patch("aiohttp.ClientSession.post", mock_post)
        provider = VonageSMSProvider()
        status, data = await provider.check_code(
            request_id="1234", code=CodeSchemaRequest(code="1234")
        )

        assert status == status_code
        assert data == content
