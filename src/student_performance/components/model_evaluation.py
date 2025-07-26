import os
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from urllib.parse import urlparse
import mlflow
import mlflow.sklearn
import joblib

from src.student_performance import logger
from src.student_performance.utils.common import save_json, load_json, load_bin
from src.student_performance.entity.config_entity import ModelEvaluationConfig

class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def eval_metrics(self, actual, pred):
        """
        Calculate evaluation metrics
        """
        rmse = np.sqrt(mean_squared_error(actual, pred))
        mae = mean_absolute_error(actual, pred)
        r2 = r2_score(actual, pred)
        return rmse, mae, r2

    def log_into_mlflow(self):
        """
        Log model metrics and artifacts into MLflow
        """
        try:
            test_data = pd.read_csv(self.config.test_data_path)
            model = joblib.load(self.config.model_path)

            test_x = test_data.drop([self.config.target_column], axis=1)
            test_y = test_data[[self.config.target_column]]

            mlflow.set_registry_uri(self.config.mlflow_uri)
            tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

            with mlflow.start_run():
                predicted_qualities = model.predict(test_x)
                (rmse, mae, r2) = self.eval_metrics(test_y, predicted_qualities)
                
                # Saving metrics as local
                scores = {"rmse": rmse, "mae": mae, "r2": r2}
                save_json(path=Path(self.config.metric_file_name), data=scores)

                mlflow.log_params(self.config.all_params)
                mlflow.log_metric("rmse", rmse)
                mlflow.log_metric("mae", mae)
                mlflow.log_metric("r2", r2)

                # Model registry does not work with file store
                if tracking_url_type_store != "file":
                    # Register the model
                    mlflow.sklearn.log_model(model, "model", registered_model_name="StudentPerformanceModel")
                else:
                    mlflow.sklearn.log_model(model, "model")

                logger.info(f"Model evaluation completed - RMSE: {rmse}, MAE: {mae}, R2: {r2}")

        except Exception as e:
            logger.error(f"Error in MLflow logging: {str(e)}")
            raise e

    def evaluate_model(self):
        """
        Evaluate model performance and save metrics
        """
        try:
            # Load test data and model
            test_data = pd.read_csv(self.config.test_data_path)
            model = load_bin(self.config.model_path)

            # Prepare test data
            test_x = test_data.drop([self.config.target_column], axis=1)
            test_y = test_data[[self.config.target_column]]

            # Make predictions
            predicted_qualities = model.predict(test_x)

            # Calculate metrics
            rmse, mae, r2 = self.eval_metrics(test_y, predicted_qualities)

            # Save metrics
            scores = {"rmse": rmse, "mae": mae, "r2": r2}
            save_json(path=Path(self.config.metric_file_name), data=scores)

            logger.info(f"Model evaluation completed:")
            logger.info(f"RMSE: {rmse}")
            logger.info(f"MAE: {mae}")
            logger.info(f"R2 Score: {r2}")

            return scores

        except Exception as e:
            logger.error(f"Error in model evaluation: {str(e)}")
            raise e

    def compare_models(self, model_results):
        """
        Compare multiple models and select the best one
        """
        try:
            logger.info("Comparing model performance...")
            
            best_model = max(model_results, key=model_results.get)
            best_score = model_results[best_model]
            
            logger.info(f"Best performing model: {best_model}")
            logger.info(f"Best R2 Score: {best_score}")
            
            # Save model comparison results
            comparison_results = {
                "best_model": best_model,
                "best_score": best_score,
                "all_models": model_results
            }
            
            comparison_path = os.path.join(self.config.root_dir, "model_comparison.json")
            save_json(path=Path(comparison_path), data=comparison_results)
            
            return best_model, best_score
            
        except Exception as e:
            logger.error(f"Error in model comparison: {str(e)}")
            raise e

    def generate_evaluation_report(self):
        """
        Generate comprehensive evaluation report
        """
        try:
            # Load metrics
            metrics = load_json(Path(self.config.metric_file_name))
            
            # Create evaluation report
            report = {
                "model_performance": {
                    "rmse": metrics.rmse,
                    "mae": metrics.mae,
                    "r2_score": metrics.r2
                },
                "model_path": str(self.config.model_path),
                "test_data_path": str(self.config.test_data_path),
                "evaluation_date": pd.Timestamp.now().isoformat(),
                "target_column": self.config.target_column
            }
            
            # Save evaluation report
            report_path = os.path.join(self.config.root_dir, "evaluation_report.json")
            save_json(path=Path(report_path), data=report)
            
            logger.info("Evaluation report generated successfully")
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating evaluation report: {str(e)}")
            raise e
