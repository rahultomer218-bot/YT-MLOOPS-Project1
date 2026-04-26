import os
import sys
import pandas as pd
import numpy as np
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

from src.logger import logging
from src.exception import MyException
from src.entity.config_entity import ModelTrainerConfig
from src.entity.artifact_entity import ModelTrainerArtifact
from src.utils.main_utils import save_object


class ModelEvaluation:
    """
    Trained model ko evaluate karta hai.
    Train aur Test metrics compare karta hai —
    model overfit toh nahi hua?
    """

    def __init__(
        self,
        model_trainer_artifact: ModelTrainerArtifact,
        model_trainer_config: ModelTrainerConfig
    ):
        try:
            self.model_trainer_artifact = model_trainer_artifact
            self.model_trainer_config = model_trainer_config
        except Exception as e:
            raise MyException(e, sys)


    # ============================================================
    # STEP 1: Saved model load karo
    # ============================================================
    def load_model(self):
        try:
            model_path = self.model_trainer_artifact.trained_model_file_path
            model = load_object(model_path)
            logging.info(f"Model load hua: {model_path} ✅")
            return model
        except Exception as e:
            raise MyException(e, sys)


    # ============================================================
    # STEP 2: Data load karo
    # ============================================================
    def load_data(self, file_path: str) -> tuple:
        try:
            df = pd.read_csv(file_path)

            target = self.model_trainer_config.target_column

            # Sirf numeric columns use karo
            df = df.select_dtypes(include=['number'])

            X = df.drop(columns=[target], errors='ignore')
            y = df[target]

            logging.info(f"Data load hua: {file_path} → Shape: {df.shape}")
            return X, y

        except Exception as e:
            raise MyException(e, sys)


    # ============================================================
    # STEP 3: Metrics calculate karo
    # ============================================================
    def get_metrics(self, y_true, y_pred, dataset_name: str) -> dict:
        try:
            r2  = r2_score(y_true, y_pred)
            mae = mean_absolute_error(y_true, y_pred)
            mse = mean_squared_error(y_true, y_pred)
            rmse = np.sqrt(mse)

            metrics = {
                "r2_score"  : round(r2, 4),
                "mae"       : round(mae, 2),
                "mse"       : round(mse, 2),
                "rmse"      : round(rmse, 2)
            }

            logging.info(
                f"\n{'='*40}"
                f"\n📊 {dataset_name} Metrics:"
                f"\n  ✅ R2 Score : {r2:.4f}"
                f"\n  ✅ MAE      : {mae:.2f}"
                f"\n  ✅ MSE      : {mse:.2f}"
                f"\n  ✅ RMSE     : {rmse:.2f}"
                f"\n{'='*40}"
            )

            return metrics

        except Exception as e:
            raise MyException(e, sys)


    # ============================================================
    # STEP 4: Overfitting check karo
    # ============================================================
    def check_overfitting(self, train_r2: float, test_r2: float) -> str:
        try:
            diff = train_r2 - test_r2

            if diff > 0.15:
                status = "⚠️  Model OVERFIT hai — Train R2 bahut zyada hai Test se"
            elif test_r2 < 0.60:
                status = "❌ Model UNDERFIT hai — R2 Score bahut kam hai"
            else:
                status = "✅ Model theek hai — Overfitting nahi hai"

            logging.info(f"Overfitting Check: {status}")
            return status

        except Exception as e:
            raise MyException(e, sys)


    # ============================================================
    # MAIN: Model Evaluation chalao
    # ============================================================
    def initiate_model_evaluation(self, train_path: str, test_path: str) -> dict:
        try:
            logging.info("========== Model Evaluation Shuru ==========")

            # Model load karo
            model = self.load_model()

            # Data load karo
            X_train, y_train = self.load_data(train_path)
            X_test,  y_test  = self.load_data(test_path)

            # Predictions karo
            y_train_pred = model.predict(X_train)
            y_test_pred  = model.predict(X_test)

            # Metrics nikalo
            train_metrics = self.get_metrics(y_train, y_train_pred, "Train Data")
            test_metrics  = self.get_metrics(y_test,  y_test_pred,  "Test Data")

            # Overfitting check karo
            overfit_status = self.check_overfitting(
                train_r2=train_metrics["r2_score"],
                test_r2=test_metrics["r2_score"]
            )

            # Final report
            evaluation_report = {
                "train_metrics"   : train_metrics,
                "test_metrics"    : test_metrics,
                "overfitting_status": overfit_status
            }

            logging.info(f"Evaluation Report: {evaluation_report}")
            logging.info("========== Model Evaluation Complete ==========")

            return evaluation_report

        except Exception as e:
            raise MyException(e, sys)