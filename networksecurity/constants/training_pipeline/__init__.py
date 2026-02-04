import os
import sys
import numpy as np
import pandas as pd


TARGET_COLUMN:str = "Result"
PIPELINE_NAME:str = "NetworkSecurity"
ARTIFACT_DIR:str = "Artifacts"
FILE_NAME:str = "phisingData.csv"

TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"


SCHEMA_FILE_PATH = os.path.join("data_schema", "schema.yaml")

"""
DATA INGESTION CONSTANTS
"""
DATA_INGESTION_DIR:str = "data_ingestion"
DATA_INGESTION_DB:str = "NetworkDataDB"
DATA_INGESTION_COLLECTION:str = "NetworkData"
DATA_INGESTION_FEATURE_STORE_DIR:str = "feature_store"
DATA_INGESTION_INGESTED_DIR:str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float = 0.2

"""
DATA VALIDATION CONSTANTS
"""
DATA_VALIDATION_DIR:str = "data_validation"
DATA_VALIDATION_VALID_DIR:str = "valid"
DATA_VALIDATION_INVALID_DIR:str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR:str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE:str = "report.yaml"


"""
DATA TRANSFORMATION CONSTANTS
"""
DATA_TRANSFORMATION_DIR_NAME = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR = "transformed_object"

DATA_TRANSFORMATION_IMPUTER_PARAMS: dict = {
    "missing_values": np.nan,
    "n_neighbors": 3,
    "weights": "uniform"
}

PREPROCESSING_OBJECT_FILE_NAME:str = "preprocessing.pkl"


"""
MODEL TRAINER CONSTANTS
"""
MODEL_TRAINER_DIR_NAME:str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_NAME:str = "model.pkl"
MODEL_TRAINER_TRAINED_MODEL_DIR:str = "trained_model"
MODEL_TRAINER_EXPECTED_SCORE:float = 0.6
MODEL_TRAINER_FITTING_THRESHOLD:float = 0.05