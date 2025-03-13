import os
import pandas as pd
import yaml
from zlogger.logger import get_logger
from zlogger.custom_exception import CustomException

logger = get_logger(__name__)


def read_ymal(file_path):
    try:

        if not os.path.exists(file_path):
            raise FileNotFoundError('file not found')
        
        with open(file_path) as ymal_file:
            config = yaml.safe_load(ymal_file)
            logger.info('Successfull read the yaml file')
            return config
    except Exception as e:
        logger.error("Error while reading yaml file")
        raise CustomException('Error while reading yaml file', e)


def load_data(path):
    try:
        logger.info('loading data')
        return pd.read_csv(path)
    except Exception as e:
        logger.error('error while reading the csv file')
        raise CustomException('error while reading the csv file', e)