from pydantic import FilePath, DirectoryPath
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    
    data_filename : FilePath
    model_path : DirectoryPath
    version : str
    model_name : str
    
    

settings = Settings()

