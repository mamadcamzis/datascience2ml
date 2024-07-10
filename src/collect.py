import os
import pandas as pd
from paths import DATA_DIR
from config import csv_filename

raw_data_path = os.path.join(DATA_DIR, csv_filename)

def load_data(path: str = raw_data_path) -> pd.DataFrame:
    """
    Charge un fichier CSV à partir d'un chemin donné et le renvoie sous forme de DataFrame pandas.

    Paramètres:
    -----------
    path : str, optionnel
        Le chemin vers le fichier CSV à charger. Par défaut, il utilise la variable `raw_data_path`.

    Retour:
    -------
    pandas.DataFrame
        Un DataFrame contenant les données du fichier CSV.

    Exemple:
    --------
    >>> df = load_data('data/raw/my_data.csv')
    >>> print(df.head())
    """
    return pd.read_csv(path)

# Test
#print(load_data().head())
