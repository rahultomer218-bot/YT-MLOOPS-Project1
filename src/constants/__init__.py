import os
from datetime import datetime

# 1. Project ki mukhya directory ka rasta (Root Directory)
ROOT_DIR = os.getcwd()

# 2. Artifacts (Output) folder ka setup
# Saara training data aur models isi folder mein jayenge
ARTIFACTS_DIR = "artifacts"

# 3. Data Ingestion se jude constants
DATA_INGESTION_DIR_NAME = "data_ingestion"
DATA_INGESTION_INGESTED_DIR = "ingested"
DATA_INGESTION_RAW_DATA_DIR = "raw"

# 4. Data Validation se jude constants
DATA_VALIDATION_DIR_NAME = "data_validation"
DATA_VALIDATION_REPORT_FILE_NAME = "report.yaml"

# 5. Model Training se jude constants
MODEL_TRAINER_DIR_NAME = "model_trainer"
MODEL_FILE_NAME = "vehicle_model.pkl" # Aapka trained model ka naam
MODEL_CONFIG_FILE_PATH = os.path.join("config", "model.yaml")

# 6. Database aur Dataset ke naam
DATABASE_NAME = "Proj1"
COLLECTION_NAME = "Proj1_data"
MONGO_DB_URL = "MONGODB_URL" # MongoDB ka URL, agar aap local pe use kar rahe hain

# 7. Common Constants
TARGET_COLUMN = "price" # Maan lijiye aap gaadi ki keemat predict kar rahe hain
PIPELINE_NAME = "vehicle_pipeline"

# 8. Timestamp (Folder naming ke liye)
TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")