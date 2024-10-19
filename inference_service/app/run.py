
"""
Flask app Entry Point.

This module serves as the entry point for the Flask application.

Usage:
    The flask app is created and started here.
    The prediction blueprint(`api.bp.prediction`) is registered here.
"""

from api.prediction import bp as prediction_bp
from flask import Flask

app = Flask(__name__)
app.register_blueprint(prediction_bp)

if __name__ == '__main__':
    app.run(debug=True)
