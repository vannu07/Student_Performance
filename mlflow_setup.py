import os
import mlflow
import dagshub

# DagsHub and MLflow setup
def setup_mlflow_dagshub():
    """
    Setup MLflow with DagsHub integration
    """
    try:
        # DagsHub configuration
        dagshub_url = "https://dagshub.com/api/v1/repo-buckets/s3/vannusingh9"
        
        # Set environment variables for DagsHub
        os.environ["MLFLOW_TRACKING_URI"] = f"{dagshub_url}.mlflow"
        os.environ["MLFLOW_TRACKING_USERNAME"] = "vannusingh9"
        os.environ["MLFLOW_TRACKING_PASSWORD"] = "7dd7114cf62f793c3c5245529383d1aeedfe9d6c"
        
        # Initialize DagsHub
        dagshub.init(repo_owner='vannusingh9', repo_name='Student', mlflow=True)
        
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
