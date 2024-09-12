import joblib

import pandas as pd

from pathlib import Path
from config import settings
from model import build_model

from loguru import logger


class ModelService:
    
    def __init__(self) -> None:
        
        self.model = None
        self.model_name = settings.MODELS_NAME
    
    def load_model(self, model_name=None):
        
        logger.info("Checking the existence of model config file ...")
        if model_name:
            self.model_name = model_name
            
        joblib_model = self.model_name + '_v_' + settings.VERSION + '.joblib'
        model_path = Path(f"{settings.MODELS_PATH}/{joblib_model}")  
    
        if not model_path.exists():
            logger.warning(f"Model not found at {model_path} -> building a new {settings.MODELS_NAME} model ...")
            build_model()
        
        
        logger.info(f"Model {settings.MODELS_NAME} exists -> Loading Model from {model_path} ...")   
        self.model = joblib.load(model_path)
        
    def predict(self, input_parameters):
        
        logger.info(f"Predicting the price of the house with the following parameters {input_parameters} ...")
        if not isinstance(input_parameters, pd.DataFrame):
            input_parameters = pd.DataFrame([input_parameters], 
                                    columns=['area',  'constraction_year',  'bedrooms', 
                                            'garden', 'balcony_yes', 'parking_yes', 
                                            'furnished_yes', 'garage_yes', 'storage_yes'])
            
        return self.model.predict(input_parameters)
    
    
    


            