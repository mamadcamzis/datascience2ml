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
logger.add(LOGGER_FILE, rotation="1 day", compression="zip", level=settings.LOG_LEVEL)
#engine = create_engine(f"sqlite:///{DB_DIR}/{settings.db_connection}") #echo=True
engine = create_engine(settings.DB_CONNECTION)