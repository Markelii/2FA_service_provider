import base64
from abc import ABC, abstractmethod
from typing import Tuple

from service_provider.app.schemas.schemas import CodeSchemaRequest
from service_provider.app.settings import settings


class BaseVonageProviderInterface(ABC):
    @property
    def base64_auth_header(self) -> str:
        """
        Prepare auth header based on Vonage Basic Authentication
        :return: prepared Authorization header
        """
        credentials = f"{settings.API_KEY}:{settings.API_SECRET}".encode("utf-8")
        base64_credentials = base64.b64encode(credentials).decode("utf-8")
        return f"Basic {base64_credentials}"

    @abstractmethod
    async def verify_request(self) -> Tuple[int, dict]:
        """
        Verify 2FA request
        :return: status code and content that is received from Vonage API
        """
        pass

    @abstractmethod
    async def check_code(
        self, request_id: str, code: CodeSchemaRequest
    ) -> Tuple[int, dict]:
        """
        Verify user's OTP code
        :param request_id: ID of the verify request
        :param code: OTP code provided by user
        :return: status code and content that is received from Vonage API
        """
        pass
