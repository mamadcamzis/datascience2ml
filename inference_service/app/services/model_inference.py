"""
This module provides functionality for managing a ML model.

It contains the ModelInferenceService class, which handles loading and using
a pre-trained ML model. The class offers methods to load a model
from a file, building it if it doesn't exist, and to make predictions
using the loaded model.
"""

from pathlib import Path

import joblib
import pandas as pd
from loguru import logger

from .config import model_settings


class ModelInferenceService:
    """
    A service class for Inference the ML model.

    This class provides functionalities to load a ML model from
    a specified path, build it if it doesn't exist, and make
    predictions using the loaded model.

    Attributes:
        model: ML model managed by this service. Initially set to None.
        model_path (str): The path to the directory containing the model.
        model_name (str): The name of the model to load.

    Methods:
        __init__: Constructor that initializes the ModelService.
        load_model: Loads the model from file or builds it if it doesn't exist.
        predict: Makes a prediction using the loaded model.
    """

    def __init__(self) -> None:
        """Initialize the ModelInferenceService with default values."""
        self.model = None
        self.model_name = model_settings.models_name
        self.model_path = model_settings.models_path
        self.model_version = model_settings.version

    def load_model(self, model_name=None) -> None:
        """Load the model from a specified path, or builds it if not exist.

        Args:
            model_name (str, optional): The name of the model to load.
                Defaults to None.

        Raises:
            FileNotFoundError: If the model file is not found
                                at the specified path
        """
        logger.info('Checking the existence of model config file ...')
        if model_name:
            self.model_name = model_name

        version = model_settings.version
        joblib_model = f'{self.model_name}_version_{version}.joblib'
        model_path = Path(f'{self.model_path}/{joblib_model}')

        if not model_path.exists():
            raise FileNotFoundError(f'Model not found at {model_path} -> ')

        logger.info(
            f'Model {self.model_name} exists -> '
            f'Loading Model from {model_path} ...',
        )
        with open(model_path, 'rb') as fichier:
            self.model = joblib.load(fichier)

    def predict(self, input_parameters: list) -> list:
        """
        Make a prediction using the loaded model.

        Takes input parameters and passes it to the model, which
        was loaded using a pickle file. The model then predicts.

        Args:
            input_parameters (list): The input data for making a prediction.

        Returns:
            list: The prediction result from the model.
        """
        logger.info(
            'Predicting the price of the house with the following '
            f'parameters {input_parameters} ...',
        )
        if not isinstance(input_parameters, pd.DataFrame):
            input_parameters = pd.DataFrame(
                [input_parameters],
                columns=[
                    'area',
                    'constraction_year',
                    'bedrooms',
                    'garden',
                    'balcony_yes',
                    'parking_yes',
                    'furnished_yes',
                    'garage_yes',
                    'storage_yes',
                ],
            )

        return self.model.predict(input_parameters).tolist()
