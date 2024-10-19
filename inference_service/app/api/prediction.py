"""
This module defines two endpoints for making predictions.

It uses Flask for handling HTTP requests and Pydantic for data validation.
Endpoints:
- GET /pred/: Fetches prediction based on query parameters.
- POST /pred/: Fetches prediction based on JSON payload.

Functions:
- get_prediction(): Handles GET requests to fetch predictions.
- get_prediction_post(): Handles POST requests to fetch predictions.
Both functions validate the input data using the Appartment schema
and then use the model_inference_service to make predictions based
on the validated data.
"""

from flask import Blueprint, abort, request
from pydantic import ValidationError
from schema.appartment import Appartment
from services import model_inference_service

bp = Blueprint('prediction', __name__, url_prefix='/pred')


@bp.get('/')
def get_prediction():
    """Handle GET requests to fetch predictions.

    Returns:
        dict: A dictionary containing the prediction.
    """
    # Get and check parameters fetched from the request
    try:
        appartment_features = Appartment(**request.args)
    except ValidationError:
        return abort(code=400, description='Bad Input parameters: ')

    # Make prediction
    prediction = model_inference_service.predict(
        list(appartment_features.model_dump().values()),
        )
    return {'prediction': prediction}


@bp.post('/')
def get_prediction_post():
    """Handle POST requests to fetch predictions.

    Returns:
        dict: A dictionary containing the prediction.
    """
    # Get and check parameters fetched from the request
    try:
        appartment_features = Appartment(**request.json)
    except ValidationError:
        return abort(code=400, description='Bad Input parameters: ')
    appartment_features = Appartment(**request.json)

    # Make prediction
    prediction = model_inference_service.predict(
        list(appartment_features.model_dump().values()),
        )
    return {'prediction': prediction}
