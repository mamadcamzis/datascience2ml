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
from pydantic import FilePath
from sqlalchemy import select
from loguru import logger

from databases.db_model import RentApartments
from config import model_settings
from config import engine


def load_data(path: FilePath = model_settings.DATA_FILE_NAME) -> pd.DataFrame:
    """
    Charge un fichier CSV à partir d'un chemin donné et le renvoie sous forme DataFrame pandas.

    Paramètres:
    -----------
    path : FilePath, optionnel
        Le chemin vers le fichier CSV à charger. Par défaut, il utilise la variable `model_settings.DATA_FILE_NAME`.

    Retour:
    -------
    pandas.DataFrame
        Un DataFrame contenant les données du fichier CSV.

    Exemple:
    --------
    >>> df = load_data('data/raw/my_data.csv')
    >>> print(df.head())
    """
    csv_path = os.path.join(model_settings.DATA_PATH, path)
    logger.info(f"Loading csv file at {csv_path} ...")
    return pd.read_csv(csv_path)


def load_data_from_db() -> pd.DataFrame:
    """
    Charge les données à partir d'une base de données SQLite.

    Retour:
    -------
    pandas.DataFrame
        Un DataFrame contenant les données de la table 'data'.

    Exemple:
    --------
    >>> df = load_data_from_db()
    >>> print(df.head())
    """
    logger.info("Loading data from database ...")
    query = select(RentApartments)
    return pd.read_sql(query, engine)
