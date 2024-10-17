"""
This module provides functionality for trainiig a ML model.

It contains the ModelBuilderService class, which handles the training
of a ML model from a specified path,
"""

from pathlib import Path

from loguru import logger

from config import model_settings
from model.pipeline.model import build_model


class ModelBuilderService:
    """
    A service class for managing the ML model.

    This class provides functionalities to load a ML model from
    a specified path, build it if it doesn't exist, and make
    predictions using the loaded model.

    Attributes:
        model_path (str): The path to the directory containing the model.
        model_name (str): The name of the model to train.
        model_version (str): The version of the model to train.

    Methods:
        __init__: Constructor that initializes the ModelBuilderService.
        train_model: Train the model from a specified path.
    """

    def __init__(self) -> None:
        """Initialize the ModelService with default values."""
        self.model_path = model_settings.models_path
        self.model_name = model_settings.models_name
        self.model_version = model_settings.version

    def train_model(self, model_name=None) -> None:
        """Train the model from a specified path, or builds it if not exist.

        Args:
            model_name (str, optional): The name of the model to load.
                Defaults to None.
        """
        logger.info('Checking the existence of model config file ...')
        if model_name:
            self.model_name = model_name

        joblib_model = f'{self.model_name}_version_{self.model_version}.joblib'
        model_path = Path(f'{self.model_path}/{joblib_model}')

        if not model_path.exists():
            logger.warning(
                f'Model not found at {model_path} -> '
                + f'Building a new {model_settings.models_name} model ...',
            )

            build_model()
