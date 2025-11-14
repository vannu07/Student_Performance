import os
import mlflow
import dagshub

# DagsHub and MLflow setup
def setup_mlflow_dagshub():
    """
    Setup MLflow with DagsHub integration
    """
    try:
        # DagsHub / MLflow configuration
        # Prefer values from environment variables for safety. If not set,
        # fall back to a reasonable default for the tracking URI only.
        default_dagshub = "https://dagshub.com/api/v1/repo-buckets/s3/vannusingh9"
        dagshub_url = os.getenv("MLFLOW_TRACKING_URI", default_dagshub + ".mlflow")

        # Set tracking URI (non-secret)
        os.environ["MLFLOW_TRACKING_URI"] = dagshub_url

        # Credentials MUST be provided through environment variables or a secrets store.
        username = os.getenv("MLFLOW_TRACKING_USERNAME")
        password = os.getenv("MLFLOW_TRACKING_PASSWORD")
        if username and password:
            os.environ["MLFLOW_TRACKING_USERNAME"] = username
            os.environ["MLFLOW_TRACKING_PASSWORD"] = password
        else:
            print("MLflow credentials not found in environment. Set MLFLOW_TRACKING_USERNAME and MLFLOW_TRACKING_PASSWORD via env/GitHub Secrets.")

        # Initialize DagsHub integration (repo info is public metadata)
        dagshub.init(repo_owner=os.getenv('DAGSHUB_REPO_OWNER', 'vannusingh9'),
                     repo_name=os.getenv('DAGSHUB_REPO_NAME', 'Student'),
                     mlflow=True)
        
        print("MLflow and DagsHub setup completed successfully!")
        print(f"MLflow Tracking URI: {mlflow.get_tracking_uri()}")
        
        return True
        
    except Exception as e:
        print(f"Error setting up MLflow/DagsHub: {str(e)}")
        return False

def create_mlflow_experiment():
    """
    Create MLflow experiment for student performance prediction
    """
    try:
        experiment_name = "Student Performance Prediction"
        
        # Create or get experiment
        try:
            experiment_id = mlflow.create_experiment(experiment_name)
            print(f"Created new experiment: {experiment_name} with ID: {experiment_id}")
        except mlflow.exceptions.MlflowException:
            experiment = mlflow.get_experiment_by_name(experiment_name)
            experiment_id = experiment.experiment_id
            print(f"Using existing experiment: {experiment_name} with ID: {experiment_id}")
        
        # Set the experiment
        mlflow.set_experiment(experiment_name)
        
        return experiment_id
        
    except Exception as e:
        print(f"Error creating MLflow experiment: {str(e)}")
        return None

if __name__ == "__main__":
    # Setup MLflow and DagsHub
    setup_success = setup_mlflow_dagshub()
    
    if setup_success:
        # Create experiment
        experiment_id = create_mlflow_experiment()
        
        if experiment_id:
            print("MLflow setup completed successfully!")
        else:
            print("Failed to create MLflow experiment")
    else:
        print("Failed to setup MLflow/DagsHub")
