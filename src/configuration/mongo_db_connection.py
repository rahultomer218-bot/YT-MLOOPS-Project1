import pymongo
import os
import sys
from src.constants import DATABASE_NAME  # Constant file se DB naam liya
from src.exception import VehicleException
from src.logger import logger

class MongoDBClient:
    """
    Class Name: MongoDBClient
    Description: Yeh class MongoDB database ke saath connection establish karti hai.
    """
    client = None

    def __init__(self, database_name=DATABASE_NAME) -> None:
        try:
            
            if MongoDBClient.client is None:
                # Environment variable se Mongo URL uthayein (Security ke liye)
                mongo_db_url = os.getenv("MONGODB_URL")
                
                if mongo_db_url is None:
                    raise Exception("Environment variable 'MONGODB_URL' set nahi hai.")
                
                # Connection establish karna
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url)
            
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
            
            logger.info(f"MongoDB connection safaltapurvak ban gaya hai: {database_name}")
            
        except Exception as e:
            # Hamare custom exception mein error bhejein
            raise VehicleException(e, sys)