"""
This module provides functionality for preparing a dataset for ML model.

It consists of functions to load data from a database,
encode categorical columns, and parse specific columns for further processing.
"""

import re

import pandas as pd
from loguru import logger

from model.pipeline.collect import load_data_from_db


def prepare_data() -> pd.DataFrame:
    """
    Prépare les données pour l'analyse en chargeant les données,
    en encodant les colonnes catégorielles,
    et en transformant la colonne 'garden'.

    Retour:
    -------
    pandas.DataFrame
        Un DataFrame préparé avec les colonnes catégorielles encodées
        et la colonne 'garden' transformée.

    Exemple:
    --------
    >>> df = prepare_data()
    >>> print(df.head())
    """
    logger.info("Preparing data pipeline processing ...")
    data = load_data_from_db()
    # Encoder les colonnes 'balcony', 'parking',
    # 'furnished', 'garage', 'storage'
    data_encoded = encode_cat_cols(data)
    # Parser la colonne 'garden'
    df = parse_garden_col(data_encoded)
    return df


def encode_cat_cols(data: pd.DataFrame,
                    columns: list = [
                        'balcony',
                        'parking',
                        'furnished',
                        'garage',
                        'storage']) -> pd.DataFrame:
    """
    Encode les colonnes catégorielles spécifiées dans un DataFrame
    en utilisant des variables fictives (one-hot encoding).

    Paramètres:
    -----------
    data : pandas.DataFrame
        Le DataFrame contenant les colonnes à encoder.
    columns : list, optionnel
        La liste des colonnes à encoder. Par défaut, ['balcony', 'parking',
        'furnished', 'garage', 'storage'].

    Retour:
    -------
    pandas.DataFrame
        Un DataFrame avec les colonnes spécifiées encodées en variables
        fictives, en supprimant la première catégorie pour éviter
        la multicolinéarité.

    Exemple:
    --------
    >>> df = pd.DataFrame({
    ...     'balcony': ['yes', 'no', 'no', 'yes'],
    ...     'parking': ['yes', 'yes', 'no', 'no'],
    ...     'furnished': ['yes', 'no', 'no', 'yes'],
    ...     'garage': ['no', 'no', 'yes', 'yes'],
    ...     'storage': ['yes', 'yes', 'no', 'no']
    ... })
    >>> encoded_df = encode_cat_cols(df)
    >>> print(encoded_df)
    """
    logger.info(f"Encoding categorical columns {columns}")
    return pd.get_dummies(data, columns=columns, drop_first=True)


def parse_garden_col(data: pd.DataFrame) -> pd.DataFrame:
    """
    Analyse et transforme la colonne 'garden' dans un DataFrame en remplaçant
    les valeurs textuelles par des valeurs numériques.

    Paramètres:
    -----------
    data : pandas.DataFrame
        Le DataFrame contenant la colonne 'garden' à transformer.

    Retour:
    -------
    pandas.DataFrame
        Le DataFrame avec la colonne 'garden' transformée
        en valeurs numériques.

    Exemple:
    --------
    >>> df = pd.DataFrame({
    ...     'garden': ['Not present', 'Present: 50 sqm',
    'Not present', 'Present: 30 sqm']
    ... })
    >>> df = parse_garden_col(df)
    >>> print(df)
    """

    logger.info("Parsing 'garden' column ...")
    data['garden'] = data['garden'].apply(
        lambda x: 0 if x == 'Not present' else int(re.findall(r'\d+', x)[0]),
    )
    return data
