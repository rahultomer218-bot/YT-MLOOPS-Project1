import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split

from src.logger import logging
from src.exception import MyException
from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
from src.data_access.proj1_data import Proj1Data
from src.constants import COLLECTION_NAME, DATABASE_NAME


class DataIngestion:
    """
    MongoDB se data fetch karke train aur test mein split karta hai.
    """

    def __init__(self, data_ingestion_config: DataIngestionConfig = DataIngestionConfig()):
        """
        DataIngestionConfig se saari paths lega.
        """
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise MyException(e, sys)


    # ============================================================
    # STEP 1: MongoDB se data fetch karke CSV mein save karo
    # ============================================================
    def export_data_into_feature_store(self) -> pd.DataFrame:
        """
        MongoDB se data fetch karta hai aur raw CSV file mein save karta hai.
        """
        try:
            logging.info("MongoDB se data fetch karna shuru...")

            # Proj1Data se data fetch karo
            proj1_data = Proj1Data()
            df = proj1_data.export_collection_as_dataframe(
                collection_name=COLLECTION_NAME,
                database_name=DATABASE_NAME
            )

            logging.info(f"Data fetch hua — Total Rows: {df.shape[0]}, Columns: {df.shape[1]}")

            # Raw data folder banao agar exist nahi karta
            feature_store_file_path = self.data_ingestion_config.raw_data_path
            os.makedirs(os.path.dirname(feature_store_file_path), exist_ok=True)

            # CSV mein save karo
            df.to_csv(feature_store_file_path, index=False)
            logging.info(f"Raw data save hua: {feature_store_file_path}")

            return df

        except Exception as e:
            raise MyException(e, sys)


    # ============================================================
    # STEP 2: Data ko Train aur Test mein split karo
    # ============================================================
    def split_data_as_train_test(self, df: pd.DataFrame) -> None:
        """
        DataFrame ko train aur test mein split karke save karta hai.
        """
        try:
            logging.info("Train-Test split shuru...")

            # 80% train, 20% test
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            logging.info(f"Train size: {train_set.shape[0]}, Test size: {test_set.shape[0]}")

            # Ingested folder banao
            ingested_dir = os.path.dirname(self.data_ingestion_config.ingested_train_path)
            os.makedirs(ingested_dir, exist_ok=True)

            # Train aur Test CSV save karo
            train_set.to_csv(self.data_ingestion_config.ingested_train_path, index=False)
            test_set.to_csv(self.data_ingestion_config.ingested_test_path, index=False)

            logging.info(f"Train data save hua: {self.data_ingestion_config.ingested_train_path}")
            logging.info(f"Test data save hua: {self.data_ingestion_config.ingested_test_path}")

        except Exception as e:
            raise MyException(e, sys)


    # ============================================================
    # STEP 3: Poora Data Ingestion Pipeline chalao
    # ============================================================
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Data Ingestion ka main method.
        Yeh method pipeline se call hoga.
        """
        try:
            logging.info("========== Data Ingestion Shuru ==========")

            # Step 1: MongoDB se data fetch karo
            df = self.export_data_into_feature_store()

            # Step 2: Train Test split karo
            self.split_data_as_train_test(df=df)

            # Step 3: Artifact banao aur return karo
            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.ingested_train_path,
                test_file_path=self.data_ingestion_config.ingested_test_path
            )

            logging.info(f"Data Ingestion Artifact: {data_ingestion_artifact}")
            logging.info("========== Data Ingestion Complete ==========")

            return data_ingestion_artifact

        except Exception as e:
            raise MyException(e, sys)