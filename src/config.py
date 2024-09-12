import os

from pydantic import Field
from pydantic import FilePath, DirectoryPath
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

from loguru import logger

PARENT_DIR = Path(__file__).parent.resolve().parent
# DATA_DIR = PARENT_DIR / 'datas'
# MODELS_DIR = PARENT_DIR / 'models'
ENV_FILE = PARENT_DIR / '.env'

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
    LOG_level : str
  
    
settings = Settings()

logger.remove()
logger.add("app.log", rotation="1 day", compression="zip", level=settings.LOG_level)

# if __name__ == '__main__':
#     print("GO")
#     print(f"data file name {settings.DATA_FILE_NAME}\n")
#     print(f"Model path {settings.MODELS_PATH}\n")
#     print(f"Model name {settings.MODELS_NAME}\n")
#     print(f"DATA PATH {settings.DATA_PATH}\n")
#     print(f"Version {settings.VERSION}\n")