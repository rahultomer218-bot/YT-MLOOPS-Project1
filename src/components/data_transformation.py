import os
import sys
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OrdinalEncoder
from sklearn.compose import ColumnTransformer

from src.logger import logging
from src.exception import MyException
from src.entity.config_entity import DataValidationConfig
from src.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from src.constants import TARGET_COLUMN


class DataTransformation:
    """
    Raw data ko ML model ke liye ready karta hai.
    Numeric aur Categorical columns alag alag process karta hai.
    """

    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_artifact: DataValidationArtifact
    ):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
        except Exception as e:
            raise MyException(e, sys)


    # ============================================================
    # STEP 1: Data load karo
    # ============================================================
    def load_data(self, file_path: str) -> pd.DataFrame:
        try:
            df = pd.read_csv(file_path)
            logging.info(f"Data load hua: {file_path} → Shape: {df.shape}")
            return df
        except Exception as e:
            raise MyException(e, sys)


    # ============================================================
    # STEP 2: Preprocessing Pipeline banao
    # ============================================================
    def get_data_transformer(self, df: pd.DataFrame) -> ColumnTransformer:
        try:
            # Target column hata do
            df = df.drop(columns=[TARGET_COLUMN], errors='ignore')

            # Numeric aur Categorical columns alag karo
            numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

            logging.info(f"Numeric Columns: {numeric_cols}")
            logging.info(f"Categorical Columns: {categorical_cols}")

            # Numeric pipeline
            numeric_pipeline = Pipeline(steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler())
            ])

            # Categorical pipeline
            categorical_pipeline = Pipeline(steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("encoder", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1))
            ])

            # Column Transformer
            preprocessor = ColumnTransformer(transformers=[
                ("numeric", numeric_pipeline, numeric_cols),
                ("categorical", categorical_pipeline, categorical_cols)
            ])

            logging.info("Preprocessing pipeline ready ✅")
            return preprocessor

        except Exception as e:
            raise MyException(e, sys)


    # ============================================================
    # STEP 3: Transform karo
    # ============================================================
    def transform_data(
        self,
        preprocessor: ColumnTransformer,
        train_df: pd.DataFrame,
        test_df: pd.DataFrame
    ) -> tuple:
        try:
            # Features aur Target alag karo
            X_train = train_df.drop(columns=[TARGET_COLUMN], errors='ignore')
            y_train = train_df[TARGET_COLUMN]

            X_test = test_df.drop(columns=[TARGET_COLUMN], errors='ignore')
            y_test = test_df[TARGET_COLUMN]

            # Fit aur Transform
            X_train_transformed = preprocessor.fit_transform(X_train)
            X_test_transformed = preprocessor.transform(X_test)

            # Target ke saath combine karo
            train_arr = np.c_[X_train_transformed, np.array(y_train)]
            test_arr = np.c_[X_test_transformed, np.array(y_test)]

            logging.info(f"Train array shape: {train_arr.shape}")
            logging.info(f"Test array shape: {test_arr.shape}")

            return train_arr, test_arr, preprocessor

        except Exception as e:
            raise MyException(e, sys)


    # ============================================================
    # MAIN: Data Transformation chalao
    # ============================================================
    def initiate_data_transformation(self) -> tuple:
        try:
            logging.info("========== Data Transformation Shuru ==========")

            # Data load karo
            train_df = self.load_data(self.data_ingestion_artifact.trained_file_path)
            test_df  = self.load_data(self.data_ingestion_artifact.test_file_path)

            # Preprocessor banao
            preprocessor = self.get_data_transformer(train_df)

            # Transform karo
            train_arr, test_arr, fitted_preprocessor = self.transform_data(
                preprocessor, train_df, test_df
            )

            logging.info("========== Data Transformation Complete ==========")

            return train_arr, test_arr, fitted_preprocessor

        except Exception as e:
            raise MyException(e, sys)