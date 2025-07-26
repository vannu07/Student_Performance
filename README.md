# Student Performance ML Project

End-to-end ML project for predicting student performance using advanced machine learning techniques.

## Project Structure

```
student_performance_ml_project/
├── data/
│   ├── raw/                    # Raw data files
│   ├── processed/              # Processed data files
│   └── external/               # External data sources
├── src/
│   ├── student_performance/
│   │   ├── __init__.py
│   │   ├── components/
│   │   │   ├── __init__.py
│   │   │   ├── data_ingestion.py
│   │   │   ├── data_transformation.py
│   │   │   ├── model_trainer.py
│   │   │   └── model_evaluation.py
│   │   ├── pipeline/
│   │   │   ├── __init__.py
│   │   │   ├── training_pipeline.py
│   │   │   └── prediction_pipeline.py
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   └── common.py
│   │   ├── config/
│   │   │   ├── __init__.py
│   │   │   └── configuration.py
│   │   ├── entity/
│   │   │   ├── __init__.py
│   │   │   └── config_entity.py
│   │   └── constants/
│   │       └── __init__.py
├── config/
│   ├── config.yaml
│   ├── params.yaml
│   └── schema.yaml
├── research/
│   └── notebooks/              # Jupyter notebooks for research
├── artifacts/                  # Model artifacts, logs, etc.
├── logs/                      # Application logs
├── tests/                     # Unit tests
├── deployment/
│   ├── app.py                 # Flask application
│   ├── Dockerfile
│   └── requirements.txt
├── dvc.yaml                   # DVC pipeline configuration
├── params.yaml               # Parameters for experiments
├── requirements.txt          # Python dependencies
├── setup.py                 # Package setup
├── main.py                  # Main training script
└── app.py                   # Web application
```

## Features

- **Data Ingestion**: Automated data collection and validation
- **Data Transformation**: Feature engineering and preprocessing
- **Model Training**: Multiple ML algorithms with hyperparameter tuning
- **Model Evaluation**: Comprehensive model assessment with MLflow tracking
- **MLflow Integration**: Experiment tracking and model registry
- **DagsHub Integration**: Remote experiment tracking and collaboration
- **Deployment Ready**: Flask web application
- **Docker Support**: Containerized deployment

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Initialize MLflow:
```bash
mlflow ui
```

3. Run the training pipeline:
```bash
python main.py
```

4. Start the web application:
```bash
python app.py
```

## Usage

### Training Pipeline
The training pipeline includes:
- Data ingestion from multiple sources
- Data validation and preprocessing
- Feature engineering
- Model training with multiple algorithms
- Model evaluation and comparison
- MLflow experiment tracking

### Web Application
- Interactive web interface for predictions
- Model performance visualization
- Real-time prediction capabilities

## Model Performance

The project supports multiple algorithms:
- Linear Regression
- Random Forest
- XGBoost
- CatBoost
- LightGBM

All models are evaluated using:
- R² Score
- Mean Absolute Error (MAE)
- Root Mean Square Error (RMSE)

## Deployment

The project is deployment-ready with:
- Docker containerization
- Flask web application
- MLflow model serving
- Cloud deployment scripts

## Author

Student Performance ML Project - End-to-end machine learning solution
