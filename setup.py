from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

REPO_NAME = "student_performance_ml_project"
AUTHOR_USER_NAME = "Student Performance Team"
SRC_REPO = "student_performance"
AUTHOR_EMAIL = "team@studentperformance.com"

setup(
    name=SRC_REPO,
    version="0.0.1",
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="End-to-end ML project for predicting student performance",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pandas",
        "numpy",
        "scikit-learn",
        "mlflow",
        "dvc",
        "flask",
        "seaborn",
        "matplotlib",
        "joblib",
        "ensure",
        "PyYAML",
        "tqdm",
        "types-PyYAML",
        "dagshub",
        "xgboost",
        "catboost",
        "lightgbm",
        "optuna"
    ]
)
