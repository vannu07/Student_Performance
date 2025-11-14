import sys
import os
from dataclasses import dataclass
import numpy as np 
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.model_selection import train_test_split

from src.student_performance import logger
from src.student_performance.utils.common import save_bin
from src.student_performance.entity.config_entity import DataTransformationConfig

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path: str

class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config

    def get_data_transformer_object(self):
        '''
        This function is responsible for data transformation
        '''
        try:
            # Use features that are actually available in the dataset
            numerical_columns = [
                "absence_days",
                "weekly_self_study_hours", 
                "history_score",
                "physics_score",
                "chemistry_score",
                "biology_score",
                "english_score",
                "geography_score",
                "writing_score",
                "reading_score"
            ]
            categorical_columns = [
                "gender",
                "part_time_job",
                "extracurricular_activities",
                "career_aspiration",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]

            num_pipeline= Pipeline(
                steps=[
                ("imputer",SimpleImputer(strategy="median")),
                ("scaler",StandardScaler())

                ]
            )

            cat_pipeline=Pipeline(

                steps=[
                ("imputer",SimpleImputer(strategy="most_frequent")),
                ("one_hot_encoder",OneHotEncoder(handle_unknown='ignore')),
                ("scaler",StandardScaler(with_mean=False))
                ]

            )

            logger.info(f"Categorical columns: {categorical_columns}")
            logger.info(f"Numerical columns: {numerical_columns}")

            preprocessor=ColumnTransformer(
                [
                ("num_pipeline",num_pipeline,numerical_columns),
                ("cat_pipelines",cat_pipeline,categorical_columns)

                ]


            )

            return preprocessor
        
        except Exception as e:
            logger.error(f"Error in get_data_transformer_object: {str(e)}")
            raise e
    
    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logger.info("Read train and test data completed")

            logger.info("Obtaining preprocessing object")

            preprocessing_obj = self.get_data_transformer_object()

            target_column_name = "math_score"
            # Remove columns that shouldn't be used for prediction
            columns_to_drop = ["id", "first_name", "last_name", "email"]
            
            # Drop unnecessary columns from both train and test sets
            available_drop_cols = [col for col in columns_to_drop if col in train_df.columns]
            if available_drop_cols:
                train_df = train_df.drop(columns=available_drop_cols, axis=1)
                test_df = test_df.drop(columns=available_drop_cols, axis=1)

            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]

            logger.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logger.info(f"Saved preprocessing object.")

            save_bin(
                preprocessing_obj,
                self.config.preprocessor_obj_file_path,
            )

            return (
                train_arr,
                test_arr,
                self.config.preprocessor_obj_file_path,
            )
        except Exception as e:
            logger.error(f"Error in initiate_data_transformation: {str(e)}")
            raise e

    def initiate_data_transformation_from_config(self):
        """
        Transform data using the configuration
        """
        try:
            # Read the raw data
            df = pd.read_csv(self.config.data_path)
            logger.info("Read data completed")
            logger.info(f"Data shape: {df.shape}")

            # Split the data
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)
            
            # Save train and test sets
            train_path = os.path.join(self.config.root_dir, "train.csv")
            test_path = os.path.join(self.config.root_dir, "test.csv")
            
            train_set.to_csv(train_path, index=False, header=True)
            test_set.to_csv(test_path, index=False, header=True)
            
            logger.info("Train test split completed")

            # Apply transformation
            train_arr, test_arr, preprocessor_path = self.initiate_data_transformation(train_path, test_path)
            
            logger.info("Data transformation completed")
            
            return train_arr, test_arr, preprocessor_path
            
        except Exception as e:
            logger.error(f"Error in initiate_data_transformation_from_config: {str(e)}")
            raise e
