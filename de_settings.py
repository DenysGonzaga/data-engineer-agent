from dynaconf import Dynaconf

app_settings = Dynaconf(
    environments=True,
    envvar_prefix="DYNACONF",
    settings_files=["settings.toml"],
)

app_settings.setenv("development")
