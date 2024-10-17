"""
Main application script for running the ML model service.

This script initializes the ModelService, loads the ML model, makes
a prediction based on predefined input parameters, and logs the output.
It demonstrates the typical workflow of using the ModelService in
a practical application context.
"""

from loguru import logger

from model.model_builder import ModelBuilderService


@logger.catch
def main():
    """Run function to launch the application."""
    logger.info(
        'Starting the prediction process, running \
        the application ...',
    )
    ml_svc = ModelBuilderService()
    # Train Model
    ml_svc.train_model()
    logger.info('Training Model completed ...')


if __name__ == '__main__':
    main()
