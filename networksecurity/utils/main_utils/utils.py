import yaml
from networksecurity.exception.exceptions import NetworkSecurityError
from networksecurity.logging.logger import logging
import os, sys
import numpy as np
import pickle


def read_yaml_file(file_path:str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityError(e, sys)
    
def write_yaml_file(file_path:str, content:object, replace: bool = False)-> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
            os.makedirs(os.path.dirname(file_path), exists_ok=True)
            with open(file_path, "w") as file:
                yaml.dump(content, file)
    except Exception as e:
        raise(e, sys)
    
def save_numpy_array_data(file_path: str, array: np.array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise NetworkSecurityError(e, sys)
    
def save_obj(file_path: str, obj: object) -> None:
    try:
        logging.info(f"Trying to save object obj")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
        logging.info(f"Successfully saved obj")
    except Exception as e:
        raise NetworkSecurityError(e, sys)