from src.student_performance import logger
from src.student_performance.pipeline.training_pipeline import CompleteTrainingPipeline

if __name__ == "__main__":
    try:
        logger.info(">>>>>> Starting Student Performance ML Training Pipeline <<<<<<")
        
        # Initialize and run the complete training pipeline
        pipeline = CompleteTrainingPipeline()
        results = pipeline.run_pipeline()
        
        logger.info(">>>>>> Training Pipeline Completed Successfully <<<<<<")
        logger.info(f"Final Results: {results}")
        
    except Exception as e:
        logger.error(f"Training pipeline failed: {str(e)}")
        raise e
