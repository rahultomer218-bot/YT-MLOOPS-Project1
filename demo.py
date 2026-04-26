import sys
import pandas as pd
from src.logger import logging
from src.exception import CustomException
from src.pipeline.training_pipeline import TrainingPipeline

try:
    df = pd.read_csv("notebook/data.csv")
    print(df.head())
except Exception as e:
    raise CustomException(e, sys)

try:
    logging.info("Training Pipeline shuru ho rahi hai...")
    pipeline = TrainingPipeline()
    pipeline.run_pipeline()
    logging.info("Training Pipeline successfully complete hui!")
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    raise