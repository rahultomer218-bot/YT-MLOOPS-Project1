import sys
from src.logger import logging
from src.exception import MyException

from src.entity.config_entity import (
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    ModelTrainerConfig
)

from src.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    ModelTrainerArtifact
)

from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.model_trainer import ModelTrainer


class TrainingPipeline:
    """
    Poori ML Training Pipeline yahan orchestrate hoti hai.
    Har component ek ke baad ek chalega.
    """

    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()


    # ============================================================
    # STEP 1: Data Ingestion
    # ============================================================
    def start_data_ingestion(self) -> DataIngestionArtifact:
        """
        MongoDB se data fetch karke train/test mein split karta hai.
        """
        try:
            logging.info("========== Data Ingestion Shuru ==========")

            data_ingestion_config = DataIngestionConfig(
                training_pipeline_config=self.training_pipeline_config
            )

            data_ingestion = DataIngestion(
                data_ingestion_config=data_ingestion_config
            )

            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

            logging.info(f"Data Ingestion Artifact: {data_ingestion_artifact}")
            logging.info("========== Data Ingestion Complete ==========")

            return data_ingestion_artifact

        except Exception as e:
            raise MyException(e, sys)


    # ============================================================
    # STEP 2: Data Validation
    # ============================================================
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        """
        Data ko validate karta hai — missing values, schema check, etc.
        """
        try:
            logging.info("========== Data Validation Shuru ==========")

            data_validation_config = DataValidationConfig(
                training_pipeline_config=self.training_pipeline_config
            )

            data_validation = DataValidation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_config=data_validation_config
            )

            data_validation_artifact = data_validation.initiate_data_validation()

            logging.info(f"Data Validation Artifact: {data_validation_artifact}")
            logging.info("========== Data Validation Complete ==========")

            return data_validation_artifact

        except Exception as e:
            raise MyException(e, sys)


    # ============================================================
    # STEP 3: Model Trainer
    # ============================================================
    def start_model_trainer(self, data_validation_artifact: DataValidationArtifact) -> ModelTrainerArtifact:
        """
        Model train karta hai aur artifacts save karta hai.
        """
        try:
            logging.info("========== Model Training Shuru ==========")

            model_trainer_config = ModelTrainerConfig(
                training_pipeline_config=self.training_pipeline_config
            )

            model_trainer = ModelTrainer(
                data_validation_artifact=data_validation_artifact,
                model_trainer_config=model_trainer_config
            )

            model_trainer_artifact = model_trainer.initiate_model_trainer()

            logging.info(f"Model Trainer Artifact: {model_trainer_artifact}")
            logging.info("========== Model Training Complete ==========")

            return model_trainer_artifact

        except Exception as e:
            raise MyException(e, sys)


    # ============================================================
    # MAIN: Poori Pipeline Chalao
    # ============================================================
    def run_pipeline(self) -> None:
        """
        Poori Training Pipeline ko sequentially chalata hai.
        Yeh method main.py se call hoga.
        """
        try:
            logging.info(">>>>>>>>>>> Training Pipeline Shuru <<<<<<<<<<<<")

            # Step 1: Data Ingestion
            data_ingestion_artifact = self.start_data_ingestion()

            # Step 2: Data Validation
            data_validation_artifact = self.start_data_validation(
                data_ingestion_artifact=data_ingestion_artifact
            )

            # Step 3: Model Trainer
            model_trainer_artifact = self.start_model_trainer(
                data_validation_artifact=data_validation_artifact
            )

            logging.info(">>>>>>>>>>> Training Pipeline Complete <<<<<<<<<<<<")

        except Exception as e:
            raise MyException(e, sys)