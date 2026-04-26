import pymongo
import pandas as pd
from src.configuration.mongo_db_connection import MongoDBClient
from src.constants import DATABASE_NAME, COLLECTION_NAME

class Proj1Data:
    """
    MongoDB se data fetch karne ke liye yeh class banai gayi hai.
    """
    def __init__(self):
        # MongoDB client se connection establish karo
        self.mongo_client = MongoDBClient()

    def export_collection_as_dataframe(self, collection_name: str, database_name: str = None) -> pd.DataFrame:
        """
        MongoDB collection ko pandas DataFrame mein convert karta hai.
        
        Parameters:
            collection_name (str): Jis collection se data lena hai
            database_name (str): Database ka naam (optional)
        
        Returns:
            pd.DataFrame: Data as DataFrame
        """
        try:
            # Agar database_name nahi diya toh default use karo
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client.client[database_name][collection_name]

            # MongoDB se data fetch karo aur DataFrame banao
            df = pd.DataFrame(list(collection.find()))

            # MongoDB ka default '_id' column hata do
            if "_id" in df.columns:
                df.drop(columns=["_id"], inplace=True)

            return df

        except Exception as e:
            raise Exception(f"Data fetch karne mein error aaya: {e}")