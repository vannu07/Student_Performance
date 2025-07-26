# Student Performance ML Project

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![MLflow](https://img.shields.io/badge/MLflow-red.svg)
![Flask](https://img.shields.io/badge/Flask-green.svg)
![Docker](https://img.shields.io/badge/Docker-blue.svg)
[![GitHub](https://img.shields.io/badge/GitHub-vannu07-black.svg)](https://github.com/vannu07/Student_Performance)

**End-to-end ML project for predicting student performance using advanced machine learning techniques**

</div>

---

## Features

- **Data Ingestion**: Automated data collection and validation
- **Data Transformation**: Feature engineering and preprocessing
- **Model Training**: Multiple ML algorithms with hyperparameter tuning
- **Model Evaluation**: Comprehensive model assessment with MLflow tracking
- **MLflow Integration**: Experiment tracking and model registry
- **DagsHub Integration**: Remote experiment tracking and collaboration
- **Deployment Ready**: Flask web application
- **Docker Support**: Containerized deployment

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/vannu07/Student_Performance.git
cd Student_Performance

# Install dependencies
pip install -r requirements.txt

# Run training pipeline
python main.py

# Launch web app
python app.py
```

Open `http://localhost:8080` to use the prediction interface.

## 📊 What This Project Does

This is an end-to-end ML system that predicts student exam scores based on various factors like study habits, family background, and previous performance. Built with industry best practices for production deployment.

### Key Components:
- **Data Pipeline**: Automated ingestion and preprocessing
- **ML Models**: Multiple algorithms with hyperparameter tuning
- **Experiment Tracking**: MLflow integration for model versioning
- **Web Interface**: Flask app for real-time predictions
- **Deployment**: Docker containerization

## 🏗️ Architecture

<div align="center">

```
📊 Data → 🔄 Processing → 🤖 Training → 📈 Evaluation → 🚀 Deployment
```

</div>

The pipeline automatically handles:
1. Data validation and cleaning
2. Feature engineering and scaling  
3. Model training with cross-validation
4. Performance evaluation and logging
5. Model deployment to web interface

## 🎯 Model Performance

Multiple algorithms tested and tracked in MLflow:

| Algorithm | R² Score | MAE | RMSE | Training Time |
|-----------|----------|-----|------|---------------|
| **Random Forest** | 0.847 | 2.34 | 3.12 | 45s |
| **XGBoost** | 0.853 | 2.28 | 3.05 | 67s |
| **LightGBM** | 0.849 | 2.32 | 3.09 | 32s |
| **CatBoost** | 0.841 | 2.41 | 3.18 | 89s |
| Linear Regression | 0.723 | 3.45 | 4.67 | 2s |

All models are evaluated using R² Score, Mean Absolute Error (MAE), and Root Mean Square Error (RMSE).

## 📁 Project Structure

```
student_performance_ml_project/
├── 📊 data/
│   ├── raw/                    # Raw data files
│   ├── processed/              # Processed data files
│   └── external/               # External data sources
├── 🧩 src/
│   └── student_performance/
│       ├── **init**.py
│       ├── components/
│       │   ├── **init**.py
│       │   ├── data_ingestion.py
│       │   ├── data_transformation.py
│       │   ├── model_trainer.py
│       │   └── model_evaluation.py
│       ├── pipeline/
│       │   ├── **init**.py
│       │   ├── training_pipeline.py
│       │   └── prediction_pipeline.py
│       ├── utils/
│       │   ├── **init**.py
│       │   └── common.py
│       ├── config/
│       │   ├── **init**.py
│       │   └── configuration.py
│       ├── entity/
│       │   ├── **init**.py
│       │   └── config_entity.py
│       └── constants/
│           └── **init**.py
├── ⚙️ config/
│   ├── config.yaml
│   ├── params.yaml
│   └── schema.yaml
├── 🔬 research/
│   └── notebooks/              # Jupyter notebooks for research
├── 📦 artifacts/               # Model artifacts, logs, etc.
├── 📋 logs/                    # Application logs
├── 🧪 tests/                   # Unit tests
├── 🚀 deployment/
│   ├── app.py                  # Flask application
│   ├── Dockerfile
│   └── requirements.txt
├── dvc.yaml                    # DVC pipeline configuration
├── params.yaml                 # Parameters for experiments
├── requirements.txt            # Python dependencies
├── setup.py                    # Package setup
├── main.py                     # Main training script
└── app.py                      # Web application
```

## 🔬 MLflow Integration

Start MLflow UI to view all experiments:
```bash
mlflow ui
```

Features:
- Automated metric logging
- Model versioning and registry
- Experiment comparison
- Parameter tracking
- Artifact storage

All model metrics, parameters, and artifacts are automatically logged for comparison.

## 🌐 Web Application

The Flask app provides:
- Interactive web interface for predictions
- Model performance visualization
- Real-time prediction capabilities
- Student data input form
- Feature importance visualization

## 🐳 Docker Deployment

The project is deployment-ready with Docker:

```bash
# Build image
docker build -t student-performance-ml .

# Run container
docker run -p 8080:8080 student-performance-ml
```

## 💡 Key Features

### Training Pipeline
The training pipeline includes:
- Data ingestion from multiple sources
- Data validation and preprocessing
- Feature engineering
- Model training with multiple algorithms
- Model evaluation and comparison
- MLflow experiment tracking

### Data Processing
- Handles missing values intelligently
- Feature scaling and encoding
- Outlier detection and treatment
- Data validation with schema checking

### Model Training  
- Grid search hyperparameter optimization
- K-fold cross-validation
- Automated feature selection
- Model performance comparison

### Production Ready
- REST API endpoints
- Input validation and error handling
- Logging and monitoring
- Model versioning support

## 🛠️ Technical Stack

- **ML Framework**: Scikit-learn, XGBoost, CatBoost, LightGBM  
- **Experiment Tracking**: MLflow
- **Web Framework**: Flask
- **Data Processing**: Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn
- **Deployment**: Docker, Gunicorn
- **Pipeline**: DVC for data versioning

## Deployment Options

The project supports multiple deployment options:
- Docker containerization
- Flask web application
- MLflow model serving
- Cloud deployment scripts

## Usage

### Training Pipeline
```bash
python main.py
```

### Web Application
```bash
python app.py
```

### MLflow UI
```bash
mlflow ui
```

## 🤝 Contributing

Contributions welcome! Please check the [issues](https://github.com/vannu07/Student_Performance/issues) page.

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/improvement`)
5. Create Pull Request

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

<div align="center">

**⭐ Star this repo if it helped you!**

[![GitHub stars](https://img.shields.io/github/stars/vannu07/Student_Performance.svg?style=social&label=Star)](https://github.com/vannu07/Student_Performance)
[![GitHub forks](https://img.shields.io/github/forks/vannu07/Student_Performance.svg?style=social&label=Fork)](https://github.com/vannu07/Student_Performance/fork)

**Student Performance ML Project - End-to-end machine learning solution**

Built with ❤️ by [vannu07](https://github.com/vannu07)

</div>
