import os

from pydantic import Field
from pydantic import FilePath, DirectoryPath
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from loguru import logger
from sqlalchemy import create_engine

PARENT_DIR = Path(__file__).parent.resolve().parent
# DATA_DIR = PARENT_DIR / 'datas'
# MODELS_DIR = PARENT_DIR / 'models'
ENV_FILE = PARENT_DIR / '.env'
DB_DIR = PARENT_DIR / 'databases'

# Path(DATA_DIR).mkdir(parents=True, exist_ok=True)
# Path(MODELS_DIR).mkdir(parents=True, exist_ok=True)


class Settings(BaseSettings):
    #file_path = Field(DATA_DIR / 'data.csv', env='DATA_FILE_NAME')
    model_config = SettingsConfigDict(env_file=ENV_FILE, env_file_encoding='utf-8')
    DATA_FILE_NAME : str
    DATA_PATH: DirectoryPath
    MODELS_PATH : DirectoryPath
    MODELS_NAME : str 
    VERSION : str 
    LOG_LEVEL : str
    DB_CONNECTION : str
    TABLE_NAME : str
  
    
settings = Settings()

logger.remove()
logger.add("app.log", rotation="1 day", compression="zip", level=settings.LOG_LEVEL)
#engine = create_engine(f"sqlite:///{DB_DIR}/{settings.db_connection}") #echo=True
engine = create_engine(settings.DB_CONNECTION)