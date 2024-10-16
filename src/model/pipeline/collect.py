"""
This module provides functionalities to load data from a database.

It includes a function to extract data from the RentApartments table
in the database and load it into a pandas DataFrame. This module is useful
for scenarios where data needs to be retrieved from a database for further
analysis or processing. It uses SQLAlchemy for executing database queries
and pandas for handling the data in a DataFrame format.
"""

import os

import pandas as pd
from loguru import logger
from pydantic import FilePath
from sqlalchemy import select

from config import engine, model_settings
from databases.db_model import RentApartments


def load_data(path: FilePath = model_settings.data_file_name) -> pd.DataFrame:
    """Load a CSV file from a given path and return it as a pandas DataFrame.

    Parameters:
        path : FilePath, optional
            The path to the CSV file to load. By default, it uses the variable
            `model_settings.data_file_name`.

    Returns:
        A DataFrame containing the data from the CSV file.

    Example:
    >>> df = load_data('data/raw/my_data.csv')
    >>> print(df.head())
    """
    csv_path = os.path.join(model_settings.data_path, path)
    logger.info(f"Loading csv file at {csv_path} ...")
    return pd.read_csv(csv_path)


def load_data_from_db() -> pd.DataFrame:
    """Charge les données à partir d'une base de données SQLite.

    Returns:
        pd.DataFrame :Un DataFrame contenant les données de la table 'data'.

    Exemple:
    --------
    >>> df = load_data_from_db()
    >>> print(df.head())
    """
    logger.info("Loading data from database ...")
    query = select(RentApartments)
    return pd.read_sql(query, engine)
