import os
import pandas as pd
from pydantic import FilePath
from config import settings

from loguru import logger


def load_data(path: FilePath = settings.DATA_FILE_NAME) -> pd.DataFrame:
    """
    Charge un fichier CSV à partir d'un chemin donné et le renvoie sous forme de DataFrame pandas.

    Paramètres:
    -----------
    path : FilePath, optionnel
        Le chemin vers le fichier CSV à charger. Par défaut, il utilise la variable `settings.DATA_FILE_NAME`.

    Retour:
    -------
    pandas.DataFrame
        Un DataFrame contenant les données du fichier CSV.

    Exemple:
    --------
    >>> df = load_data('data/raw/my_data.csv')
    >>> print(df.head())
    """
    csv_path = os.path.join(settings.DATA_PATH, path)
    logger.info(f"Loading csv file at {csv_path}")
    return pd.read_csv(csv_path)
