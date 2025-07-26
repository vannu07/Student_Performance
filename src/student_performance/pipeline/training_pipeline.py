import os
import sys
from src.student_performance import logger
from src.student_performance.config.configuration import ConfigurationManager
from src.student_performance.components.data_ingestion import DataIngestion
from src.student_performance.components.data_transformation import DataTransformation
from src.student_performance.components.model_trainer import ModelTrainer
from src.student_performance.components.model_evaluation import ModelEvaluation

STAGE_NAME = "Data Ingestion stage"

class DataIngestionTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            config = ConfigurationManager()
            data_ingestion_config = config.get_data_ingestion_config()
            data_ingestion = DataIngestion(config=data_ingestion_config)
            data_ingestion.initiate_data_ingestion()
        except Exception as e:
            logger.error(f"Error in {STAGE_NAME}: {str(e)}")
            raise e

STAGE_NAME = "Data Transformation stage"

class DataTransformationTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            config = ConfigurationManager()
            data_transformation_config = config.get_data_transformation_config()
            data_transformation = DataTransformation(config=data_transformation_config)
            train_arr, test_arr, _ = data_transformation.initiate_data_transformation_from_config()
            return train_arr, test_arr
        except Exception as e:
            logger.error(f"Error in {STAGE_NAME}: {str(e)}")
            raise e

STAGE_NAME = "Model Trainer stage"

class ModelTrainerTrainingPipeline:
    def __init__(self):
        pass

    def main(self, train_arr, test_arr):
        try:
            config = ConfigurationManager()
            model_trainer_config = config.get_model_trainer_config()
            model_trainer = ModelTrainer(config=model_trainer_config)
            r2_score, best_model_name, model_report = model_trainer.initiate_model_trainer(train_arr, test_arr)
            return r2_score, best_model_name, model_report
        except Exception as e:
            logger.error(f"Error in {STAGE_NAME}: {str(e)}")
            raise e

STAGE_NAME = "Model Evaluation stage"

class ModelEvaluationTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            config = ConfigurationManager()
            model_evaluation_config = config.get_model_evaluation_config()
            model_evaluation = ModelEvaluation(config=model_evaluation_config)
            model_evaluation.log_into_mlflow()
        except Exception as e:
            logger.error(f"Error in {STAGE_NAME}: {str(e)}")
            raise e

class CompleteTrainingPipeline:
    def __init__(self):
        pass

    def run_pipeline(self):
        """
        Run the complete training pipeline
        """
        try:
            logger.info("Starting complete training pipeline")
            
            # Stage 1: Data Ingestion
            logger.info(f">>>>>> stage {DataIngestionTrainingPipeline.__name__} started <<<<<<")
            data_ingestion_pipeline = DataIngestionTrainingPipeline()
            data_ingestion_pipeline.main()
            logger.info(f">>>>>> stage {DataIngestionTrainingPipeline.__name__} completed <<<<<<\n\nx==========x")

            # Stage 2: Data Transformation
            logger.info(f">>>>>> stage {DataTransformationTrainingPipeline.__name__} started <<<<<<")
            data_transformation_pipeline = DataTransformationTrainingPipeline()
            train_arr, test_arr = data_transformation_pipeline.main()
            logger.info(f">>>>>> stage {DataTransformationTrainingPipeline.__name__} completed <<<<<<\n\nx==========x")

            # Stage 3: Model Training
            logger.info(f">>>>>> stage {ModelTrainerTrainingPipeline.__name__} started <<<<<<")
            model_trainer_pipeline = ModelTrainerTrainingPipeline()
            r2_score, best_model_name, model_report = model_trainer_pipeline.main(train_arr, test_arr)
            logger.info(f">>>>>> stage {ModelTrainerTrainingPipeline.__name__} completed <<<<<<\n\nx==========x")

            # Stage 4: Model Evaluation
            logger.info(f">>>>>> stage {ModelEvaluationTrainingPipeline.__name__} started <<<<<<")
            model_evaluation_pipeline = ModelEvaluationTrainingPipeline()
            model_evaluation_pipeline.main()
            logger.info(f">>>>>> stage {ModelEvaluationTrainingPipeline.__name__} completed <<<<<<\n\nx==========x")

            logger.info("Complete training pipeline finished successfully")
            logger.info(f"Best model: {best_model_name} with R2 score: {r2_score}")
            
            return {
                "best_model": best_model_name,
                "r2_score": r2_score,
                "model_report": model_report
            }

        except Exception as e:
            logger.error(f"Error in complete training pipeline: {str(e)}")
            raise e

if __name__ == '__main__':
    try:
        pipeline = CompleteTrainingPipeline()
        results = pipeline.run_pipeline()
        logger.info(f"Pipeline completed with results: {results}")
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        raise e
