import os
import sys
import shutil

from src.logger import logging
from src.exception import MyException
from src.entity.artifact_entity import ModelTrainerArtifact


class ModelPusher:
    """
    Trained model ko production folder mein push karta hai.
    Taaki Flask/FastAPI app isse use kar sake prediction ke liye.
    """

    def __init__(
        self,
        model_trainer_artifact: ModelTrainerArtifact,
        production_model_path: str = os.path.join("saved_models", "vehicle_model.pkl")
    ):
        try:
            self.model_trainer_artifact = model_trainer_artifact
            self.production_model_path = production_model_path
        except Exception as e:
            raise MyException(e, sys)


    # ============================================================
    # STEP 1: Production folder banao
    # ============================================================
    def create_production_folder(self) -> None:
        try:
            production_dir = os.path.dirname(self.production_model_path)
            os.makedirs(production_dir, exist_ok=True)
            logging.info(f"Production folder ready: {production_dir} ✅")
        except Exception as e:
            raise MyException(e, sys)


    # ============================================================
    # STEP 2: Model copy karo artifacts se production mein
    # ============================================================
    def push_model(self) -> str:
        try:
            trained_model_path = self.model_trainer_artifact.trained_model_file_path

            # Check karo ki trained model exist karta hai
            if not os.path.exists(trained_model_path):
                raise FileNotFoundError(
                    f"Trained model nahi mila: {trained_model_path}"
                )

            # Production folder mein copy karo
            shutil.copy(trained_model_path, self.production_model_path)

            logging.info(
                f"Model push hua:"
                f"\n  From : {trained_model_path}"
                f"\n  To   : {self.production_model_path} ✅"
            )

            return self.production_model_path

        except Exception as e:
            raise MyException(e, sys)


    # ============================================================
    # STEP 3: Backup rakho purana model ka
    # ============================================================
    def backup_existing_model(self) -> None:
        try:
            if os.path.exists(self.production_model_path):
                backup_path = self.production_model_path.replace(
                    ".pkl", "_backup.pkl"
                )
                shutil.copy(self.production_model_path, backup_path)
                logging.info(f"Purana model backup hua: {backup_path} ✅")
            else:
                logging.info("Koi purana model nahi mila — backup skip kiya")
        except Exception as e:
            raise MyException(e, sys)


    # ============================================================
    # MAIN: Model Pusher chalao
    # ============================================================
    def initiate_model_pusher(self) -> dict:
        try:
            logging.info("========== Model Pusher Shuru ==========")

            # Step 1: Production folder banao
            self.create_production_folder()

            # Step 2: Purane model ka backup lo
            self.backup_existing_model()

            # Step 3: Naya model push karo
            production_model_path = self.push_model()

            pusher_report = {
                "trained_model_path"   : self.model_trainer_artifact.trained_model_file_path,
                "production_model_path": production_model_path,
                "status"               : "Model successfully pushed ✅"
            }

            logging.info(f"Model Pusher Report: {pusher_report}")
            logging.info("========== Model Pusher Complete ==========")

            return pusher_report

        except Exception as e:
            raise MyException(e, sys)