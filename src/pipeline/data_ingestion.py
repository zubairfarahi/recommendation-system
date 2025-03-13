import os
from zlogger.logger import get_logger
from zlogger.custom_exception import CustomException
import boto3
from config.paths import RAW_DIR
from dotenv import load_dotenv

logger = get_logger(__name__)

logger.info("Loading environment variables...")
load_dotenv()

class DataIgestion:

    def __init__(self):
        
        self.AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
        self.AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.AWS_REGION = os.getenv("AWS_REGION")
        self.S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
        self.S3_FOLDER_NAME = os.getenv("S3_FOLDER_NAME")
        self.RAW_DIR = RAW_DIR

        if not all([self.AWS_ACCESS_KEY_ID,
                    self.AWS_SECRET_ACCESS_KEY,
                    self.AWS_REGION,
                    self.S3_BUCKET_NAME,
                    self.S3_FOLDER_NAME ]):
                logger.error("Missing one or more required environment variables.")
                raise ValueError("Missing one or more required environment variables.")
        
        os.makedirs(self.RAW_DIR, exist_ok=True)
        logger.info("Environment variables loaded successfully.")
    
    def download_data_from_aws_s3(self):
        try:
            s3 = boto3.client(
                "s3",
                aws_access_key_id=self.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY,
                region_name=self.AWS_REGION,
            )
            logger.info("S3 client setup successful.")
        except Exception as e:
            logger.error(f"Error setting up S3 client: {str(e)}")
            raise CustomException("Error setting up S3 client", e) from e

        logger.info(f"Attempting to download files from {self.S3_FOLDER_NAME} in S3 bucket {self.S3_BUCKET_NAME}...")

        try:
            response = s3.list_objects_v2(Bucket=self.S3_BUCKET_NAME, Prefix=f"{self.S3_FOLDER_NAME}/")

            if "Contents" not in response:
                logger.warning(f"No files found in {self.S3_FOLDER_NAME} on S3.")
                return False  

            for obj in response["Contents"]:
                file_key = obj["Key"]
                if file_key.endswith(".csv"):
                    file_name = file_key.split("/")[-1]
                    file_path = os.path.join(self.RAW_DIR, file_name)

                    s3.download_file(self.S3_BUCKET_NAME, file_key, file_path)
                    logger.info(f"Downloaded: {file_name} -> {file_path}")

            logger.info(f"All CSV files successfully downloaded from {self.S3_FOLDER_NAME} in S3 bucket {self.S3_BUCKET_NAME}.")
            return True 

        except Exception as e:
            logger.error(f"Error downloading files from S3: {str(e)}")
            raise CustomException("Error downloading files from S3", e) from e  

    def run(self):
        logger.info(f"Setting up S3 client for region: {self.AWS_REGION}...")
        self.download_data_from_aws_s3()

         

