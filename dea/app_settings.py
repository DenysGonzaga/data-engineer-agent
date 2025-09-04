import boto3
from dynaconf import Dynaconf

settings = Dynaconf(
    environments=True,
    envvar_prefix="DYNACONF",
    settings_files=["../settings.toml"],
)

settings.setenv("development")

def __get_session():
    if hasattr(settings, 'AWS_PROFILE'):
        return boto3.Session(profile_name=settings.AWS_PROFILE)
    else:
        return boto3.Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            aws_session_token=settings.AWS_SESSION_TOKEN,
            region_name=settings.AWS_DEFAULT_REGION,
        )
    
session = __get_session()