import os
import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor
from catboost import CatBoostRegressor
from sklearn.ensemble import RandomForestRegressor

from src.student_performance import logger
from src.student_performance.utils.common import save_bin, evaluate_models
from src.student_performance.entity.config_entity import ModelTrainerConfig

class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def initiate_model_trainer(self, train_array, test_array):
        try:
            logger.info("Split training and test input data")
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1]
            )
            
            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "XGBRegressor": XGBRegressor(),
                "CatBoosting Regressor": CatBoostRegressor(verbose=False),
                "AdaBoost Regressor": AdaBoostRegressor(),
            }
            
            params = {
                "Decision Tree": {
                    'criterion': ['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                },
                "Random Forest": {
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                },
                "Gradient Boosting": {
                    'learning_rate': [.1, .01, .05, .001],
                    'subsample': [0.6, 0.7, 0.75, 0.8, 0.85, 0.9],
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                },
                "Linear Regression": {},
                "XGBRegressor": {
                    'learning_rate': [.1, .01, .05, .001],
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                },
                "CatBoosting Regressor": {
                    'depth': [6, 8, 10],
                    'learning_rate': [0.01, 0.05, 0.1],
                    'iterations': [30, 50, 100]
                },
                "AdaBoost Regressor": {
                    'learning_rate': [.1, .01, 0.5, .001],
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                }
            }

            model_report: dict = evaluate_models(X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test,
                                                 models=models, param=params)

            # Log all model scores for debugging
            logger.info("Model performance report:")
            for model_name, score in model_report.items():
                logger.info(f"{model_name}: {score}")

            # To get best model score from dict
            best_model_score = max(sorted(model_report.values()))

            # To get best model name from dict
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]

            logger.info(f"Expected accuracy threshold: {self.config.expected_accuracy}")
            logger.info(f"Best model score achieved: {best_model_score}")
            logger.info(f"Best model name: {best_model_name}")

            if best_model_score < self.config.expected_accuracy:
                logger.warning(f"No best model found with score > {self.config.expected_accuracy}")
                logger.info(f"Best model score achieved: {best_model_score}")
                raise Exception("No best model found")

            logger.info(f"Best found model on both training and testing dataset: {best_model_name}")
            logger.info(f"Best model score: {best_model_score}")

            # Save the best model
            model_path = os.path.join(self.config.root_dir, self.config.model_name)
            save_bin(best_model, model_path)

            predicted = best_model.predict(X_test)
            r2_square = r2_score(y_test, predicted)
            
            logger.info(f"R2 Score: {r2_square}")
            
            return r2_square, best_model_name, model_report

        except Exception as e:
            logger.error(f"Error in model training: {str(e)}")
            raise e

    def train_models_with_mlflow(self, train_array, test_array):
        """
        Train models with MLflow tracking
        """
        try:
            import mlflow
            import mlflow.sklearn
            from urllib.parse import urlparse
            
            logger.info("Starting model training with MLflow tracking")
            
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1]
            )
            
            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "XGBRegressor": XGBRegressor(),
                "CatBoosting Regressor": CatBoostRegressor(verbose=False),
                "AdaBoost Regressor": AdaBoostRegressor(),
            }
            
            best_model = None
            best_score = 0
            best_model_name = ""
            
            # Set MLflow experiment
            mlflow.set_experiment("Student Performance Prediction")
            
            for model_name, model in models.items():
                with mlflow.start_run(run_name=model_name):
                    # Train model
                    model.fit(X_train, y_train)
                    
                    # Make predictions
                    y_pred = model.predict(X_test)
                    
                    # Calculate metrics
                    r2 = r2_score(y_test, y_pred)
                    
                    # Log parameters and metrics
                    mlflow.log_params(model.get_params())
                    mlflow.log_metric("r2_score", r2)
                    
                    # Log model
                    mlflow.sklearn.log_model(model, model_name)
                    
                    logger.info(f"{model_name} - R2 Score: {r2}")
                    
                    if r2 > best_score:
                        best_score = r2
                        best_model = model
                        best_model_name = model_name
            
            # Save the best model
            model_path = os.path.join(self.config.root_dir, self.config.model_name)
            save_bin(best_model, model_path)
            
            logger.info(f"Best model: {best_model_name} with R2 Score: {best_score}")
            
            return best_score, best_model_name, best_model
            
        except Exception as e:
            logger.error(f"Error in MLflow model training: {str(e)}")
            raise e
