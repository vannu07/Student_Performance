"""Minimal training runner that executes ingestion, transformation and model training
without requiring MLflow (useful for local/dev when mlflow isn't installed).

Run with:
  PYTHONPATH=$PWD python3 scripts/run_training_minimal.py
"""
import logging
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from src.student_performance.config.configuration import ConfigurationManager
from src.student_performance.components.data_ingestion import DataIngestion
from src.student_performance.components.data_transformation import DataTransformation
from src.student_performance.components.model_trainer import ModelTrainer


def main():
    try:
        config = ConfigurationManager()

        # Data ingestion (skip if a CSV already exists at the expected data path)
        dt_conf = config.get_data_transformation_config()
        data_path = dt_conf.data_path
        if not data_path or not Path(data_path).exists():
            di_conf = config.get_data_ingestion_config()
            di = DataIngestion(config=di_conf)
            data_file = di.initiate_data_ingestion()
            logger.info(f"Data ingested to: {data_file}")
        else:
            logger.info(f"Using existing data file at: {data_path}")

        # Data transformation
        dt_conf = config.get_data_transformation_config()
        dt = DataTransformation(config=dt_conf)
        train_arr, test_arr, _ = dt.initiate_data_transformation_from_config()
        logger.info("Data transformation completed")

        # Model training
        mt_conf = config.get_model_trainer_config()
        mt = ModelTrainer(config=mt_conf)
        r2_score, best_model_name, model_report = mt.initiate_model_trainer(train_arr, test_arr)
        logger.info(f"Model training completed. Best model: {best_model_name}, R2: {r2_score}")

    except Exception as e:
        logger.exception(f"Training failed: {e}")


if __name__ == '__main__':
    main()
