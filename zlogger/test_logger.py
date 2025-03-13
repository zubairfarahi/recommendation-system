from logger import get_logger
from custom_exception import CustomException
import sys
logger = get_logger(__name__)

logger.info("this is test only")


def sum(a, b):
    try:
        result = a/b
        logger.info(f'sum result is {result}')
    except Exception as e:
        logger.error(e)
        raise CustomException('Cusstom error',sys)
    
if __name__ == '__main__':
    try:
        sum(10, 0)
    except CustomException as e:
        logger.error(e)