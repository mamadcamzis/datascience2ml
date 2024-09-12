from loguru import logger

#logger.add("logs.log", rotation="11:40", compression="zip")
logger.catch
def divide_by(a, b):
    #logger.warning(f"b should not be zero")
    try:
        logger.warning(f"b should not be zero")
        result = a / b
        logger.info(f"a = {a}, b = {b}, a / b = {result}")
       
    except ZeroDivisionError:
        logger.critical("Divide by zero")
    #return result


#logger.info("Calculating a / b")
divide_by(1, 0)

