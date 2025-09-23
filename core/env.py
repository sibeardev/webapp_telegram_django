from functools import cached_property

from pydantic import AnyHttpUrl, BaseModel, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class TelegramSettings(BaseModel):
    TOKEN: str
    ADMINS: list[int]
    SECRET: str


class PostgresSettings(BaseModel):
    USER: str
    PASSWORD: str
    DB: str
    HOST: str = "db"
    PORT: int = 5432
    URL: str | None = None

    @model_validator(mode="after")
    def assemble_url(cls, model):
        if not model.URL:
            model.URL = f"postgresql://{model.USER}:{model.PASSWORD}@{model.HOST}:{model.PORT}/{model.DB}"
        return model


class DjangoSettings(BaseModel):
    SECRET_KEY: str
    ALLOWED_HOSTS: list[str] = ["127.0.0.1", "localhost"]
    CSRF_TRUSTED_ORIGINS: list[str] = []


class EnvSettings(BaseSettings):
    DJANGO: DjangoSettings
    POSTGRES: PostgresSettings
    TELEGRAM: TelegramSettings
    EXTERNAL_URL: AnyHttpUrl
    PORT: int = 8000
    DEBUG: bool = True
    PROJECT_NAME: str = "mimir"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        case_sensitive=False,
        validate_default=True,
        ignored_types=(cached_property,),
        extra="allow",
        use_attribute_docstrings=True,
    )
