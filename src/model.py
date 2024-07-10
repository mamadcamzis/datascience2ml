
import os
import pickle
import joblib
import pandas as pd 
from typing import List, Tuple
from sklearn.base import BaseEstimator
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from preparation import prepare_data
from paths import MODELS_DIR
from config import version, model_name


def build_model() -> None:
    """
    Construit, entraîne, évalue et sauvegarde un modèle de classification.

    Notes
    -----
    Cette fonction utilise les fonctions suivantes définies ailleurs :
    - prepare_data() : Prépare les données pour l'entraînement du modèle.
    - get_X_y(data) : Extrait les caractéristiques et la variable cible à partir des données.
    - split_train_test(X, y) : Divise les données en ensembles d'entraînement et de test.
    - train_model(X_train, y_train) : Entraîne le modèle avec les données d'entraînement.
    - evaluate_model(model, X_test, y_test) : Évalue les performances du modèle sur l'ensemble de test.
    - save_model(model) : Sauvegarde le modèle entraîné.

    """
    # Préparation des données
    data = prepare_data()

    # Extraction des caractéristiques et de la variable cible
    X, y = get_X_y(data)

    # Division en ensembles d'entraînement et de test
    X_train, X_test, y_train, y_test = split_train_test(X, y)

    # Entraînement du modèle
    rf_classifier = train_model(X_train, y_train)

    # Évaluation du modèle
    score = evaluate_model(rf_classifier, X_test, y_test)

    # Sauvegarde du modèle entraîné
    save_model(rf_classifier)

    # Affichage du score obtenu
    print(f"Score is: {score}")




def get_X_y(
    data: pd.DataFrame, 
    col_x: List[str] = ['area', 'constraction_year', 'bedrooms', 'garden', 
                        'balcony_yes', 'parking_yes', 'furnished_yes', 
                        'garage_yes', 'storage_yes'], 
    col_y: str = 'rent'
) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Extrait les caractéristiques (X) et la variable cible (y) d'un DataFrame.

    Parameters
    ----------
    data : pandas.DataFrame
        Le DataFrame contenant les données.
    col_x : List[str], optional
        La liste des colonnes à utiliser comme caractéristiques. 
        Les colonnes par défaut sont ['area', 'constraction_year', 
        'bedrooms', 'garden', 'balcony_yes', 'parking_yes', 
        'furnished_yes', 'garage_yes', 'storage_yes'].
    col_y : str, optional
        Le nom de la colonne à utiliser comme variable cible. 
        La colonne par défaut est 'rent'.

    Returns
    -------
    Tuple[pd.DataFrame, pd.Series]
        Un tuple contenant deux éléments :
        - X : pandas.DataFrame
            Le DataFrame des caractéristiques.
        - y : pandas.Series
            La série représentant la variable cible.
    """
    X = data[col_x]
    y = data[col_y]
    return X, y
    

def split_train_test(
    X: pd.DataFrame, 
    y: pd.Series, 
    test_size: float = 0.2
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Sépare les données en ensembles d'entraînement et de test.

    Parameters
    ----------
    X : pandas.DataFrame
        Le DataFrame contenant les caractéristiques.
    y : pandas.Series
        La série représentant la variable cible.
    test_size : float, optional
        La proportion de l'ensemble de données à inclure dans l'ensemble de test. 
        La valeur par défaut est 0.2.

    Returns
    -------
    Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]
        Un tuple contenant quatre éléments :
        - X_train : pandas.DataFrame
            Le DataFrame des caractéristiques pour l'ensemble d'entraînement.
        - X_test : pandas.DataFrame
            Le DataFrame des caractéristiques pour l'ensemble de test.
        - y_train : pandas.Series
            La série représentant la variable cible pour l'ensemble d'entraînement.
        - y_test : pandas.Series
            La série représentant la variable cible pour l'ensemble de test.
    """
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
    return X_train, X_test, y_train, y_test




def train_model(
    x_train: pd.DataFrame, 
    y_train: pd.Series
) -> BaseEstimator:
    """
    Entraîne un modèle de classification avec les données fournies.

    Parameters
    ----------
    x_train : pandas.DataFrame
        Le DataFrame contenant les caractéristiques.
    y_train : pandas.Series
        La série représentant la variable cible.


    Returns
    -------
    BaseEstimator
        Le modèle de classification entraîné.
    """
    rf_classifier = RandomForestRegressor()
    grid_space = {'n_estimators': [100, 200, 300], 'max_depth': [3, 6, 9, 12]}
    grid = GridSearchCV(rf_classifier, param_grid=grid_space, cv=5, scoring = 'r2')
    model_grid = grid.fit(x_train, y_train)
    
    return  model_grid.best_estimator_

    
def evaluate_model(
    model: BaseEstimator, 
    X_test: pd.DataFrame, 
    y_test: pd.Series
) -> float:
    """
    Évalue les performances d'un modèle sur un ensemble de test.

    Parameters
    ----------
    model : BaseEstimator
        Le modèle de classification entraîné.
    X_test : pandas.DataFrame
        Le DataFrame des caractéristiques pour l'ensemble de test.
    y_test : pandas.Series
        La série représentant la variable cible pour l'ensemble de test.

    Returns
    -------
    float
        Le score de performance du modèle sur l'ensemble de test.
    """
    score = model.score(X_test, y_test)
    return score


def save_model(model):
    """
    Sauvegarde le modèle à la fois en format pickle et joblib dans le répertoire MODELS_DIR.

    Parameters
    ----------
    model : object
        Le modèle à sauvegarder. Il doit être sérialisable.

    Notes
    -----
    Cette fonction utilise les variables globales model_name et version pour générer
    les noms de fichiers. Assurez-vous que ces variables sont définies correctement
    avant d'appeler cette fonction.
    """
    
    
    joblib_model = model_name + '_v_' + version + '.joblib'
    pickle_model = model_name + '_v_' + version + '.pkl'
    
    persist_dir_p = os.path.join(MODELS_DIR, pickle_model)
    persist_dir_j = os.path.join(MODELS_DIR, joblib_model)  
    
    # Sauvegarde en format pickle
    # with open(persist_dir_p, 'wb') as f:
    #     pickle.dump(model, f)
    
    # Sauvegarde en format joblib
    joblib.dump(model, persist_dir_j)


build_model()