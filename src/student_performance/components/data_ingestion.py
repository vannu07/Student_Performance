import os
import shutil
import zipfile
from src.student_performance import logger
from src.student_performance.utils.common import get_size
from src.student_performance.entity.config_entity import DataIngestionConfig
from pathlib import Path
import pandas as pd

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def copy_local_file(self):
        """Copy local dataset file to artifacts directory"""
        try:
            # Ensure the target directory exists
            os.makedirs(os.path.dirname(self.config.local_data_file), exist_ok=True)
            
            # Check if target file already exists
            if not os.path.exists(self.config.local_data_file):
                # Copy from local data folder to artifacts
                source_path = self.config.source_URL  # Now points to local file
                
                if os.path.exists(source_path):
                    shutil.copy2(source_path, self.config.local_data_file)
                    logger.info(f"File copied from {source_path} to {self.config.local_data_file}")
                    logger.info(f"File size: {get_size(Path(self.config.local_data_file))}")
                else:
                    raise FileNotFoundError(f"Source dataset file not found at: {source_path}")
            else:
                logger.info(f"File already exists of size: {get_size(Path(self.config.local_data_file))}")
                
        except Exception as e:
            logger.error(f"Error copying local file: {str(e)}")
            raise e

    def extract_zip_file(self):
        """
        zip_file_path: str
        Extracts the zip file into the data directory
        Function returns None
        """
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)

    def initiate_data_ingestion(self):
        """
        This function initiates the data ingestion process
        """
        try:
            logger.info("Starting data ingestion process")
            
            # Copy the local data file to artifacts directory
            self.copy_local_file()
            
            # If it's a zip file, extract it
            if Path(self.config.local_data_file).suffix == '.zip':
                self.extract_zip_file()
            
            # Track the final data file path
            final_data_file = str(self.config.local_data_file)
            
            # If it's an Excel file, convert to CSV for easier processing
            if str(self.config.local_data_file).endswith('.xlsx'):
                csv_file = self.convert_excel_to_csv()
                final_data_file = csv_file
                logger.info(f"Excel file converted to CSV: {csv_file}")
            
            # Validate the data file exists
            if os.path.exists(final_data_file):
                logger.info("Data ingestion completed successfully")
                
                # Get and log data information using the final file path
                self.get_data_info_from_file(final_data_file)
                
                return final_data_file
            else:
                raise Exception("Data file not found after ingestion")
                
        except Exception as e:
            logger.error(f"Error in data ingestion: {str(e)}")
            raise e

    def convert_excel_to_csv(self):
        """
        Convert Excel file to CSV for easier processing
        """
        try:
            if self.config.local_data_file.endswith('.xlsx'):
                # Read Excel file
                df = pd.read_excel(self.config.local_data_file)
                
                # Create CSV file path
                csv_path = self.config.local_data_file.replace('.xlsx', '.csv')
                
                # Save as CSV
                df.to_csv(csv_path, index=False)
                logger.info(f"Converted Excel file to CSV: {csv_path}")
                
                # Return CSV path instead of modifying frozen dataclass
                return csv_path
            else:
                return str(self.config.local_data_file)
                
        except Exception as e:
            logger.error(f"Error converting Excel to CSV: {str(e)}")
            raise e

    def get_data_info(self):
        """
        Get basic information about the ingested data
        """
        return self.get_data_info_from_file(str(self.config.local_data_file))
    
    def get_data_info_from_file(self, file_path):
        """
        Get basic information about the ingested data from a specific file path
        """
        try:
            # Determine file type and read accordingly
            if file_path.endswith('.xlsx'):
                df = pd.read_excel(file_path)
            else:
                df = pd.read_csv(file_path)
                
            logger.info(f"Data shape: {df.shape}")
            logger.info(f"Data columns: {list(df.columns)}")
            logger.info(f"Data types: \n{df.dtypes}")
            logger.info(f"Missing values: \n{df.isnull().sum()}")
            logger.info(f"Data description: \n{df.describe()}")
            
            # Log categorical column unique values
            categorical_cols = df.select_dtypes(include=['object']).columns
            for col in categorical_cols:
                unique_vals = df[col].unique()
                logger.info(f"Unique values in {col}: {unique_vals}")
            
            return df
        except Exception as e:
            logger.error(f"Error getting data info: {str(e)}")
            return None
