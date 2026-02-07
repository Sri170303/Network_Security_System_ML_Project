import os
import sys
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constants.training_pipeline import TARGET_COLUMN
from networksecurity.constants.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.entity.artifact_entity import DataTransformationArtifact, DataValidationArtifact

from networksecurity.exception.exceptions import NetworkSecurityError
from networksecurity.logging.logger import logging
from networksecurity.utils.main_utils.utils import save_numpy_array_data, save_obj



class DataTransformation:
    def __init__(self, data_validation_artifact:DataValidationArtifact, data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact:DataValidationArtifact = data_validation_artifact
            self.data_transformation_config:DataTransformationConfig = data_transformation_config
        except Exception as e:
            raise NetworkSecurityError(e, sys)

    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityError(e, sys)
        
    def get_data_transformer_object(cls) -> Pipeline:
        logging.info(
            "Starting object creating for KNN imputer"
        )
        try:
            imputer:KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info("Successfully created KNN imputer object with desired imputer params")
            processor: Pipeline = Pipeline([("imputer", imputer)])
            return processor
        except Exception as e:
            raise NetworkSecurityError(e, sys)

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        logging.info("Starting Data Transformation")
        try:
            print(DataValidationArtifact)
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            target_column_train_df = train_df[TARGET_COLUMN]
            target_column_train_df.replace(-1, 0, inplace=True)
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN])

            target_column_test_df = test_df[TARGET_COLUMN]
            target_column_test_df.replace(-1, 0, inplace=True)
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN])

            preprocessor = self.get_data_transformer_object()
            preprocessor_obj = preprocessor.fit(input_feature_train_df)
            transformed_train_features = preprocessor_obj.transform(input_feature_train_df)
            transformed_test_features = preprocessor_obj.transform(input_feature_test_df)

            train_arr = np.c_[transformed_train_features, np.array(target_column_train_df)]
            test_arr = np.c_[transformed_test_features, np.array(target_column_test_df)]

            save_numpy_array_data(self.data_transformation_config.data_transformed_train_file_path, array = train_arr)
            save_numpy_array_data(self.data_transformation_config.data_transformed_test_file_path, array= test_arr)
            save_obj(self.data_transformation_config.data_transformed_object_file_path, preprocessor_obj)

            save_obj("final_model/preprocessing.pkl", preprocessor_obj)

            data_transformation_artifacts = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.data_transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.data_transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.data_transformed_test_file_path
            )

            return data_transformation_artifacts
        except Exception as e:
            raise NetworkSecurityError(e, sys)
