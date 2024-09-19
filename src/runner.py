from model_service import ModelService
from loguru import logger

@logger.catch
def main():
    
    logger.info("Starting the prediction process, running  the application ...")
    
    ml_svc = ModelService()
    # Load Model
    ml_svc.load_model()
    pred = ml_svc.predict([85, 2015, 2, 20, 1, 1, 0, 0, 1])

    logger.info(f"Prediction is: {pred[0]:.2f} ...")
    
    
if __name__ == '__main__':
    
    main()