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
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            yaml.dump(data, f, default_flow_style=False)
        logging.info(f"YAML file save hui: {file_path} ✅")
    except Exception as e:
        raise MyException(e, sys)