from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from service_provider.app.api.sms_provider import VonageSMSProvider
from service_provider.app.schemas.schemas import (
    CodeSchemaRequest,
    ConflictSchemaResponse,
    InvalidCodeSchemaResponse,
    RateLimitHitSchemaResponse,
    VerifyDataResponse,
)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post(
    "/2FA_request",
    description="2FA verification request",
    responses={
        202: {"model": VerifyDataResponse},
        409: {"model": ConflictSchemaResponse},
        429: {"model": RateLimitHitSchemaResponse},
    },
)
async def verify_2fa_request():
    provider = VonageSMSProvider()
    status_code, content = await provider.verify_request()
    return JSONResponse(status_code=status_code, content=content)


@app.post(
    "/check_code/{request_id}",
    description="Provide OTP code to finish 2FA verification",
    responses={
        200: {"model": VerifyDataResponse},
        400: {"model": InvalidCodeSchemaResponse},
        404: {"model": RateLimitHitSchemaResponse},
        409: {"model": InvalidCodeSchemaResponse},
        410: {"model": InvalidCodeSchemaResponse},
        429: {"model": InvalidCodeSchemaResponse},
    },
)
async def check_code(request_id: str, payload: CodeSchemaRequest):
    provider = VonageSMSProvider()
    status_code, content = await provider.check_code(request_id, payload)
    return JSONResponse(status_code=status_code, content=content)
