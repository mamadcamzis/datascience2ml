"""
Main application script for running the ML model service.

This script initializes the ModelService, loads the ML model, makes
a prediction based on predefined input parameters, and logs the output.
It demonstrates the typical workflow of using the ModelService in
a practical application context.
"""

from loguru import logger

from model.model_service import ModelService


@logger.catch
def main():
    """Main function to run the application."""

    logger.info(
        'Starting the prediction process, running \
        the application ...'
    )
    ml_svc = ModelService()
    # Load Model
    ml_svc.load_model()
    pred = ml_svc.predict([85, 2015, 2, 20, 1, 1, 0, 0, 1])

    logger.info(f'Prediction is: {pred[0]:.2f} ...')
    logger.info('Application run completed ...')


if __name__ == '__main__':
    main()
