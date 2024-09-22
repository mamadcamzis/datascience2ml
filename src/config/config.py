"""
This module sets up the configuration for the data science project using Pydantic for settings management,
Loguru for logging, and SQLAlchemy for database connection.
Attributes:
    CONFI_DIR (Path): The directory where the configuration file is located.
    PARENT_DIR (Path): The parent directory of the configuration directory.
    LOGER_DIR (Path): The directory where log files will be stored.
    ENV_FILE (Path): The path to the environment file.
    LOGGER_FILE (Path): The path to the log file.
Classes:
    Settings(BaseSettings): A Pydantic model that loads settings from the environment file.
        Attributes:
            model_config (SettingsConfigDict): Configuration for loading environment variables.
            DATA_FILE_NAME (str): The name of the data file.
            DATA_PATH (DirectoryPath): The directory path where data files are stored.
            MODELS_PATH (DirectoryPath): The directory path where model files are stored.
            MODELS_NAME (str): The name of the model.
            VERSION (str): The version of the project.
            LOG_LEVEL (str): The logging level.
            DB_CONNECTION (str): The database connection string.
            TABLE_NAME (str): The name of the database table.
Variables:
    settings (Settings): An instance of the Settings class with loaded configuration.
    engine (Engine): An SQLAlchemy engine instance for database connection.
"""

from pydantic import DirectoryPath
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

from loguru import logger
from sqlalchemy import create_engine

CONFI_DIR = Path(__file__).parent.resolve()
PARENT_DIR = CONFI_DIR.parent
LOGER_DIR = PARENT_DIR / 'logs'

ENV_FILE = CONFI_DIR / '.env'
LOGGER_FILE = LOGER_DIR / 'app.log'

logger.info(f"Setting Config: {ENV_FILE}")

class Settings(BaseSettings):
    """A Pydantic model that loads settings from the environment file."""
    
    model_config = SettingsConfigDict(env_file=ENV_FILE, env_file_encoding='utf-8')
    DATA_FILE_NAME: str
    DATA_PATH: DirectoryPath
    MODELS_PATH: DirectoryPath
    MODELS_NAME: str
    VERSION: str
    LOG_LEVEL: str
    DB_CONNECTION: str
    TABLE_NAME: str
  
    
def configure_logging(log_level: str) -> None:
    """This function removes any existing loggers and adds a new logger with the specified settings.
    The log files are rotated daily, retained for two days, and compressed in zip format.
    Args:
        log_level (str): The logging level to be set for the logger.
    Returns:
        None
    """
    
    logger.remove()
    logger.add(LOGGER_FILE, 
               rotation="1 day",
               retention='2 days',
               compression="zip",
               level=log_level)

settings = Settings()
configure_logging(settings.LOG_LEVEL)
#engine = create_engine(f"sqlite:///{DB_DIR}/{settings.db_connection}") #echo=True
engine = create_engine(settings.DB_CONNECTION)