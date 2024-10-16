"""
This module sets up the ML model configuration.

It utilizes Pydantic's BaseSettings for configuration management,
allowing settings to be read from environment variables and a .env file.
"""

from pydantic import DirectoryPath
from pydantic_settings import BaseSettings, SettingsConfigDict


class ModelSettings(BaseSettings):
    """
    ML model configuration settings for the application.

    Attributes:
        model_config (SettingsConfigDict): Model config, loaded from .env file.
        models_path (DirectoryPath): Filesystem path to the model.
        models_name (str): Name of the ML model.
        version (str): Version of the ML model.
        data_file_name (str): Name of the data file.
    """

    model_config = SettingsConfigDict(
        env_file="config/.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    models_path: DirectoryPath
    models_name: str
    version: str
    data_file_name: str


model_settings = ModelSettings()
