import os
from dataclasses import dataclass


# ============================================================
# 1. Data Ingestion Artifact
# ============================================================
@dataclass
class DataIngestionArtifact:
    """
    Data Ingestion complete hone ke baad
    train aur test file ki paths return karta hai.
    """
    trained_file_path: str
    test_file_path: str


# ============================================================
# 2. Data Validation Artifact
# ============================================================
@dataclass
class DataValidationArtifact:
    """
    Data Validation complete hone ke baad
    validation status aur report path return karta hai.
    """
    validation_status: bool
    message: str
    validation_report_file_path: str


# ============================================================
# 3. Model Trainer Artifact
# ============================================================
@dataclass
class ModelTrainerArtifact:
    """
    Model Training complete hone ke baad
    trained model ki path return karta hai.
    """
    trained_model_file_path: str
    train_metric_artifact: object
    test_metric_artifact: object