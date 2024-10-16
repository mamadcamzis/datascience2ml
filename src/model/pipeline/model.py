"""
This module creates the pipeline for building, training and saving ML model.

It includes the process of data preparation, model training using
RandomForestRegressor, hyperparameter tuning with GridSearchCV,
model evaluation, and serialization of the trained model.
"""

import os
from typing import List, Tuple

import joblib
import pandas as pd
from loguru import logger
from sklearn.base import BaseEstimator
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV, train_test_split

from config import model_settings
from model.pipeline.preparation import prepare_data


def build_model() -> None:
    """
    Construit, entraîne, évalue et sauvegarde un modèle de classification.

    Notes
    -----
    Cette fonction utilise les fonctions suivantes définies ailleurs :
        - prepare_data() : Prépare les données pour l'entraînement du modèle.
        - get_X_y(data) : Extrait les caractéristiques et la variable cible
            à partir des données.
        - split_train_test(X, y) : Divise les données en ensembles
            d'entraînement et de test.
        - train_model(X_train, y_train) : Entraîne le modèle avec les données
            d'entraînement.
        - evaluate_model(model, X_test, y_test) : Évalue les performances
            du modèle sur l'ensemble de test.
        - save_model(model) : Sauvegarde le modèle entraîné.

    """
    logger.info("Starting  Building Model Pipeline ...")
    # Préparation des données
    dataframe = prepare_data()
    # Extraction des caractéristiques et de la variable cible
    X, y = _get_x_y(dataframe)
    # Division en ensembles d'entraînement et de test
    X_train, X_test, y_train, y_test = split_train_test(X, y)
    # Entraînement du modèle
    rf_classifier = train_model(X_train, y_train)
    # Évaluation du modèle
    evaluate_model(rf_classifier, X_test, y_test)
    # Sauvegarde du modèle entraîné
    save_model(rf_classifier)


def _get_x_y(
    df: pd.DataFrame,
    col_x: List[str] = None,
    col_y: str = "rent",
) -> Tuple[pd.DataFrame, pd.Series]:
    """Extaction des features et du target.

    Les caractéristiques (`col_x`) et la variable cible (`col_y`)
    d'un DataFrame.

    Args:
        df: pandas.DataFrame
            Le DataFrame contenant les données.
        col_x: List[str], optional
            La liste des colonnes à utiliser comme caractéristiques.
            Les colonnes par défaut sont ['area', 'constraction_year',
            'bedrooms', 'garden', 'balcony_yes', 'parking_yes',
            'furnished_yes', 'garage_yes', 'storage_yes'].
        col_y: str, optional
            Le nom de la colonne à utiliser comme variable cible.
            La colonne par défaut est 'rent'.

    Returns:
        Tuple[pd.DataFrame, pd.Series]
            Un tuple contenant deux éléments :
                - X : pandas.DataFrame
                    Le DataFrame des caractéristiques.
                - y : pandas.Series
                    La série représentant la variable cible.
    """
    if col_x is None:
        col_x = [
            "area",
            "constraction_year",
            "bedrooms",
            "garden",
            "balcony_yes",
            "parking_yes",
            "furnished_yes",
            "garage_yes",
            "storage_yes",
        ]
    logger.info("Getting X, y data ...")
    X = df[col_x]
    y = df[col_y]
    return X, y


def split_train_test(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float = 0.2,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Separe les données en ensembles d'entraînement et de test.

    X = df[col_x]

    Args:
        X: pandas.DataFrame
            Le DataFrame contenant les caractéristiques.
        y: pandas.Series
            La série représentant la variable cible.
        test_size: float, optional
            La proportion de l'ensemble de données à inclure dans l'ensemble de
            test. La valeur par défaut est 0.2.

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]
        Un tuple contenant quatre éléments
        X_train: pandas.DataFrame
        Le DataFrame des caractéristiques pour l'ensemble d'entraînement.
        X_test: pandas.DataFrame
        Le DataFrame des caractéristiques pour l'ensemble de test.
        y_train: pandas.Series
        La série représentant la variable cible pour l'ensemble
        d'entraînement.
        y_test: pandas.Series
        La série représentant la variable cible pour l'ensemble de test.
    """
    logger.info("Splitting data in train and test ...")
    x_train, x_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=42,
    )
    return x_train, x_test, y_train, y_test


def train_model(
    x_train: pd.DataFrame,
    y_train: pd.Series,
) -> BaseEstimator:
    """Entraîne un modèle de classification avec les données fournies.

    Args:
        x_train: pandas.DataFrame, Le DataFrame contenant les caractéristiques.
        y_train: pandas.Series, La série représentant la variable cible.

    Returns:
        BaseEstimator: Le modèle de classification entraîné.
    """
    logger.info("Training model and tunning hyperparams ...")
    rf_classifier = RandomForestRegressor()
    grid_space = {"n_estimators": [100, 200, 300], "max_depth": [3, 6, 9, 12]}
    logger.debug(f"Grid Space is {grid_space}  ...")
    grid = GridSearchCV(
        rf_classifier,
        param_grid=grid_space,
        cv=5,
        scoring="r2",
        n_jobs=-1,
    )
    model_grid = grid.fit(x_train, y_train)
    return model_grid.best_estimator_


def evaluate_model(
    model: BaseEstimator,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> float:
    """Évalue les performances d'un modèle sur un ensemble de test.

    Args:
        model: BaseEstimator
        X_test: pandas.DataFrame
        y_test: pandas.Series

    Returns:
        float, Le score de performance du modèle sur l'ensemble de test.
    """
    score = model.score(X_test, y_test)
    logger.info(f"Evaluating Model, Score is {score:.2f}")
    return score


def save_model(model):
    """Sauvegarde le modèle à la fois en format joblib.

    Dans le repertoire MODELS_DIR.

    Args:
        model: object
            Le modèle à sauvegarder. Il doit être sérialisable.

    Notes
    -----
    Cette fonction utilise les variables globales model_name et version pour
    générer les noms de fichiers. Assurez-vous que ces variables sont définies
    correctement avant d'appeler cette fonction.
    """
    joblib_model = f"{model_settings.models_name}_V_{model_settings.version}"
    extension = ".joblib"
    joblib_model += extension
    persist_path = os.path.join(model_settings.models_path, joblib_model)
    logger.info(f"Saving Model at {persist_path}")
    # Sauvegarde en format joblib
    with open(persist_path, "wb") as fichier:
        joblib.dump(model, fichier)
