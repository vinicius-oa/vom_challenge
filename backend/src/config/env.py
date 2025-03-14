from pydantic_settings import BaseSettings, SettingsConfigDict

from infra.database.factory.enums import SupportedDatabasesEnum


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    DATABASE: SupportedDatabasesEnum = SupportedDatabasesEnum.sqlite
    DNS: str = "sqlite:///:memory:"
