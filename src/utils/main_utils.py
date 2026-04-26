import os
import sys
import pickle
import yaml
import numpy as np

from src.logger import logging
from src.exception import MyException


# ============================================================
# 1. Object Save karo (Model ya Preprocessor)
# ============================================================
def save_object(file_path: str, obj: object) -> None:
    """
    Koi bhi Python object ko pickle file mein save karta hai.
    Model aur Preprocessor save karne ke liye use hota hai.
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as f:
            pickle.dump(obj, f)
        logging.info(f"Object save hua: {file_path} ✅")
    except Exception as e:
        raise MyException(e, sys)


# ============================================================
# 2. Object Load karo (Model ya Preprocessor)
# ============================================================
def load_object(file_path: str) -> object:
    """
    Pickle file se object load karta hai.
    Saved model ko load karne ke liye use hota hai.
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File nahi mili: {file_path}")
        with open(file_path, "rb") as f:
            obj = pickle.load(f)
        logging.info(f"Object load hua: {file_path} ✅")
        return obj
    except Exception as e:
        raise MyException(e, sys)


# ============================================================
# 3. Numpy Array Save karo
# ============================================================
def save_numpy_array(file_path: str, array: np.ndarray) -> None:
    """
    Numpy array ko .npy file mein save karta hai.
    Transformed data save karne ke liye use hota hai.
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as f:
            np.save(f, array)
        logging.info(f"Numpy array save hua: {file_path} ✅")
    except Exception as e:
        raise MyException(e, sys)


# ============================================================
# 4. Numpy Array Load karo
# ============================================================
def load_numpy_array(file_path: str) -> np.ndarray:
    """
    .npy file se numpy array load karta hai.
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File nahi mili: {file_path}")
        with open(file_path, "rb") as f:
            array = np.load(f, allow_pickle=True)
        logging.info(f"Numpy array load hua: {file_path} ✅")
        return array
    except Exception as e:
        raise MyException(e, sys)


# ============================================================
# 5. YAML file read karo
# ============================================================
def read_yaml_file(file_path: str) -> dict:
    """
    YAML file ko read karke dictionary return karta hai.
    Config files padhne ke liye use hota hai.
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"YAML file nahi mili: {file_path}")
        with open(file_path, "r") as f:
            data = yaml.safe_load(f)
        logging.info(f"YAML file read hui: {file_path} ✅")
        return data
    except Exception as e:
        raise MyException(e, sys)


# ============================================================
# 6. YAML file write karo
# ============================================================
def write_yaml_file(file_path: str, data: dict) -> None:
    """
    Dictionary ko YAML file mein save karta hai.
    Validation report save karne ke liye use hota hai.
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            yaml.dump(data, f, default_flow_style=False)
        logging.info(f"YAML file save hui: {file_path} ✅")
    except Exception as e:
        raise MyException(e, sys)