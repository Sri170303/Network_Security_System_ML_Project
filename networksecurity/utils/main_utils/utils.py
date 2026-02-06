import yaml
from networksecurity.exception.exceptions import NetworkSecurityError
from networksecurity.logging.logger import logging
import os, sys
import numpy as np
import pickle
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score


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
    

def load_object(file_path:str) -> object:
    try:
        if not file_path:
            raise Exception(f"The file: {file_path} does not exists")
        with open(file_path, "rb") as file_obj:
            print(file_obj)
            return pickle.load(file_obj)
    except Exception as e:
        raise NetworkSecurityError(e, sys)


def load_numpy_array_data(file_path:str) -> np.array:
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise NetworkSecurityError(e, sys)
    

def evaluate_models(X_train, y_train, X_test, y_test, models, params):

    try:
        report = {}

        for model_name, model in models.items():

            param = params.get(model_name, {})

            gs = GridSearchCV(
                estimator=model,
                param_grid=param,
                cv=3,
                n_jobs=-1,
                verbose=1
            )

            # Train model
            gs.fit(X_train, y_train)

            # Get best trained model
            best_model = gs.best_estimator_

            # Replace untrained model with trained model
            models[model_name] = best_model

            # Predictions
            y_test_pred = best_model.predict(X_test)

            # Precision score (for classification)
            test_score = r2_score(y_test, y_test_pred)

            report[model_name] = test_score

        return report

    except Exception as e:
        raise NetworkSecurityError(e, sys)