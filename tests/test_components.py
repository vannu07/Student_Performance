import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.student_performance.components.data_ingestion import DataIngestion
from src.student_performance.components.data_transformation import DataTransformation
from src.student_performance.components.model_trainer import ModelTrainer
from src.student_performance.entity.config_entity import (
    DataIngestionConfig,
    DataTransformationConfig,
    ModelTrainerConfig
)

class TestDataIngestion:
    def test_data_ingestion_config(self):
        config = DataIngestionConfig(
            root_dir=Path("test_artifacts/data_ingestion"),
            source_URL="https://example.com/data.csv",
            local_data_file=Path("test_artifacts/data_ingestion/data.csv"),
            unzip_dir=Path("test_artifacts/data_ingestion")
        )
        
        assert config.root_dir == Path("test_artifacts/data_ingestion")
        assert config.source_URL == "https://example.com/data.csv"

class TestDataTransformation:
    def test_data_transformer_object(self):
        config = DataTransformationConfig(
            root_dir=Path("test_artifacts/data_transformation"),
            data_path=Path("test_data.csv"),
            preprocessor_obj_file_path=Path("test_preprocessor.pkl")
        )
        
        data_transformation = DataTransformation(config)
        preprocessor = data_transformation.get_data_transformer_object()
        
        assert preprocessor is not None
        assert hasattr(preprocessor, 'fit_transform')

class TestModelTrainer:
    def test_model_trainer_initialization(self):
        config = ModelTrainerConfig(
            root_dir=Path("test_artifacts/model_trainer"),
            train_data_path=Path("train.csv"),
            test_data_path=Path("test.csv"),
            model_name="test_model.pkl",
            target_column="math_score",
            expected_accuracy=0.6,
            model_config={}
        )
        
        model_trainer = ModelTrainer(config)
        assert model_trainer.config == config

if __name__ == "__main__":
    pytest.main([__file__])
