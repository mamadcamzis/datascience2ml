import joblib
from pathlib import Path

import pandas as pd
from loguru import logger
from config.config import settings
from model.pipeline.model import build_model


class ModelService:
    """A service class for handling machine learning model operations such as loading a model and making predictions.
    Attributes:
        model (Any): The machine learning model instance.
        model_name (str): The name of the model to be loaded.
    Methods:
        __init__(): Initializes the ModelService with default values.
        load_model(model_name=None): Loads the machine learning model from a file.
        predict(input_parameters): Predicts the output using the loaded model based on input parameters.
        Initializes the ModelService instance with default values.
        Loads the machine learning model from a file. If the model file does not exist, it triggers the model building process.
        Args:
            model_name (str, optional): The name of the model to be loaded. Defaults to None.
        Predicts the output using the loaded model based on input parameters.
        Args:
            input_parameters (dict or pd.DataFrame): The input parameters for making predictions. If a dictionary is provided, it will be converted to a DataFrame.
        Returns:
            np.ndarray: The predicted values.
    """
    
    def __init__(self) -> None:
        """Initializes the ModelService with default values."""
        
        self.model = None
        self.model_name = settings.MODELS_NAME
    
    def load_model(self, model_name=None) -> None:
        """Loads the machine learning model from a file."""
        
        logger.info("Checking the existence of model config file ...")
        if model_name:
            self.model_name = model_name
            
        joblib_model = self.model_name + '_v_' + settings.VERSION + '.joblib'
        model_path = Path(f"{settings.MODELS_PATH}/{joblib_model}")  
    
        if not model_path.exists():
            logger.warning(f"Model not found at {model_path} -> building a new {settings.MODELS_NAME} model ...")
            build_model()
        
        logger.info(f"Model {settings.MODELS_NAME} exists -> Loading Model from {model_path} ...")   
        with open(model_path, 'rb') as file:
            self.model = joblib.load(file)
        
    def predict(self, input_parameters: list) -> list:
        """Predicts the output using the loaded model based on input parameters.
        Parameters:
        -----------
        input_parameters: list or pd.DataFrame
          
        Returns:
        --------
        list:
            The predicted output from the model.
        
        """
        
        logger.info(f"Predicting the price of the house with the following parameters {input_parameters} ...")
        if not isinstance(input_parameters, pd.DataFrame):
            input_parameters = pd.DataFrame([input_parameters], 
                                            columns=['area',  'constraction_year', 'bedrooms', 
                                            'garden', 'balcony_yes', 'parking_yes', 
                                            'furnished_yes', 'garage_yes', 'storage_yes'])
            
        return self.model.predict(input_parameters)