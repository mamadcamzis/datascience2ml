import logging
from model_service import ModelService

logger = logging.getLogger(__name__)

def main():
    
    logging.basicConfig(level=logging.INFO)
    ml_svc = ModelService()
    # Load Model
    ml_svc.load_model()

    # Prediction

    pred = ml_svc.predict([85, 2015, 2, 20, 1, 1, 0, 0, 1])

    print(f"Prediction is: {pred}")
    
    
if __name__ == '__main__':
    
    main()