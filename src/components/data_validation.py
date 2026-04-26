import os
import sys
import pandas as pd
from src.logger import logging
from src.exception import MyException
from src.entity.config_entity import DataValidationConfig
from src.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact


class DataValidation:
    """
    Data ko validate karta hai — 
    missing columns, null values, aur data types check karta hai.
    """

    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_config: DataValidationConfig
    ):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
        except Exception as e:
            raise MyException(e, sys)


    # ============================================================
    # STEP 1: Train aur Test data load karo
    # ============================================================
    def load_data(self) -> tuple:
        try:
            train_df = pd.read_csv(self.data_ingestion_artifact.trained_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            logging.info(f"Train shape: {train_df.shape}, Test shape: {test_df.shape}")
            return train_df, test_df
        except Exception as e:
            raise MyException(e, sys)


    # ============================================================
    # STEP 2: Columns validate karo
    # ============================================================
    def validate_columns(self, df: pd.DataFrame, df_name: str) -> bool:
        try:
            required_columns = [
                "vehicle_id", "make", "model", "year", "type",
                "fuel_type", "transmission", "price"
            ]
            missing_columns = [col for col in required_columns if col not in df.columns]

            if missing_columns:
                logging.info(f"{df_name} mein yeh columns missing hain: {missing_columns}")
                return False

            logging.info(f"{df_name} ke saare required columns present hain ✅")
            return True
        except Exception as e:
            raise MyException(e, sys)


    # ============================================================
    # STEP 3: Null values check karo
    # ============================================================
    def validate_null_values(self, df: pd.DataFrame, df_name: str) -> bool:
        try:
            null_counts = df.isnull().sum()
            null_columns = null_counts[null_counts > 0]

            if len(null_columns) > 0:
                logging.info(f"{df_name} mein null values hain:\n{null_columns}")
            else:
                logging.info(f"{df_name} mein koi null values nahi hain ✅")

            return True
        except Exception as e:
            raise MyException(e, sys)


    # ============================================================
    # MAIN: Data Validation chalao
    # ============================================================
    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            logging.info("========== Data Validation Shuru ==========")

            # Data load karo
            train_df, test_df = self.load_data()

            # Columns validate karo
            train_col_status = self.validate_columns(train_df, "Train Data")
            test_col_status = self.validate_columns(test_df, "Test Data")

            # Null values check karo
            self.validate_null_values(train_df, "Train Data")
            self.validate_null_values(test_df, "Test Data")

            # Overall validation status
            validation_status = train_col_status and test_col_status

            # Report folder banao
            os.makedirs(
                os.path.dirname(self.data_validation_config.validation_report_file_path),
                exist_ok=True
            )

            # Report file likho
            with open(self.data_validation_config.validation_report_file_path, "w") as f:
                f.write(f"Validation Status: {validation_status}\n")
                f.write(f"Train Columns OK: {train_col_status}\n")
                f.write(f"Test Columns OK: {test_col_status}\n")

            # Artifact banao
            data_validation_artifact = DataValidationArtifact(
                validation_status=validation_status,
                message="Data Validation complete ho gayi!",
                validation_report_file_path=self.data_validation_config.validation_report_file_path
            )

            logging.info(f"Data Validation Artifact: {data_validation_artifact}")
            logging.info("========== Data Validation Complete ==========")

            return data_validation_artifact

        except Exception as e:
            raise MyException(e, sys)