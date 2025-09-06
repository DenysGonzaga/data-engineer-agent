"""Module containing all settings and tools necessary to agent works."""

import boto3
from dynaconf import Dynaconf

settings = Dynaconf(
    environments=True,
    envvar_prefix="DYNACONF",
    settings_files=["../settings.toml"],
)

settings.setenv("development")


def __get_session():
    args = {}

    if hasattr(settings, "AWS_PROFILE"):
        args = {"profile_name": settings.AWS_PROFILE}
    else:
        args = {
            "aws_access_key_id": settings.AWS_ACCESS_KEY_ID,
            "aws_secret_access_key": settings.AWS_SECRET_ACCESS_KEY,
            "aws_session_token": settings.AWS_SESSION_TOKEN,
            "region_name": settings.AWS_DEFAULT_REGION,
        }

    return boto3.Session(**args)


session = __get_session()
