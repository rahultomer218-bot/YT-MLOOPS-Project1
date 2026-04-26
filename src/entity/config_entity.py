import os
from dataclasses import dataclass, field
from src.constants import (
    ARTIFACTS_DIR,
    DATA_INGESTION_DIR_NAME,
    DATA_INGESTION_INGESTED_DIR,
    DATA_INGESTION_RAW_DATA_DIR,
    DATA_VALIDATION_DIR_NAME,
    DATA_VALIDATION_REPORT_FILE_NAME,
    MODEL_TRAINER_DIR_NAME,
    MODEL_FILE_NAME,
    MODEL_CONFIG_FILE_PATH,
    TARGET_COLUMN,
    TIMESTAMP
)

# ============================================================
# 1. Training Pipeline Config
# ============================================================
@dataclass
class TrainingPipelineConfig:
    pipeline_name: str = "vehicle_pipeline"
    artifact_dir: str = os.path.join(ARTIFACTS_DIR, TIMESTAMP)


# ============================================================
# 2. Data Ingestion Config
# ============================================================
@dataclass
class DataIngestionConfig:
    training_pipeline_config: TrainingPipelineConfig = field(
        default_factory=TrainingPipelineConfig
    )
    data_ingestion_dir: str = field(init=False)
    raw_data_path: str = field(init=False)
    ingested_train_path: str = field(init=False)
    ingested_test_path: str = field(init=False)

    def __post_init__(self):
        self.data_ingestion_dir = os.path.join(
            self.training_pipeline_config.artifact_dir, DATA_INGESTION_DIR_NAME
        )
        self.raw_data_path = os.path.join(
            self.data_ingestion_dir, DATA_INGESTION_RAW_DATA_DIR, "vehicle_data.csv"
        )
        self.ingested_train_path = os.path.join(
            self.data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, "train.csv"
        )
        self.ingested_test_path = os.path.join(
            self.data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, "test.csv"
        )


# ============================================================
# 3. Data Validation Config
# ============================================================
@dataclass
class DataValidationConfig:
    training_pipeline_config: TrainingPipelineConfig = field(
        default_factory=TrainingPipelineConfig
    )
    data_validation_dir: str = field(init=False)
    validation_report_file_path: str = field(init=False)

    def __post_init__(self):
        self.data_validation_dir = os.path.join(
            self.training_pipeline_config.artifact_dir, DATA_VALIDATION_DIR_NAME
        )
        self.validation_report_file_path = os.path.join(
            self.data_validation_dir, DATA_VALIDATION_REPORT_FILE_NAME
        )


# ============================================================
# 4. Model Trainer Config
# ============================================================
@dataclass
class ModelTrainerConfig:
    training_pipeline_config: TrainingPipelineConfig = field(
        default_factory=TrainingPipelineConfig
    )
    model_trainer_dir: str = field(init=False)
    trained_model_path: str = field(init=False)
    model_config_file_path: str = MODEL_CONFIG_FILE_PATH
    target_column: str = TARGET_COLUMN

    def __post_init__(self):
        self.model_trainer_dir = os.path.join(
            self.training_pipeline_config.artifact_dir, MODEL_TRAINER_DIR_NAME
        )
        self.trained_model_path = os.path.join(
            self.model_trainer_dir, MODEL_FILE_NAME
        )