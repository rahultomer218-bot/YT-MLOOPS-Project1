import os
import sys
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

from src.logger import logging
from src.exception import MyException
from src.entity.config_entity import ModelTrainerConfig
from src.entity.artifact_entity import DataValidationArtifact, ModelTrainerArtifact
from src.utils.main_utils import save_object


class ModelTrainer:
    """
    Vehicle price predict karne ke liye model train karta hai.
    """

    def __init__(
        self,
        data_validation_artifact: DataValidationArtifact,
        model_trainer_config: ModelTrainerConfig
    ):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.model_trainer_config = model_trainer_config
        except Exception as e:
            raise MyException(e, sys)


    # ============================================================
    # STEP 1: Data load aur preprocess karo
    # ============================================================
    def load_and_prepare_data(self, file_path: str) -> tuple:
        try:
            df = pd.read_csv(file_path)

            # Target column alag karo
            target = self.model_trainer_config.target_column
            
            # Sirf numeric columns use karo
            df = df.select_dtypes(include=['number'])

            X = df.drop(columns=[target], errors='ignore')
            y = df[target]

            logging.info(f"Features: {X.shape}, Target: {y.shape}")
            return X, y

        except Exception as e:
            raise MyException(e, sys)


    # ============================================================
    # STEP 2: Model train karo
    # ============================================================
    def train_model(self, X_train, y_train):
        try:
            logging.info("RandomForestRegressor se model train ho raha hai...")

            model = RandomForestRegressor(
                n_estimators=100,
                random_state=42
            )
            model.fit(X_train, y_train)

            logging.info("Model training complete ✅")
            return model

        except Exception as e:
            raise MyException(e, sys)


    # ============================================================
    # STEP 3: Model evaluate karo
    # ============================================================
    def evaluate_model(self, model, X, y, dataset_name: str) -> dict:
        try:
            y_pred = model.predict(X)

            r2    = r2_score(y, y_pred)
            mae   = mean_absolute_error(y, y_pred)
            mse   = mean_squared_error(y, y_pred)

            metrics = {"r2_score": r2, "mae": mae, "mse": mse}

            logging.info(f"{dataset_name} Metrics → R2: {r2:.4f} | MAE: {mae:.2f} | MSE: {mse:.2f}")
            return metrics

        except Exception as e:
            raise MyException(e, sys)


    # ============================================================
    # MAIN: Model Trainer chalao
    # ============================================================
    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            logging.info("========== Model Training Shuru ==========")

            # Train aur Test data load karo
            train_path = self.data_validation_artifact.validation_report_file_path
            train_path = train_path.replace("data_validation", "data_ingestion")
            train_path = train_path.replace("report.yaml", "ingested/train.csv")
            test_path  = train_path.replace("train.csv", "test.csv")

            X_train, y_train = self.load_and_prepare_data(train_path)
            X_test,  y_test  = self.load_and_prepare_data(test_path)

            # Model train karo
            model = self.train_model(X_train, y_train)

            # Metrics nikalo
            train_metrics = self.evaluate_model(model, X_train, y_train, "Train")
            test_metrics  = self.evaluate_model(model, X_test,  y_test,  "Test")

            # Model save karo
            os.makedirs(self.model_trainer_config.model_trainer_dir, exist_ok=True)
            save_object(self.model_trainer_config.trained_model_path, model)
            logging.info(f"Model save hua: {self.model_trainer_config.trained_model_path}")

            # Artifact banao
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_path,
                train_metric_artifact=train_metrics,
                test_metric_artifact=test_metrics
            )

            logging.info(f"Model Trainer Artifact: {model_trainer_artifact}")
            logging.info("========== Model Training Complete ==========")

            return model_trainer_artifact

        except Exception as e:
            raise MyException(e, sys)