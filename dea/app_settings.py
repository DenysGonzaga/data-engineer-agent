import boto3
from dynaconf import Dynaconf
from app_settings import app_settings


app_settings = Dynaconf(
    environments=True,
    envvar_prefix="DYNACONF",
    settings_files=["../settings.toml"],
)

app_settings.setenv("development")

def __get_session():
    if hasattr(app_settings, 'AWS_PROFILE'):
        return boto3.Session(profile_name=app_settings.AWS_PROFILE)
    else:
        return boto3.Session(
            aws_access_key_id=app_settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=app_settings.AWS_SECRET_ACCESS_KEY,
            aws_session_token=app_settings.AWS_SESSION_TOKEN,
            region_name=app_settings.AWS_DEFAULT_REGION,
        )
    
session = __get_session()