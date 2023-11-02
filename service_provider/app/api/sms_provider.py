from typing import Tuple

import aiohttp

from service_provider.app.api.base import BaseVonageProviderInterface
from service_provider.app.constants import BASE_VONAGE_ENDPOINT
from service_provider.app.schemas.schemas import CodeSchemaRequest, VerifyDataRequest
from service_provider.app.settings import settings


class VonageSMSProvider(BaseVonageProviderInterface):
    async def verify_request(self) -> Tuple[int, dict]:
        """
        Verify 2FA request
        :return: status code and content that is received from Vonage API
        """
        headers = {
            "Authorization": self.base64_auth_header,
            "Content-Type": "application/json",
        }

        url = f"{BASE_VONAGE_ENDPOINT}/verify"

        payload = VerifyDataRequest(
            brand="ACME", workflow=[{"channel": "sms", "to": settings.PHONE_NUMBER}]
        )
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url, json=payload.dict(), headers=headers
            ) as response:
                data = await response.json()
                return response.status, data

    async def check_code(
        self, request_id: str, code: CodeSchemaRequest
    ) -> Tuple[int, dict]:
        """
        Verify user's OTP code
        :param request_id: ID of the verify request
        :param code: OTP code provided by user
        :return: status code and content that is received from Vonage API
        """
        headers = {
            "Authorization": self.base64_auth_header,
            "Content-Type": "application/json",
        }

        url = f"{BASE_VONAGE_ENDPOINT}/verify/{request_id}"
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=code.dict(), headers=headers) as response:
                data = await response.json()
                return response.status, data
