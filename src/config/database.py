"""
This module sets up the database configuration.

It utilizes Pydantic's BaseSettings for configuration management,
allowing settings to be read from environment variables and a .env file.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine


class DbSettings(BaseSettings):
    """
    Database configuration settings for the application.

    Attributes:
        model_config (SettingsConfigDict): Model config, loaded from .env file.
        DB_CONNECTION (str): Database connection string.
        TABLE_NAME (str): Name of the rental apartments table in DB.
"""

    model_config = SettingsConfigDict(
        env_file='config/.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    DB_CONNECTION: str
    TABLE_NAME: str


db_settings = DbSettings()

engine = create_engine(db_settings.DB_CONNECTION)
