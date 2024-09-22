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
        MODELS_PATH (DirectoryPath): Filesystem path to the model.
        MODELS_NAME (str): Name of the ML model.
        VERSION (str): Version of the ML model.
        DATA_FILE_NAME (str): Name of the data file.
    """

    model_config = SettingsConfigDict(
        env_file='config/.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    MODELS_PATH: DirectoryPath
    MODELS_NAME: str
    VERSION: str
    DATA_FILE_NAME: str


model_settings = ModelSettings()
