from typing import List, Optional

from pydantic import BaseModel, HttpUrl


class Workflow(BaseModel):
    channel: str
    to: str


class VerifyDataRequest(BaseModel):
    locale: Optional[str]
    channel_timeout: Optional[int]
    client_ref: Optional[str]
    code_length: Optional[int]
    code: Optional[str]
    brand: str
    workflow: List[Workflow]


class VerifyDataResponse(BaseModel):
    request_id: str
    check_url: HttpUrl


class ConflictSchemaResponse(BaseModel):
    title: str
    type: str
    detail: str
    instance: str
    request_id: str


class RateLimitHitSchemaResponse(BaseModel):
    title: str
    type: str
    detail: str
    instance: str


class Successful2FAVerificationSchemaResponse(BaseModel):
    request_id: str
    status: str


class BaseInvalidCodeSchemaResponse(BaseModel):
    title: str
    detail: str
    instance: str


class InvalidCodeSchemaResponse(BaseInvalidCodeSchemaResponse):
    type: str


class CodeSchemaRequest(BaseModel):
    code: str
