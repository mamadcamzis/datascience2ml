

import joblib
import pandas as pd
from pathlib import Path
from paths import MODELS_DIR
from config import version, model_name
from model import build_model



class ModelService:
    
    def __init__(self) -> None:
        
        self.model = None
        self.model_name = model_name
    
    def load_model(self, model_name=None):
        
        if model_name:
            self.model_name = model_name
            
        joblib_model = self.model_name + '_v_' + version + '.joblib'
        model_path = Path(f"{MODELS_DIR}/{joblib_model}")  
        if not model_path.exists():
            build_model()
            
        self.model = joblib.load(model_path)
        
    def predict(self, input_parameters):
        
        if not isinstance(input_parameters, pd.DataFrame):
            input_parameters = pd.DataFrame([input_parameters], 
                                    columns=['area',  'constraction_year',  'bedrooms', 
                                            'garden', 'balcony_yes', 'parking_yes', 
                                            'furnished_yes', 'garage_yes', 'storage_yes'])
            
        return self.model.predict(input_parameters)
    
    
    


            