# 2FA verification via Vonage

* [Overview](#overview)
* [Project set up](#project-set-up)

## Overview
A microservice that integrates with an SMS provider to verify 2FA passcodes.
Any user on the platform should be able to provide a login and password to log in.
To enforce security and prevent unwanted access to the user's profile,
the platform offers an additional layer of protection - 2FA.
Microservice implements verification of account ownership
by sending an SMS to an already registered phone number on our platform
that is linked to the user's account. If the user provides the correct code,
the platform will allow the user to log in. If the code is wrong,
the user should be notified that the verification code is incorrect.

## Project set up:
Firstly, add environment variables  in `.env`
in /service_provider directory. Environment variables in `.env` are the same as
environment variables in `/service_provider/.test.env` file.

To set up project on your local machine run command:

```bash
docker compose up --build
```

Or create venv install requirements and run project in terminal:
```bash
python3 -m venv venv
. venv/bin/activate
cd service_provider
poetry install
uvicorn service_provider.app.main:app --host 0.0.0.0 --port 8080 --reload
```

Application will be running on host `0.0.0.0` and `8080` port.

You can use swagger documentation of the application to test how it works.
Go to `http://0.0.0.0:8080/docs` and test the endpoints.

### Tests
To run tests use command:
```bash
pytest tests
```