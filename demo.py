#!/usr/bin/env python3
"""
Student Performance ML Project - Complete Demonstration
This script demonstrates the complete end-to-end ML pipeline
"""

import os
import sys
import pandas as pd
from pathlib import Path

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.student_performance import logger
from src.student_performance.pipeline.training_pipeline import CompleteTrainingPipeline
from src.student_performance.pipeline.prediction_pipeline import PredictPipeline, CustomData

def demonstrate_training_pipeline():
    """
    Demonstrate the complete training pipeline
    """
    try:
        logger.info("="*60)
        logger.info("STUDENT PERFORMANCE ML PROJECT - TRAINING DEMO")
        logger.info("="*60)
        
        # Initialize and run the complete training pipeline
        pipeline = CompleteTrainingPipeline()
        results = pipeline.run_pipeline()
        
        logger.info("="*60)
        logger.info("TRAINING PIPELINE COMPLETED SUCCESSFULLY!")
        logger.info(f"Best Model: {results['best_model']}")
        logger.info(f"R2 Score: {results['r2_score']:.4f}")
        logger.info("="*60)
        
        return results
        
    except Exception as e:
        logger.error(f"Training pipeline demonstration failed: {str(e)}")
        return None

def demonstrate_prediction_pipeline():
    """
    Demonstrate the prediction pipeline with sample data
    """
    try:
        logger.info("="*60)
        logger.info("PREDICTION PIPELINE DEMONSTRATION")
        logger.info("="*60)
        
        # Sample student data for prediction
        sample_students = [
            {
                "gender": "female",
                "race_ethnicity": "group B",
                "parental_level_of_education": "bachelor's degree",
                "lunch": "standard",
                "test_preparation_course": "none",
                "reading_score": 72,
                "writing_score": 74
            },
            {
                "gender": "male",
                "race_ethnicity": "group C",
                "parental_level_of_education": "some college",
                "lunch": "standard",
                "test_preparation_course": "completed",
                "reading_score": 69,
                "writing_score": 88
            },
            {
                "gender": "female",
                "race_ethnicity": "group A",
                "parental_level_of_education": "master's degree",
                "lunch": "free/reduced",
                "test_preparation_course": "none",
                "reading_score": 90,
                "writing_score": 95
            }
        ]
        
        # Initialize prediction pipeline
        predict_pipeline = PredictPipeline()
        
        logger.info("Making predictions for sample students:")
        
        for i, student_data in enumerate(sample_students, 1):
            logger.info(f"\nStudent {i}:")
            logger.info(f"  Gender: {student_data['gender']}")
            logger.info(f"  Race/Ethnicity: {student_data['race_ethnicity']}")
            logger.info(f"  Parental Education: {student_data['parental_level_of_education']}")
            logger.info(f"  Lunch: {student_data['lunch']}")
            logger.info(f"  Test Prep: {student_data['test_preparation_course']}")
            logger.info(f"  Reading Score: {student_data['reading_score']}")
            logger.info(f"  Writing Score: {student_data['writing_score']}")
            
            # Create custom data object
            custom_data = CustomData(**student_data)
            
            # Get prediction
            pred_df = custom_data.get_data_as_data_frame()
            prediction = predict_pipeline.predict(pred_df)
            
            logger.info(f"  📊 PREDICTED MATH SCORE: {prediction[0]:.2f}")
            logger.info("-" * 50)
        
        logger.info("="*60)
        logger.info("PREDICTION PIPELINE DEMONSTRATION COMPLETED!")
        logger.info("="*60)
        
        return True
        
    except Exception as e:
        logger.error(f"Prediction pipeline demonstration failed: {str(e)}")
        return False

def show_project_structure():
    """
    Display the project structure
    """
    logger.info("="*60)
    logger.info("PROJECT STRUCTURE")
    logger.info("="*60)
    
    structure = """
    student_performance_ml_project/
    ├── 📁 artifacts/                  # Generated artifacts (models, data, etc.)
    ├── 📁 config/                     # Configuration files
    │   ├── config.yaml               # Main configuration
    │   └── schema.yaml               # Data schema
    ├── 📁 logs/                      # Application logs
    ├── 📁 research/                  # Research notebooks
    │   └── notebooks/
    │       └── EDA.ipynb            # Exploratory Data Analysis
    ├── 📁 src/student_performance/   # Source code
    │   ├── 📁 components/            # ML components
    │   │   ├── data_ingestion.py    # Data ingestion
    │   │   ├── data_transformation.py # Data preprocessing
    │   │   ├── model_trainer.py     # Model training
    │   │   └── model_evaluation.py  # Model evaluation
    │   ├── 📁 pipeline/              # ML pipelines
    │   │   ├── training_pipeline.py # Training pipeline
    │   │   └── prediction_pipeline.py # Prediction pipeline
    │   ├── 📁 config/                # Configuration management
    │   ├── 📁 entity/                # Data classes
    │   └── 📁 utils/                 # Utility functions
    ├── 📁 templates/                 # Web templates
    │   ├── index.html               # Home page
    │   └── home.html                # Prediction form
    ├── 📁 tests/                     # Unit tests
    ├── 🐳 Dockerfile                 # Docker configuration
    ├── 📊 dvc.yaml                   # DVC pipeline
    ├── 🚀 app.py                     # Flask web application
    ├── 🎯 main.py                    # Training script
    ├── 📋 requirements.txt           # Dependencies
    └── 📖 README.md                  # Documentation
    """
    
    logger.info(structure)

def main():
    """
    Main demonstration function
    """
    try:
        # Show project structure
        show_project_structure()
        
        # Run training pipeline demonstration
        training_results = demonstrate_training_pipeline()
        
        if training_results:
            # Run prediction pipeline demonstration
            demonstrate_prediction_pipeline()
            
            logger.info("="*60)
            logger.info("🎉 COMPLETE DEMONSTRATION FINISHED SUCCESSFULLY!")
            logger.info("="*60)
            logger.info("Next steps:")
            logger.info("1. Run 'python main.py' to train the model")
            logger.info("2. Run 'python app.py' to start the web application")
            logger.info("3. Open http://localhost:5000 in your browser")
            logger.info("4. Use 'mlflow ui' to view experiment tracking")
            logger.info("="*60)
        else:
            logger.error("Training pipeline failed. Please check the logs.")
    
    except Exception as e:
        logger.error(f"Demonstration failed: {str(e)}")

if __name__ == "__main__":
    main()
